# Contexto: Bob Learning Hub — Plataforma de Aprendizado

> **Uso deste documento**: Forneça este arquivo como contexto único em novas solicitações relacionadas ao Bob Learning Hub. Ele consolida a arquitetura, os detalhes técnicos de todos os repositórios e o contexto geral da plataforma — servindo tanto como referência para novas conversas com IA quanto como base para criar especificações técnicas, descrições de histórias de desenvolvimento e critérios de aceite.

---

## 1. Visão Geral da Plataforma

O **Bob Learning Hub** é uma plataforma educacional de código aberto para aprendizado de desenvolvimento full-stack moderno. O projeto demonstra boas práticas de arquitetura, desenvolvimento e documentação de software, servindo como referência para desenvolvedores que desejam aprender padrões modernos de desenvolvimento web.

### Objetivos da Plataforma

- **Educacional**: Fornecer conteúdos de aprendizado estruturados (cursos, tutoriais, artigos)
- **Demonstrativo**: Exemplificar arquitetura moderna de aplicações web (Angular + Spring Boot)
- **Open Source**: Código aberto para estudo e contribuição da comunidade
- **Escalável**: Arquitetura preparada para crescimento e evolução

---

## 2. Arquitetura dos Componentes

```
fed-bob-a-thon  (Frontend — Angular 17)
       │
       ▼
bff-bob-a-thon  (Backend for Frontend — Spring Boot 3)
       │
       ▼
   [Futuras integrações: banco de dados, serviços externos]
```

### Repositórios

| Repositório          | Tipo | Responsabilidade                                                    |
|---------------------|------|---------------------------------------------------------------------|
| `fed-bob-a-thon`    | FED  | Interface do usuário — catálogo de cursos, navegação, filtros       |
| `bff-bob-a-thon`    | BFF  | API REST para gerenciamento de conteúdos educacionais (CRUD)        |
| `cmn-bob-a-thon`    | DOC  | Repositório central de documentação (inventários, mapas, contextos) |

---

## 3. Stack Tecnológica

### Frontend (`fed-bob-a-thon`)
- **Angular**: `17.3.0`
- **TypeScript**: Standalone Components (sem NgModules)
- **State Management**: Angular Signals (reativo, sem bibliotecas externas)
- **HTTP Client**: `HttpClient` nativo do Angular
- **Estilização**: SCSS customizado (sem framework UI externo)
- **Build**: Angular CLI

### Backend (`bff-bob-a-thon`)
- **Java**: `17` (ou superior)
- **Spring Boot**: `3.x`
- **Arquitetura**: Clean Architecture / Hexagonal (Ports & Adapters)
- **API Documentation**: OpenAPI/Swagger
- **Build**: Maven

---

## 4. Serviço: `bff-bob-a-thon`

### Responsabilidade
Backend for Frontend que expõe API REST para gerenciamento de conteúdos educacionais. Responsável por operações CRUD (Create, Read, Update, Delete) de cursos, tutoriais e outros materiais de aprendizado.

### Estrutura de Código (Clean Architecture)

```
adapter/input/
  ContentApiController.java       → REST endpoints
adapter/output/
  [Futuro: persistência, integrações externas]
usecase/
  GetAllContentsUsecase.java
  GetContentByIdUsecase.java
  CreateContentUsecase.java
  DeleteContentUsecase.java
domain/model/
  Content.java                    → Entidade de domínio
config/
  CorsConfiguration.java
  SwaggerConfiguration.java
```

### Endpoints Expostos

> **Base-path**: `/api`

| Método | Path                  | OperationId       | Descrição                    |
|--------|-----------------------|-------------------|------------------------------|
| GET    | `/api/contents`       | getAllContents    | Listar todos os conteúdos    |
| GET    | `/api/contents/{id}`  | getContentById    | Buscar conteúdo por ID       |
| POST   | `/api/contents`       | createContent     | Criar novo conteúdo          |
| DELETE | `/api/contents/{id}`  | deleteContent     | Deletar conteúdo existente   |

### Contratos Principais

**GET `/api/contents`**
```json
Response: [
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "category": "string",
    "author": "string",
    "duration": "string",
    "imageUrl": "string",
    "rating": number,
    "featured": boolean
  }
]
```

