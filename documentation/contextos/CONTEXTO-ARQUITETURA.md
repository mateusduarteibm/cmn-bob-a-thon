# Contexto: Arquitetura Bob Learning Hub

> **Uso deste documento**: Forneça este arquivo como contexto em solicitações relacionadas à arquitetura, estrutura de código e padrões de design dos repositórios do Bob Learning Hub. Ele consolida os padrões arquiteturais, organização de código e decisões técnicas de ambos os repositórios (frontend e backend).

---

## 1. Visão Geral da Arquitetura

O Bob Learning Hub utiliza uma arquitetura moderna de aplicação web separando claramente as responsabilidades entre frontend e backend:

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Angular 17)                    │
│                    fed-bob-a-thon                            │
│  - Interface do usuário                                      │
│  - State management com Signals                              │
│  - Comunicação HTTP                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │ (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│              BACKEND FOR FRONTEND (Spring Boot 3)            │
│                    bff-bob-a-thon                            │
│  - API REST                                                  │
│  - Lógica de negócio                                         │
│  - Validações                                                │
│  - Tratamento de erros                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
              [Futuras integrações]
           - Banco de dados
           - Serviços externos
           - Cache
```

### Princípios Arquiteturais

1. **Separação de Responsabilidades**: Frontend cuida da apresentação, Backend cuida da lógica de negócio
2. **Clean Architecture**: Backend organizado em camadas bem definidas (Adapters, Domain, Use Cases)
3. **API-First**: Contrato de API bem definido e documentado (OpenAPI/Swagger)
4. **Stateless**: Backend não mantém estado de sessão (preparado para escalabilidade horizontal)
5. **Type-Safe**: Uso de TypeScript no frontend e Java com tipagem forte no backend

---

## 2. Arquitetura do Backend (`bff-bob-a-thon`)

### 2.1. Padrão Arquitetural: Hexagonal Architecture (Ports & Adapters)

O backend segue os princípios da **Clean Architecture** e **Hexagonal Architecture**, organizando o código em camadas concêntricas onde as dependências apontam sempre para dentro (em direção ao domínio).

```
┌─────────────────────────────────────────────────────────────┐
│                    ADAPTER (INPUT)                           │
│  - Controllers REST                                          │
│  - DTOs de entrada/saída                                     │
│  - Mappers                                                   │
│  - Exception Handlers                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                       DOMAIN                                 │
│  - Entidades de negócio (Content)                            │
│  - Exceções de domínio                                       │
│  - Serviços de domínio                                       │
│  - Regras de negócio                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   ADAPTER (OUTPUT)                           │
│  - Repositórios (atualmente in-memory)                       │
│  - Integrações externas (futuro)                             │
│  - Persistência (futuro)                                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Estrutura de Diretórios

```
src/main/java/com/hackathon/bffbobathon/
├── Application.java                          # Classe principal Spring Boot
├── adapter/
│   ├── input/                                # Camada de entrada (Controllers)
│   │   ├── controller/
│   │   │   └── ContentController.java        # REST Controller
│   │   ├── dto/                              # Data Transfer Objects
│   │   │   ├── ContentDTO.java               # DTO de resposta
│   │   │   ├── CreateContentRequest.java     # DTO de criação
│   │   │   └── UpdateContentRequest.java     # DTO de atualização
│   │   ├── exception/                        # Tratamento de exceções
│   │   │   ├── ErrorResponse.java            # Resposta de erro padrão
│   │   │   ├── ValidationErrorResponse.java  # Resposta de erro de validação
│   │   │   └── GlobalExceptionHandler.java   # Handler global de exceções
│   │   └── mapper/
│   │       └── ContentMapper.java            # MapStruct mapper
│   └── output/                               # Camada de saída (Repositórios)
│       ├── database/                         # (Futuro: JPA entities)
│       └── memory/
│           └── ContentRepository.java        # Repositório in-memory
├── config/                                   # Configurações Spring
│   ├── CorsConfig.java                       # Configuração CORS
│   └── OpenApiConfig.java                    # Configuração Swagger
└── domain/                                   # Camada de domínio
    ├── entity/
    │   ├── Content.java                      # Entidade de domínio
    │   └── ContentType.java                  # Enum de tipos
    ├── exception/
    │   └── ContentNotFoundException.java     # Exceção de domínio
    └── service/
        └── ContentService.java               # Serviço de domínio

src/main/resources/
└── application.yml                           # Configurações da aplicação
```

### 2.3. Camadas e Responsabilidades

#### Adapter Input (Entrada)

**Responsabilidade**: Receber requisições HTTP, validar entrada, converter para objetos de domínio e retornar respostas.

**Componentes principais**:

- **Controllers**: Endpoints REST anotados com `@RestController`
  - Usam `@RequiredArgsConstructor` (Lombok) para injeção de dependências
  - Documentados com anotações OpenAPI (`@Operation`, `@ApiResponse`)
  - Retornam `ResponseEntity<T>` com status HTTP apropriado

- **DTOs**: Objetos de transferência de dados
  - Usam Bean Validation (`@NotBlank`, `@Size`, `@Pattern`)
  - Separados por operação (Request/Response)
  - Construídos com Lombok (`@Builder`, `@Getter`, `@Setter`)

- **Mappers**: Conversão entre DTOs e entidades de domínio
  - Implementados com MapStruct (`@Mapper(componentModel = "spring")`)
  - Conversão automática de tipos compatíveis
  - Métodos para conversão de listas

- **Exception Handlers**: Tratamento centralizado de exceções
  - `@RestControllerAdvice` para captura global
  - Métodos específicos para cada tipo de exceção (`@ExceptionHandler`)
  - Retornam respostas padronizadas com timestamp, status e mensagem

**Exemplo de Controller**:
```java
@RestController
@RequestMapping("/contents")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Contents", description = "API para gerenciamento de conteúdos")
public class ContentController {
    private final ContentService contentService;
    private final ContentMapper contentMapper;

    @GetMapping
    @Operation(summary = "Listar conteúdos")
    public ResponseEntity<List<ContentDTO>> getAllContents() {
        List<Content> contents = contentService.getAllContents();
        return ResponseEntity.ok(contentMapper.toDTOList(contents));
    }
}
```

#### Domain (Domínio)

**Responsabilidade**: Conter a lógica de negócio, regras de domínio e entidades principais.

**Componentes principais**:

- **Entities**: Objetos de domínio puros (POJOs)
  - Sem anotações de persistência (JPA-free)
  - Usam Lombok para reduzir boilerplate
  - `@EqualsAndHashCode(of = "id")` para comparação por ID

- **Services**: Lógica de negócio e orquestração
  - Anotados com `@Service`
  - Usam `@RequiredArgsConstructor` para injeção
  - Contêm regras de validação e transformação
  - Lançam exceções de domínio quando necessário

- **Exceptions**: Exceções específicas do domínio
  - Estendem `RuntimeException`
  - Mensagens descritivas e contextualizadas
  - Capturadas pelo `GlobalExceptionHandler`

**Exemplo de Entidade**:
```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(of = "id")
@ToString
public class Content {
    private Long id;
    private String name;
    private String description;
    private String imageUrl;
}
```

#### Adapter Output (Saída)

**Responsabilidade**: Implementar interfaces de saída (repositórios, integrações externas).

**Componentes principais**:

- **Repositories**: Implementação de persistência
  - Atualmente: `ContentRepository` in-memory com `ConcurrentHashMap`
  - Futuro: Implementações JPA para banco de dados real
  - Thread-safe usando `AtomicLong` para geração de IDs

**Exemplo de Repositório In-Memory**:
```java
@Repository
public class ContentRepository {
    private final Map<Long, Content> contents = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    public Content save(Content content) {
        if (content.getId() == null) {
            content.setId(idGenerator.getAndIncrement());
        }
        contents.put(content.getId(), content);
        return content;
    }
}
```

### 2.4. Stack Tecnológica Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Java | 17 | Linguagem base |
| Spring Boot | 3.2.5 | Framework principal |
| Spring Web | 3.2.5 | REST Controllers |
| Spring Validation | 3.2.5 | Bean Validation |
| Spring Actuator | 3.2.5 | Health checks e métricas |
| Lombok | 1.18.30 | Redução de boilerplate |
| MapStruct | 1.5.5.Final | Mapeamento de objetos |
| Springdoc OpenAPI | 2.5.0 | Documentação Swagger |
| Maven | 3.x | Build e gerenciamento de dependências |

### 2.5. Configurações Importantes

#### application.yml

```yaml
spring:
  application:
    name: bff-bob-a-thon
  jackson:
    serialization:
      write-dates-as-timestamps: false
    time-zone: America/Sao_Paulo

server:
  port: ${SERVER_PORT:8080}
  servlet:
    context-path: /api

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics

springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
```

**Pontos-chave**:
- Context path: `/api` (todos os endpoints começam com `/api`)
- Porta configurável via variável de ambiente `SERVER_PORT`
- Jackson configurado para timezone de São Paulo
- Actuator expõe health, info e metrics
- Swagger UI disponível em `/api/swagger-ui.html`

#### CORS Configuration

```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.setAllowedOriginPatterns(List.of("*"));
        config.setAllowedHeaders(Arrays.asList(
            "Origin", "Content-Type", "Accept", "Authorization"
        ));
        config.setAllowedMethods(Arrays.asList(
            "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
        ));
        config.setMaxAge(3600L);
        // ...
    }
}
```

**Pontos-chave**:
- Permite todas as origens (desenvolvimento)
- Suporta credenciais
- Todos os métodos HTTP permitidos
- Cache de 1 hora para preflight requests

---

## 3. Arquitetura do Frontend (`fed-bob-a-thon`)

### 3.1. Padrão Arquitetural: Component-Based Architecture

O frontend utiliza **Angular 17** com **Standalone Components** (sem NgModules), seguindo uma arquitetura baseada em componentes reativos com Signals.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  - Components (Standalone)                                   │
│  - Templates (HTML)                                          │
│  - Styles (SCSS)                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     STATE MANAGEMENT                         │
│  - Angular Signals                                           │
│  - Computed values                                           │
│  - Reactive state                                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    DATA ACCESS LAYER                         │
│  - HttpClient                                                │
│  - API calls                                                 │
│  - Error handling                                            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2. Estrutura de Diretórios

```
src/
├── main.ts                           # Bootstrap da aplicação
├── index.html                        # HTML principal
├── styles.scss                       # Estilos globais
└── app/
    ├── app.component.ts              # Componente raiz
    ├── app.component.html            # Template raiz
    ├── app.component.scss            # Estilos do componente raiz
    ├── app.config.ts                 # Configuração da aplicação
    └── app.routes.ts                 # Definição de rotas

Estrutura futura recomendada:
src/app/
├── core/                             # Serviços singleton, guards, interceptors
│   ├── services/
│   ├── guards/
│   └── interceptors/
├── features/                         # Módulos de funcionalidade
│   └── {feature}/
│       ├── components/
│       ├── services/
│       └── models/
└── shared/                           # Componentes, pipes e diretivas reutilizáveis
    ├── components/
    ├── pipes/
    └── directives/
```

### 3.3. Padrões de Código Angular

#### Standalone Components

**Todos os componentes são standalone** (sem NgModules):

```typescript
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],  // Importa dependências diretamente
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  // ...
}
```

**Vantagens**:
- Menos boilerplate
- Imports explícitos e claros
- Melhor tree-shaking
- Mais fácil de testar

#### Angular Signals para State Management

O projeto usa **Angular Signals** para gerenciamento de estado reativo:

```typescript
export class AppComponent {
  // Signals básicos
  protected readonly isLoading = signal(true);
  protected readonly selectedCategory = signal('All');
  protected readonly courses = signal<CourseItem[]>([]);

  // Computed signals (derivados)
  protected readonly featuredCourse = computed(() => 
    this.courses()[0] ?? null
  );

  protected readonly filteredCourses = computed(() => {
    const activeCategory = this.selectedCategory();
    const items = this.courses();
    return activeCategory === 'All' 
      ? items 
      : items.filter(c => c.category === activeCategory);
  });
}
```

**Características dos Signals**:
- **Reatividade automática**: Templates atualizam quando signals mudam
- **Computed values**: Valores derivados recalculados automaticamente
- **Type-safe**: Totalmente tipados com TypeScript
- **Performance**: Apenas o necessário é recalculado

#### Dependency Injection com inject()

Uso da função `inject()` em vez de constructor injection:

```typescript
export class AppComponent {
  #http = inject(HttpClient);  // Private field com ES private syntax

  constructor() {
    this.loadCourses();
  }

  private loadCourses(): void {
    this.#http.get<ApiCourse[]>('url').subscribe({
      next: (response) => this.courses.set(response),
      error: () => this.errorMessage.set('Erro ao carregar')
    });
  }
}
```

**Vantagens**:
- Mais conciso
- Permite injeção fora do constructor
- Suporta ES private fields (`#field`)

#### Template Syntax Moderno

Uso de **control flow** nativo do Angular 17:

```html
<!-- Conditional rendering -->
@if (isLoading()) {
  <div class="loading">Carregando...</div>
} @else if (errorMessage()) {
  <div class="error">{{ errorMessage() }}</div>
} @else {
  <div class="content">...</div>
}

<!-- List rendering -->
@for (course of filteredCourses(); track course.id) {
  <div class="course-card">{{ course.title }}</div>
} @empty {
  <div class="empty">Nenhum curso encontrado</div>
}
```

**Vantagens sobre diretivas estruturais antigas**:
- Sintaxe mais limpa e legível
- Melhor performance
- Suporte a `@empty` para listas vazias
- `track` obrigatório para otimização

### 3.4. Stack Tecnológica Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Angular | 17.3.0 | Framework principal |
| TypeScript | 5.4.2 | Linguagem base |
| RxJS | 7.8.0 | Programação reativa |
| Angular Signals | 17.3.0 | State management |
| SCSS | - | Estilização |
| Jasmine | 5.1.0 | Framework de testes |
| Karma | 6.4.0 | Test runner |

### 3.5. Configurações Importantes

#### tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "target": "ES2022",
    "module": "ES2022"
  },
  "angularCompilerOptions": {
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}
```

**Pontos-chave**:
- **Strict mode** habilitado (máxima segurança de tipos)
- Target ES2022 (features modernas)
- Angular compiler em modo strict

#### angular.json

```json
{
  "schematics": {
    "@schematics/angular:component": {
      "style": "scss",
      "skipTests": true  // Testes não gerados por padrão
    }
  }
}
```

**Nota**: O projeto está configurado para **não gerar testes automaticamente**. Isso deve ser alterado em projetos de produção.

#### app.config.ts

```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideRouter(routes)
  ]
};
```

**Configuração minimalista**:
- HttpClient configurado globalmente
- Router configurado com rotas vazias (expandir conforme necessário)

---

## 4. Comunicação Frontend-Backend

### 4.1. Protocolo de Comunicação

- **Protocolo**: HTTP/HTTPS
- **Formato**: JSON
- **Content-Type**: `application/json`
- **Base URL Backend**: `https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com/api`

### 4.2. Fluxo de Requisição

```
┌─────────────┐                                    ┌─────────────┐
│   Angular   │                                    │ Spring Boot │
│  Component  │                                    │  Controller │
└──────┬──────┘                                    └──────┬──────┘
       │                                                  │
       │ 1. User action (click, load)                    │
       │                                                  │
       │ 2. HttpClient.get/post()                        │
       ├─────────────────────────────────────────────────>│
       │         HTTP Request (JSON)                      │
       │                                                  │
       │                                          3. Validate input
       │                                          4. Call service
       │                                          5. Process business logic
       │                                                  │
       │<─────────────────────────────────────────────────┤
       │         HTTP Response (JSON)                     │
       │                                                  │
       │ 6. Update signals                               │
       │ 7. Template auto-updates                        │
       │                                                  │
```

### 4.3. Exemplo de Integração

**Frontend (Angular)**:
```typescript
private loadCourses(): void {
  this.isLoading.set(true);
  this.errorMessage.set('');

  this.#http
    .get<ApiCourse[]>('https://bff-bob-a-thon.../api/contents')
    .subscribe({
      next: (response) => {
        this.courses.set(response.map(this.mapCourse));
        this.isLoading.set(false);
      },
      error: () => {
        this.errorMessage.set('Erro ao carregar cursos');
        this.isLoading.set(false);
      }
    });
}
```

**Backend (Spring Boot)**:
```java
@GetMapping
public ResponseEntity<List<ContentDTO>> getAllContents() {
    log.info("GET /contents - Listando todos os conteúdos");
    List<Content> contents = contentService.getAllContents();
    List<ContentDTO> response = contentMapper.toDTOList(contents);
    return ResponseEntity.ok(response);
}
```

### 4.4. Tratamento de Erros

**Backend**: Retorna respostas padronizadas com status HTTP apropriado

```java
@ExceptionHandler(ContentNotFoundException.class)
public ResponseEntity<ErrorResponse> handleContentNotFound(ContentNotFoundException ex) {
    ErrorResponse error = ErrorResponse.builder()
        .timestamp(LocalDateTime.now())
        .status(HttpStatus.NOT_FOUND.value())
        .error("Not Found")
        .message(ex.getMessage())
        .build();
    return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
}
```

**Frontend**: Captura erros no `subscribe` e atualiza estado

```typescript
.subscribe({
  next: (data) => { /* sucesso */ },
  error: (err) => {
    this.errorMessage.set('Mensagem amigável para o usuário');
    console.error('Erro detalhado:', err);
  }
});
```

---

## 5. Padrões de Design Utilizados

### 5.1. Backend

| Padrão | Onde | Propósito |
|--------|------|-----------|
| **Hexagonal Architecture** | Estrutura geral | Separação de camadas e inversão de dependências |
| **Repository Pattern** | `ContentRepository` | Abstração de persistência |
| **DTO Pattern** | `adapter/input/dto` | Separação entre API e domínio |
| **Mapper Pattern** | `ContentMapper` | Conversão entre DTOs e entidades |
| **Service Layer** | `ContentService` | Encapsulamento de lógica de negócio |
| **Exception Handler** | `GlobalExceptionHandler` | Tratamento centralizado de erros |
| **Builder Pattern** | Lombok `@Builder` | Construção fluente de objetos |
| **Dependency Injection** | Spring `@Autowired` | Inversão de controle |

### 5.2. Frontend

| Padrão | Onde | Propósito |
|--------|------|-----------|
| **Component-Based** | Estrutura geral | Modularização da UI |
| **Reactive Programming** | Signals, RxJS | Estado reativo e assíncrono |
| **Observer Pattern** | `subscribe()` | Reação a mudanças de dados |
| **Computed Values** | `computed()` | Valores derivados automaticamente |
| **Dependency Injection** | `inject()` | Inversão de controle |
| **Adapter Pattern** | `mapCourse()` | Adaptação de dados da API |

---

## 6. Decisões Arquiteturais Importantes

### 6.1. Por que Hexagonal Architecture no Backend?

**Vantagens**:
- ✅ Domínio isolado de frameworks e bibliotecas
- ✅ Fácil de testar (mock de adapters)
- ✅ Flexível para mudanças de infraestrutura (trocar banco, adicionar cache)
- ✅ Código organizado e fácil de navegar

**Trade-offs**:
- ⚠️ Mais arquivos e camadas (maior complexidade inicial)
- ⚠️ Curva de aprendizado para desenvolvedores novos

### 6.2. Por que Standalone Components no Frontend?

**Vantagens**:
- ✅ Menos boilerplate (sem NgModules)
- ✅ Imports explícitos e claros
- ✅ Melhor tree-shaking (bundles menores)
- ✅ Mais fácil de testar

**Trade-offs**:
- ⚠️ Requer Angular 14+ (não compatível com versões antigas)

### 6.3. Por que Angular Signals em vez de RxJS para estado?

**Vantagens**:
- ✅ Sintaxe mais simples e intuitiva
- ✅ Melhor performance (fine-grained reactivity)
- ✅ Menos código boilerplate
- ✅ Integração nativa com templates

**Trade-offs**:
- ⚠️ RxJS ainda necessário para operações assíncronas complexas
- ⚠️ Signals são relativamente novos (Angular 16+)

### 6.4. Por que Repositório In-Memory?

**Decisão temporária para MVP**:
- ✅ Desenvolvimento rápido sem setup de banco
- ✅ Fácil de testar e demonstrar
- ✅ Preparado para migração futura (interface já definida)

**Próximos passos**:
- 🔄 Implementar persistência com PostgreSQL/MongoDB
- 🔄 Adicionar camada de cache (Redis)
- 🔄 Implementar autenticação e autorização

---

## 7. Boas Práticas Implementadas

### 7.1. Backend

✅ **Validação de entrada**: Bean Validation em DTOs  
✅ **Tratamento de erros**: GlobalExceptionHandler centralizado  
✅ **Logging estruturado**: Slf4j com níveis apropriados  
✅ **Documentação de API**: OpenAPI/Swagger completo  
✅ **CORS configurado**: Permite integração com frontend  
✅ **Health checks**: Spring Actuator para monitoramento  
✅ **Código limpo**: Lombok reduz boilerplate  
✅ **Separação de responsabilidades**: Camadas bem definidas  

### 7.2. Frontend

✅ **TypeScript strict mode**: Máxima segurança de tipos  
✅ **Standalone components**: Arquitetura moderna  
✅ **Signals para estado**: Reatividade nativa  
✅ **Control flow nativo**: Sintaxe moderna de templates  
✅ **ES private fields**: Encapsulamento real (`#field`)  
✅ **Tratamento de erros**: Estados de loading e erro  
✅ **Type-safe HTTP**: Interfaces para respostas da API  
✅ **Computed values**: Lógica derivada automática  