**GET `/api/contents/{id}`**
```json
Response: {
  "id": "string",
  "title": "string",
  "description": "string",
  "category": "string",
  "author": "string",
  "duration": "string",
  "imageUrl": "string",
  "rating": number,
  "featured": boolean,
  "content": "string (conteúdo completo do curso)"
}
```

**POST `/api/contents`**
```json
Request: {
  "title": "string",
  "description": "string",
  "category": "string",
  "author": "string",
  "duration": "string",
  "imageUrl": "string (opcional)",
  "rating": number (opcional),
  "featured": boolean (opcional),
  "content": "string"
}

Response: {
  "id": "string (gerado)",
  "title": "string",
  "description": "string",
  ...
}
```

**DELETE `/api/contents/{id}`**
```
Response: 204 No Content
```

### Configurações Técnicas

| Propriedade                | Valor / Padrão | Observação                          |
|----------------------------|----------------|-------------------------------------|
| Porta                      | `8080`         | Configurável via `SERVER_PORT`      |
| CORS                       | Habilitado     | Permite requisições do frontend     |
| Swagger UI                 | `/swagger-ui/index.html` | Documentação interativa  |
| Health Check               | `/actuator/health` | Spring Boot Actuator          |
| Profile ativo              | `default`      | Configurável via `SPRING_PROFILES_ACTIVE` |

### Deployment

- **Plataforma**: AWS Elastic Beanstalk
- **URL de produção**: `https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com`
- **Região**: `us-east-1`

---

## 5. Frontend: `fed-bob-a-thon`

### Responsabilidade
Interface do usuário da plataforma de aprendizado. Exibe catálogo de cursos com filtros por categoria, destaque de cursos em evidência, e navegação intuitiva.

### Estrutura do Projeto

```
src/app/
  app.component.ts              → Componente principal (orquestrador)
  app.component.html            → Template do catálogo
  app.component.scss            → Estilos customizados
  app.config.ts                 → Configuração da aplicação
  app.routes.ts                 → Definição de rotas
models/
  content.model.ts              → Interface do modelo de conteúdo
```

### Arquitetura do Frontend

- **Padrão**: Single Component Application (SCA) — toda lógica no `AppComponent`
- **State Management**: Angular Signals
  - `contents` — lista completa de conteúdos
  - `selectedCategory` — categoria selecionada para filtro
  - `filteredContents` — computed signal com conteúdos filtrados
  - `categories` — computed signal com lista de categorias únicas
  - `isLoading` — estado de carregamento
  - `error` — mensagens de erro

### Integração com Backend

```typescript
// URL base hardcoded (futuramente via environment)
private readonly apiUrl = 'https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com';

// Chamada HTTP
this.http.get<Content[]>(`${this.apiUrl}/api/contents`)
```

**Endpoint consumido:**
- `GET /api/contents` — carrega catálogo completo de cursos

### Funcionalidades Implementadas

1. **Catálogo de Cursos**
   - Exibição em cards responsivos
   - Informações: título, descrição, categoria, autor, duração, rating
   - Imagens ilustrativas

2. **Filtro por Categoria**
   - Botões de categoria gerados dinamicamente
   - Filtro reativo via computed signals
   - Opção "Todos" para remover filtro

3. **Curso em Destaque**
   - Seção especial para curso marcado como `featured: true`
   - Layout diferenciado (hero section)

4. **Tratamento de Erros**
   - Retry automático em caso de falha
   - Mensagens de erro amigáveis
   - Estados de loading

5. **Responsividade**
   - Layout adaptável para mobile, tablet e desktop
   - Grid system com CSS Grid

### Mapeamento de Dados

O frontend trata variações de nomenclatura da API:
```typescript
// Aceita tanto "title" quanto "name"
title: item.title || item.name || 'Sem título'

// Aceita tanto "description" quanto "summary"
description: item.description || item.summary || 'Sem descrição'
```

### Dados de Fallback

Quando a API não retorna campos opcionais, o frontend gera valores padrão:
- **Categorias**: `['Desenvolvimento', 'Design', 'Negócios']`
- **Autores**: `['Instrutor A', 'Instrutor B', 'Instrutor C']`
- **Durações**: `['2h', '4h', '6h', '8h']`
- **Imagens**: URLs de placeholder do Unsplash
- **Ratings**: Valores entre 4.0 e 5.0

---

## 6. Fluxo Principal de Navegação

```
Usuário acessa a aplicação
         │
         ▼
AppComponent.ngOnInit()
         │
         ├─► HTTP GET /api/contents
         │        │
         │        ▼
         │   bff-bob-a-thon processa
         │        │
         │        ▼
         │   Retorna lista de conteúdos
         │
         ▼
Frontend renderiza catálogo
         │
         ├─► Exibe curso em destaque (se houver)
         ├─► Exibe botões de categoria
         └─► Exibe cards de cursos
         │
         ▼
Usuário seleciona categoria
         │
         ▼
Computed signal filtra conteúdos
         │
         ▼
UI atualiza automaticamente (reatividade)
```

---

## 7. Padrões de Desenvolvimento

### Frontend (Angular)

**Convenções de Código:**
- Standalone Components obrigatório (sem NgModules)
- Angular Signals para estado reativo
- `inject()` function em vez de constructor injection
- TypeScript strict mode
- SCSS para estilização

**Estrutura de Componentes:**
```typescript
export class AppComponent {
  // Injeção de dependências
  private readonly http = inject(HttpClient);
  
  // Signals de estado
  contents = signal<Content[]>([]);
  selectedCategory = signal<string>('all');
  
  // Computed signals (derivados)
  filteredContents = computed(() => {
    // lógica de filtro
  });
  
  // Lifecycle hooks
  ngOnInit() {
    this.loadContents();
  }
  
  // Métodos públicos
  selectCategory(category: string) {
    this.selectedCategory.set(category);
  }
}
```

**Boas Práticas:**
- Separação de concerns (template, lógica, estilos)
- Tratamento de erros com retry
- Loading states para melhor UX
- Tipagem forte (evitar `any`)
- Código autodocumentado

### Backend (Spring Boot)

**Arquitetura Hexagonal:**
```
Adapter (Input) → Usecase → Domain Model → Adapter (Output)
```

**Convenções de Código:**
- Clean Architecture / Ports & Adapters
- Separação clara de responsabilidades
- DTOs para contratos de API
- Validações com Bean Validation
- Tratamento de exceções centralizado

**Estrutura de Endpoints:**
```java
@RestController
@RequestMapping("/api/contents")
public class ContentApiController {
    
    private final GetAllContentsUsecase getAllContentsUsecase;
    
    @GetMapping
    public ResponseEntity<List<ContentDto>> getAllContents() {
        return ResponseEntity.ok(getAllContentsUsecase.execute());
    }
}
```

**Boas Práticas:**
- Injeção de dependências via construtor
- Imutabilidade quando possível
- Testes unitários e de integração
- Documentação OpenAPI/Swagger
- Logs estruturados

---

## 8. Configuração de Ambiente

### Pré-requisitos

**Frontend:**
- Node.js 18+ e npm 9+
- Angular CLI 17+

**Backend:**
- Java 17+
- Maven 3.8+

### Executando Localmente

**Frontend:**
```bash
cd repositories/fed-bob-a-thon
npm install
npm start
# Acesse: http://localhost:4200
```

**Backend:**
```bash
cd repositories/bff-bob-a-thon
mvn clean install
mvn spring-boot:run
# Acesse: http://localhost:8080
# Swagger: http://localhost:8080/swagger-ui/index.html
```

### Variáveis de Ambiente

**Frontend:**
```bash
# Futuramente via environment.ts
API_URL=https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com
```

**Backend:**
```bash
SERVER_PORT=8080
SPRING_PROFILES_ACTIVE=dev
# Futuras: DATABASE_URL, JWT_SECRET, AWS_ACCESS_KEY, etc.
```

---

## 9. Testes

### Frontend

**Estratégia de Testes:**
- Testes unitários com Jest
- Testes de componentes com Angular Testing Library
- Testes E2E com Cypress (futuro)

**Cobertura esperada:** ≥ 80%

**Comandos:**
```bash
npm test              # Testes unitários
npm run test:coverage # Relatório de cobertura
npm run e2e           # Testes E2E (futuro)
```

### Backend

**Estratégia de Testes:**
- Testes unitários com JUnit 5
- Testes de integração com Spring Boot Test
- Testes de contrato com Spring Cloud Contract (futuro)

**Cobertura esperada:** ≥ 80%

**Comandos:**
```bash
mvn test                    # Testes unitários
mvn verify                  # Testes de integração
mvn jacoco:report           # Relatório de cobertura
```