---

## 8. Próximos Passos Arquiteturais

### 8.1. Backend

1. **Persistência real**: Implementar JPA com PostgreSQL
2. **Autenticação**: JWT + Spring Security
3. **Cache**: Redis para otimização
4. **Testes**: Cobertura de testes unitários e integração
5. **CI/CD**: Pipeline automatizado
6. **Observabilidade**: Logs estruturados, métricas, tracing

### 8.2. Frontend

1. **Roteamento**: Implementar navegação entre páginas
2. **Lazy loading**: Carregar features sob demanda
3. **State management avançado**: Serviços compartilhados com Signals
4. **Testes**: Cobertura de testes unitários e E2E
5. **PWA**: Transformar em Progressive Web App
6. **Acessibilidade**: ARIA labels, navegação por teclado

### 8.3. Infraestrutura

1. **Containerização**: Docker para ambos os serviços
2. **Orquestração**: Kubernetes para deploy
3. **API Gateway**: Centralizar roteamento e segurança
4. **CDN**: Servir assets estáticos do frontend
5. **Monitoramento**: Prometheus + Grafana

---

## 9. Referências e Recursos

### Documentação Oficial

- [Angular Documentation](https://angular.io/docs)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### Padrões e Práticas

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Angular Signals](https://angular.io/guide/signals)
- [MapStruct](https://mapstruct.org/)
- [OpenAPI Specification](https://swagger.io/specification/)

---

**Última atualização**: 2026-05-21  
**Versão do documento**: 1.0.0