---

## 10. Documentação Complementar

### Arquivos de Referência

| Arquivo | Descrição |
|---------|-----------|
| `INVENTARIO-REPOSITORIOS.md` | Índice geral do inventário |
| `INVENTARIO-FED.md` | Detalhes técnicos do frontend |
| `INVENTARIO-BFF.md` | Detalhes técnicos do backend |
| `MAPA-REPOSITORIOS.md` | Mapeamento de endpoints e fluxos |
| `MAPA-REPOSITORIOS-LISTAS.md` | Lista de repositórios por funcionalidade |

### Diagramas

**Arquitetura de Alto Nível:**
```
┌─────────────────┐
│   Navegador     │
│   (Browser)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  fed-bob-a-thon │
│  (Angular 17)   │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│  bff-bob-a-thon │
│  (Spring Boot)  │
└────────┬────────┘
         │
         ▼
   [Futuro: DB]
```

**Fluxo de Dados:**
```
User Action → Component Signal → HTTP Request → BFF → Response → Signal Update → UI Render
```

---

## 11. Contribuindo

### Processo de Desenvolvimento

1. **Fork** do repositório
2. **Clone** local
3. **Branch** para feature/bugfix (`git checkout -b feature/nova-funcionalidade`)
4. **Desenvolvimento** seguindo padrões estabelecidos
5. **Testes** (unitários + integração)
6. **Commit** com mensagens descritivas (Conventional Commits)
7. **Push** para o fork
8. **Pull Request** com descrição detalhada

### Padrões de Commit

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona filtro por autor no catálogo
fix: corrige erro de carregamento em telas mobile
docs: atualiza README com instruções de deploy
test: adiciona testes para ContentService
refactor: reorganiza estrutura de pastas do frontend
```

### Code Review

- Pelo menos 1 aprovação necessária
- Todos os testes devem passar
- Cobertura de código mantida ou aumentada
- Documentação atualizada quando necessário

---

## 12. Requisitos Não Funcionais

| Requisito | Especificação |
|-----------|---------------|
| **Performance** | Tempo de carregamento inicial < 3s |
| **Disponibilidade** | 99.5% uptime (objetivo) |
| **Escalabilidade** | Suportar 1000 usuários simultâneos |
| **Segurança** | HTTPS obrigatório, CORS configurado, sanitização de inputs |
| **Acessibilidade** | WCAG 2.1 Level AA (objetivo) |
| **SEO** | Meta tags, sitemap, robots.txt |
| **Responsividade** | Mobile-first, suporte a tablets e desktops |
| **Compatibilidade** | Navegadores modernos (últimas 2 versões) |
| **Manutenibilidade** | Código limpo, documentado, testado |
| **Observabilidade** | Logs estruturados, métricas, tracing (futuro) |

---

## 13. Glossário

| Termo | Definição |
|-------|-----------|
| **BFF** | Backend for Frontend — API específica para um frontend |
| **FED** | Frontend — aplicação Angular que roda no navegador |
| **Content** | Conteúdo educacional (curso, tutorial, artigo) |
| **Category** | Categoria de conteúdo (ex: Desenvolvimento, Design) |
| **Featured** | Conteúdo em destaque na página principal |
| **Signal** | Primitiva reativa do Angular 17+ para gerenciamento de estado |
| **Computed Signal** | Signal derivado de outros signals (atualiza automaticamente) |
| **Standalone Component** | Componente Angular sem NgModule |
| **Clean Architecture** | Padrão arquitetural com separação de camadas |
| **Hexagonal Architecture** | Arquitetura de Ports & Adapters |
| **Usecase** | Caso de uso — lógica de negócio isolada |

---

## 14. Contatos e Suporte

### Repositórios

- **Frontend**: `repositories/fed-bob-a-thon`
- **Backend**: `repositories/bff-bob-a-thon`
- **Documentação**: `repositories/cmn-bob-a-thon`

### Recursos

- **Issues**: Use GitHub Issues para reportar bugs ou sugerir features
- **Discussions**: Use GitHub Discussions para perguntas e discussões
- **Wiki**: Documentação adicional na Wiki do projeto

---

**Última atualização**: 2026-05-20  
**Versão do documento**: 1.0.0  
**Mantenedores**: Equipe Bob-a-thon