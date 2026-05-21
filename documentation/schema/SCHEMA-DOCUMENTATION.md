# Documentação do Schema JSON-LD — Bob Learning Hub

> **Arquivo de referência**: `bob-learning-hub-schema.jsonld`  
> **Versão**: 1.0.0  
> **Última atualização**: 2026-05-21

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Schema](#estrutura-do-schema)
3. [Vocabulários Utilizados](#vocabulários-utilizados)
4. [Plataforma](#plataforma)
5. [Arquitetura](#arquitetura)
6. [Aplicações](#aplicações)
7. [API REST](#api-rest)
8. [Features](#features)
9. [Capacidades Técnicas](#capacidades-técnicas)
10. [Domínio de Conteúdo](#domínio-de-conteúdo)
11. [Roadmap de Melhorias](#roadmap-de-melhorias)
12. [Como Usar Este Schema](#como-usar-este-schema)

---

## Visão Geral

O schema JSON-LD do Bob Learning Hub é uma **representação semântica completa** da plataforma educacional, incluindo:

- ✅ Arquitetura da plataforma (frontend + backend)
- ✅ APIs REST com todos os endpoints
- ✅ Features implementadas e planejadas
- ✅ Capacidades técnicas
- ✅ Domínio de negócio (conteúdos educacionais)
- ✅ Roadmap de melhorias futuras

Este schema serve como:
- 📚 **Documentação técnica** completa da plataforma
- 🗺️ **Mapa de capacidades** atuais e futuras
- 🔗 **Base para integrações** com outros sistemas
- 📊 **Referência para desenvolvimento** de novas features
- 🎓 **Guia educacional** sobre a arquitetura

---

## Estrutura do Schema

O schema segue o padrão **JSON-LD** (JSON for Linking Data) e está organizado em:

```json
{
  "@context": { ... },  // Definição de vocabulários e prefixos
  "@graph": [ ... ]     // Grafo de entidades e relacionamentos
}
```

### @context

Define os vocabulários e prefixos utilizados:

| Prefixo | Namespace | Uso |
|---------|-----------|-----|
| `@vocab` | `https://schema.org/` | Vocabulário base (schema.org) |
| `bob` | `https://bob-learning-hub.com/schema#` | Vocabulário customizado da plataforma |
| `dc` | `http://purl.org/dc/terms/` | Dublin Core (metadados temporais) |
| `xsd` | `http://www.w3.org/2001/XMLSchema#` | Tipos de dados XML Schema |
| `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | RDF Schema (estrutura semântica) |
| `hydra` | `http://www.w3.org/ns/hydra/core#` | Hydra Core (APIs REST) |
| `api` | `https://bob-learning-hub.com/api#` | APIs da plataforma |

### @graph

Contém todas as entidades e seus relacionamentos:
- Plataforma (`bob:BobLearningHub`)
- Arquitetura (`bob:PlatformArchitecture`)
- Aplicações (`bob:FrontendApp`, `bob:BackendApp`)
- APIs (`bob:ContentAPI`)
- Endpoints (`bob:Endpoint/*`)
- Features (`bob:Feature/*`)
- Capacidades (`bob:Capability/*`)
- Domínio (`bob:LearningContent`, `bob:ContentType`, etc.)
- Roadmap (`bob:FutureEnhancements`)

---

## Vocabulários Utilizados

### Schema.org

Vocabulário base para tipos comuns:
- `CreativeWork` - Base para conteúdos educacionais
- `Person` - Base para instrutores e estudantes
- `AggregateRating` - Base para avaliações
- `Enumeration` - Base para enumerações

### Dublin Core (dc)

Metadados temporais:
- `dc:created` - Data de criação
- `dc:modified` - Data de modificação
- `dc:description` - Descrição detalhada

### Hydra Core

Documentação de APIs REST:
- `hydra:method` - Método HTTP
- `hydra:path` - Caminho do endpoint
- `hydra:operationId` - Identificador da operação
- `hydra:expects` - Parâmetros esperados
- `hydra:returns` - Tipo de retorno
- `hydra:statusCodes` - Códigos de status HTTP

### RDF/RDFS

Estrutura semântica:
- `rdfs:Class` - Define uma classe
- `rdfs:label` - Rótulo legível
- `rdfs:comment` - Comentário descritivo
- `rdfs:subClassOf` - Herança de classes
- `rdfs:domain` - Domínio de uma propriedade
- `rdfs:range` - Range de uma propriedade

---

## Plataforma

### bob:BobLearningHub

Entidade raiz que representa a plataforma completa.

**Propriedades:**

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `@id` | IRI | `bob:BobLearningHub` |
| `@type` | Class | `bob:Platform` |
| `name` | String | "Bob Learning Hub" |
| `description` | String | Descrição da plataforma |
| `version` | String | "1.0.0" |
| `url` | URL | https://bob-learning-hub.com |
| `dc:created` | DateTime | Data de criação |
| `dc:modified` | DateTime | Última modificação |

**Relacionamentos:**

| Propriedade | Aponta para | Descrição |
|-------------|-------------|-----------|
| `bob:hasApplication` | Array | Frontend e Backend apps |
| `bob:hasArchitecture` | IRI | Arquitetura da plataforma |
| `bob:hasFeature` | Array | Features implementadas |
| `bob:hasTechnicalCapability` | Array | Capacidades técnicas |
| `bob:supportedContentTypes` | Array | Tipos de conteúdo suportados |

---

## Arquitetura

### bob:PlatformArchitecture

Descreve a arquitetura da plataforma.

**Propriedades:**

| Propriedade | Valor |
|-------------|-------|
| `@type` | `bob:Architecture` |
| `name` | "Bob Learning Hub Architecture" |
| `architecturePattern` | "Frontend-Backend Separation with BFF Pattern" |
| `bob:hasFrontend` | `bob:FrontendApp` |
| `bob:hasBackend` | `bob:BackendApp` |
| `bob:communicationProtocol` | "REST over HTTPS" |
| `bob:dataFormat` | "JSON" |
| `bob:authenticationStrategy` | "Future: JWT/OAuth2" |
| `bob:deploymentStrategy` | "Cloud-native (AWS Elastic Beanstalk)" |

**Diagrama:**

```
┌─────────────────────┐
│   bob:FrontendApp   │
│   (Angular 17)      │
└──────────┬──────────┘
           │ REST/HTTPS
           │ JSON
           ▼
┌─────────────────────┐
│   bob:BackendApp    │
│   (Spring Boot 3)   │
└──────────┬──────────┘
           │
           ▼
    [Future: Database]
```

---

## Aplicações

### bob:FrontendApp (fed-bob-a-thon)

Interface do usuário da plataforma.

**Especificações Técnicas:**

| Propriedade | Valor |
|-------------|-------|
| `@type` | `bob:FrontendApplication` |
| `name` | "fed-bob-a-thon" |
| `version` | "0.0.0" |
| `framework` | "Angular" |
| `frameworkVersion` | "17.3.0" |
| `language` | "TypeScript" |
| `architecturePattern` | "Standalone Components" |
| `stateManagement` | "Angular Signals" |
| `buildTool` | "Angular CLI" |
| `packageManager` | "npm" |

**User Interfaces:**

- `bob:UI/CourseCatalog` - Catálogo de cursos
- `bob:UI/CategoryFilter` - Filtro de categorias
- `bob:UI/FeaturedSection` - Seção de destaque
- `bob:UI/CourseCard` - Card de curso
- `bob:UI/LoadingState` - Estado de carregamento
- `bob:UI/ErrorState` - Estado de erro

**Rotas:**

| Path | Component | Descrição |
|------|-----------|-----------|
| `/` | `AppComponent` | Página principal com catálogo |

**State Management (Signals):**

| Signal | Tipo | Descrição |
|--------|------|-----------|
| `courses` | `CourseItem[]` | Lista de cursos |
| `selectedCategory` | `string` | Categoria selecionada |
| `isLoading` | `boolean` | Estado de carregamento |
| `errorMessage` | `string` | Mensagem de erro |
| `featuredCourse` | `CourseItem \| null` | Curso em destaque (computed) |
| `categories` | `string[]` | Lista de categorias (computed) |
| `filteredCourses` | `CourseItem[]` | Cursos filtrados (computed) |

**Features Implementadas:**

1. Content Catalog
2. Category Filtering
3. Featured Content
4. Responsive UI
5. Error Handling
6. Loading States
7. Dynamic Categories
8. Fallback Data

**Capacidades Técnicas:**

- Reactive state with computed signals
- HTTP client integration
- Error handling with retry
- Responsive card-based layout
- Dynamic category generation
- Fallback data for missing API fields
- Track by optimization for lists

---

### bob:BackendApp (bff-bob-a-thon)

Backend for Frontend - API REST.

**Especificações Técnicas:**

| Propriedade | Valor |
|-------------|-------|
| `@type` | `bob:BackendService` |
| `name` | "bff-bob-a-thon" |
| `version` | "1.0.0" |
| `framework` | "Spring Boot" |
| `frameworkVersion` | "3.x" |
| `language` | "Java" |
| `languageVersion` | "17" |
| `architecturePattern` | "Clean Architecture / Hexagonal" |
| `buildTool` | "Maven" |
| `basePath` | "/api" |
| `port` | 8080 |

**Deployment:**

| Propriedade | Valor |
|-------------|-------|
| `platform` | AWS Elastic Beanstalk |
| `region` | us-east-1 |
| `url` | https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com |
| `healthCheckEndpoint` | /api/actuator/health |

**Camadas da Arquitetura:**

1. **Adapter Input**
   - Controllers REST
   - DTOs de entrada
   - Componentes: `ContentController`, `ContentDTO`, `CreateContentRequest`, `UpdateContentRequest`

2. **Adapter Output**
   - Repositórios
   - Integrações externas
   - Componentes: `ContentRepository` (in-memory)

3. **Domain**
   - Entidades de domínio
   - Lógica de negócio
   - Componentes: `Content`, `ContentType`, `ContentService`

4. **Config**
   - Configurações da aplicação
   - Componentes: `CorsConfig`, `OpenApiConfig`

**Features Implementadas:**

1. Content Management
2. CRUD Operations
3. Validation
4. Exception Handling
5. API Documentation
6. CORS Support
7. Health Check
8. Logging

**Capacidades Técnicas:**

- RESTful API design
- Bean Validation (Jakarta)
- Global exception handling
- OpenAPI/Swagger documentation
- CORS configuration
- Spring Boot Actuator
- Structured logging
- Clean Architecture separation
- In-memory data storage (future: database)

---

## API REST

### bob:ContentAPI

API REST para gerenciamento de conteúdos educacionais.

**Especificações:**

| Propriedade | Valor |
|-------------|-------|
| `@type` | `bob:APIService` |
| `name` | "Content Management API" |
| `basePath` | "/api/contents" |
| `version` | "1.0" |
| `documentation` | "/api/swagger-ui.html" |

### Endpoints

#### 1. GET /api/contents

**Listar todos os conteúdos**

```json
{
  "@id": "bob:Endpoint/GetAllContents",
  "hydra:method": "GET",
  "hydra:path": "/api/contents",
  "hydra:operationId": "getAllContents"
}
```

**Descrição:** Retorna todos os conteúdos educacionais disponíveis

**Retorno:** Array de `bob:LearningContent`

**Status Codes:**
- `200` - Lista retornada com sucesso

**Exemplo de Resposta:**
```json
[
  {
    "id": 1,
    "name": "Introdução ao Angular 17",
    "description": "Aprenda os fundamentos...",
    "imageUrl": "https://example.com/image.jpg"
  }
]
```

---

#### 2. GET /api/contents/{id}

**Buscar conteúdo por ID**

```json
{
  "@id": "bob:Endpoint/GetContentById",
  "hydra:method": "GET",
  "hydra:path": "/api/contents/{id}",
  "hydra:operationId": "getContentById"
}
```

**Descrição:** Retorna um conteúdo específico pelo seu identificador

**Parâmetros:**
- `id` (path, required) - Long - ID do conteúdo

**Retorno:** `bob:LearningContent`

**Status Codes:**
- `200` - Conteúdo encontrado
- `404` - Conteúdo não encontrado

**Exemplo de Resposta:**
```json
{
  "id": 1,
  "name": "Introdução ao Angular 17",
  "description": "Aprenda os fundamentos do Angular 17...",
  "imageUrl": "https://example.com/image.jpg"
}
```

---

#### 3. POST /api/contents

**Criar novo conteúdo**

```json
{
  "@id": "bob:Endpoint/CreateContent",
  "hydra:method": "POST",
  "hydra:path": "/api/contents",
  "hydra:operationId": "createContent"
}
```

**Descrição:** Cria um novo conteúdo educacional no sistema

**Body (required):**
```json
{
  "name": "string (max 200 chars, required)",
  "description": "string (max 1000 chars, required)",
  "imageUrl": "string (max 500 chars, required, must start with http:// or https://)"
}
```

**Retorno:** `bob:LearningContent` (com ID gerado)

**Status Codes:**
- `201` - Conteúdo criado com sucesso
- `400` - Dados inválidos

**Validações:**
- `name`: obrigatório, máximo 200 caracteres
- `description`: obrigatório, máximo 1000 caracteres
- `imageUrl`: obrigatório, máximo 500 caracteres, deve começar com http:// ou https://

---

#### 4. DELETE /api/contents/{id}

**Deletar conteúdo**

```json
{
  "@id": "bob:Endpoint/DeleteContent",
  "hydra:method": "DELETE",
  "hydra:path": "/api/contents/{id}",
  "hydra:operationId": "deleteContent"
}
```

**Descrição:** Remove um conteúdo do sistema

**Parâmetros:**
- `id` (path, required) - Long - ID do conteúdo

**Retorno:** Sem corpo (204 No Content)

**Status Codes:**
- `204` - Conteúdo deletado com sucesso
- `404` - Conteúdo não encontrado

---

## Features

### Features Implementadas

#### 1. bob:Feature/ContentCatalog

**Catálogo de Conteúdos**

- **Status:** Implemented
- **Implementado em:** Frontend
- **Usa API:** `GET /api/contents`
- **Descrição:** Exibição de todos os conteúdos educacionais em formato de cards responsivos

---

#### 2. bob:Feature/ContentManagement

**Gerenciamento de Conteúdos**

- **Status:** Implemented
- **Implementado em:** Backend
- **Provê API:** Content Management API
- **Descrição:** CRUD completo de conteúdos educacionais via API REST

---

#### 3. bob:Feature/CategoryFiltering

**Filtro por Categoria**

- **Status:** Implemented
- **Implementado em:** Frontend
- **Detalhes técnicos:** Uses Angular computed signals for reactive filtering without re-fetching data
- **Descrição:** Filtragem reativa de conteúdos por categoria usando computed signals

---

#### 4. bob:Feature/FeaturedContent

**Conteúdo em Destaque**

- **Status:** Implemented
- **Implementado em:** Frontend
- **Detalhes técnicos:** First course in the list is automatically featured
- **Descrição:** Seção especial para destacar um conteúdo principal

---

#### 5. bob:Feature/ResponsiveUI

**Interface Responsiva**

- **Status:** Implemented
- **Implementado em:** Frontend
- **Detalhes técnicos:** CSS Grid with responsive breakpoints
- **Descrição:** Layout adaptável para mobile, tablet e desktop

---

#### 6. bob:Feature/ErrorHandling

**Tratamento de Erros**

- **Status:** Implemented
- **Implementado em:** Frontend e Backend
- **Detalhes técnicos:** Frontend: RxJS error handling with retry. Backend: Global exception handler
- **Descrição:** Tratamento global de erros com mensagens amigáveis e retry

---

#### 7. bob:Feature/LoadingStates

**Estados de Carregamento**

- **Status:** Implemented
- **Implementado em:** Frontend
- **Detalhes técnicos:** Signal-based loading state management
- **Descrição:** Indicadores visuais durante operações assíncronas

---

## Capacidades Técnicas

### 1. bob:Capability/RESTAPI

**REST API**

- **Implementado em:** Backend
- **Descrição:** API RESTful seguindo padrões HTTP
- **Standards:** REST, HTTP/1.1, JSON

---

### 2. bob:Capability/CRUD

**CRUD Operations**

- **Implementado em:** Backend
- **Descrição:** Operações completas de Create, Read, Update, Delete
- **Operações implementadas:** Create, Read, Delete
- **Operações futuras:** Update

---

### 3. bob:Capability/ReactiveState

**Reactive State Management**

- **Implementado em:** Frontend
- **Descrição:** Gerenciamento de estado reativo com Angular Signals
- **Tecnologia:** Angular Signals
- **Benefícios:**
  - Automatic UI updates
  - Computed values
  - No external dependencies

---

### 4. bob:Capability/CORS

**CORS Support**

- **Implementado em:** Backend
- **Descrição:** Cross-Origin Resource Sharing configurado para permitir requisições do frontend
- **Allowed Origins:** `*` (todos)
- **Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

---

### 5. bob:Capability/OpenAPI

**OpenAPI Documentation**

- **Implementado em:** Backend
- **Descrição:** Documentação interativa da API com Swagger UI
- **URL:** `/api/swagger-ui.html`
- **Specification:** OpenAPI 3.0

---

### 6. bob:Capability/HealthCheck

**Health Check**

- **Implementado em:** Backend
- **Descrição:** Endpoint de health check para monitoramento
- **URL:** `/api/actuator/health`
- **Tecnologia:** Spring Boot Actuator

---

### 7. bob:Capability/CloudDeployment

**Cloud Deployment**

- **Implementado em:** Backend
- **Descrição:** Deployment em cloud com AWS Elastic Beanstalk
- **Platform:** AWS Elastic Beanstalk
- **Region:** us-east-1

---

## Domínio de Conteúdo

### bob:LearningContent

**Entidade principal** que representa um conteúdo educacional.

**Propriedades:**

| Propriedade | Tipo | Descrição | Validação |
|-------------|------|-----------|-----------|
| `contentId` | Long | Identificador único | - |
| `contentName` | String | Nome/título do conteúdo | Max 200 chars, obrigatório |
| `contentDescription` | String | Descrição detalhada | Max 1000 chars, obrigatório |
| `contentImageUrl` | URI | URL da imagem | Max 500 chars, obrigatório, http(s):// |
| `contentType` | ContentType | Tipo do conteúdo | Enum |
| `category` | Category | Categoria temática | - |
| `instructor` | Instructor | Instrutor/autor | - |
| `duration` | String | Duração estimada | Ex: "2h", "4h30m" |
| `level` | String | Nível de dificuldade | Ex: "Iniciante", "Avançado" |
| `rating` | Decimal | Avaliação média | 0-5 |
| `enrolledStudents` | Integer | Número de estudantes | - |
| `featured` | Boolean | Está em destaque? | - |

**Relacionamentos:**

- `contentType` → `bob:ContentType`
- `category` → `bob:Category`
- `instructor` → `bob:Instructor`
- `hasEnrollment` → `bob:Enrollment[]`

---

### bob:ContentType

**Enumeração** dos tipos de conteúdo suportados.

**Valores:**

| Valor | Label | Descrição |
|-------|-------|-----------|
| `VIDEO` | Video | Conteúdo em formato de vídeo |
| `ARTICLE` | Article | Conteúdo em formato de artigo/texto |
| `TUTORIAL` | Tutorial | Conteúdo em formato de tutorial passo a passo |
| `DOCUMENTATION` | Documentation | Conteúdo em formato de documentação técnica |
| `COURSE` | Course | Conteúdo em formato de curso completo |
| `PODCAST` | Podcast | Conteúdo em formato de podcast/áudio |

---

### Outras Entidades do Domínio

#### bob:Category
- Categoria temática de um conteúdo
- Exemplos: Desenvolvimento, Design, Negócios, Cloud, DevOps

#### bob:Instructor
- Instrutor ou autor de um conteúdo
- Propriedades: nome, bio, email

#### bob:Student
- Estudante que consome conteúdos
- Relacionamento com Enrollment

#### bob:Enrollment
- Matrícula de um estudante em um conteúdo
- Propriedades: data de matrícula, data de conclusão, progresso

#### bob:Rating
- Avaliação de um conteúdo por estudantes
- Propriedades: nota, comentário

---

## Roadmap de Melhorias

### bob:FutureEnhancements

Lista de melhorias planejadas para a plataforma.

#### Prioridade Alta

##### 1. Database Integration
- **Descrição:** Substituir in-memory storage por banco de dados (PostgreSQL/MongoDB)
- **Afeta:** Backend
- **Impacto:** Persistência real de dados

##### 2. User Authentication
- **Descrição:** Implementar autenticação JWT/OAuth2
- **Afeta:** Frontend e Backend
- **Impacto:** Segurança e controle de acesso

---

#### Prioridade Média

##### 3. User Enrollment
- **Descrição:** Sistema de matrícula de estudantes em cursos
- **Afeta:** Frontend e Backend
- **Requer entidades:** Enrollment, Student
- **Impacto:** Funcionalidade core da plataforma

##### 4. Content Rating
- **Descrição:** Sistema de avaliação de conteúdos por estudantes
- **Afeta:** Frontend e Backend
- **Requer entidades:** Rating
- **Impacto:** Feedback e qualidade

##### 5. Search Functionality
- **Descrição:** Busca textual de conteúdos
- **Afeta:** Frontend e Backend
- **Impacto:** Usabilidade

---

#### Prioridade Baixa

##### 6. Content Update
- **Descrição:** Endpoint PUT para atualização de conteúdos
- **Afeta:** Backend
- **Impacto:** Completar CRUD

##### 7. Pagination
- **Descrição:** Paginação de resultados na listagem de conteúdos
- **Afeta:** Frontend e Backend
- **Impacto:** Performance com grandes volumes

##### 8. Content Progress Tracking
- **Descrição:** Rastreamento de progresso do estudante em cada conteúdo
- **Afeta:** Frontend e Backend
- **Impacto:** Engajamento

##### 9. Multi-language Support
- **Descrição:** Internacionalização (i18n) da interface
- **Afeta:** Frontend
- **Impacto:** Alcance global

##### 10. Analytics Dashboard
- **Descrição:** Dashboard com métricas de uso da plataforma
- **Afeta:** Frontend e Backend
- **Impacto:** Insights e tomada de decisão

---

## Como Usar Este Schema

### 1. Documentação Técnica

Use o schema como referência completa da plataforma:

```bash
# Consultar estrutura da plataforma
cat bob-learning-hub-schema.jsonld | jq '.["@graph"][] | select(.["@id"] == "bob:BobLearningHub")'

# Listar todas as features
cat bob-learning-hub-schema.jsonld | jq '.["@graph"][] | select(.["@type"] == "bob:Feature")'

# Listar endpoints da API
cat bob-learning-hub-schema.jsonld | jq '.["@graph"][] | select(.["@type"] == "bob:APIEndpoint")'
```

### 2. Desenvolvimento de Novas Features

Ao desenvolver uma nova feature:

1. Adicione uma entrada em `bob:Feature/*`
2. Documente status, componentes afetados e APIs utilizadas
3. Atualize `bob:FutureEnhancements` se aplicável
4. Adicione capacidades técnicas em `bob:Capability/*` se necessário

### 3. Integração com Outros Sistemas

O schema pode ser usado para:
- Gerar documentação automática
- Criar clientes de API
- Integrar com sistemas de descoberta de serviços
- Alimentar ferramentas de monitoramento

### 4. Validação de Arquitetura

Use o schema para validar que:
- Todas as features estão documentadas
- Todos os endpoints estão mapeados
- Relacionamentos entre componentes estão claros
- Roadmap está atualizado

### 5. Onboarding de Desenvolvedores

Novos desenvolvedores podem usar o schema para:
- Entender a arquitetura completa
- Identificar componentes e responsabilidades
- Conhecer as APIs disponíveis
- Ver o roadmap de evolução

---

## Manutenção do Schema

### Quando Atualizar

Atualize o schema quando:
- ✅ Nova feature for implementada
- ✅ Novo endpoint for criado
- ✅ Arquitetura for modificada
- ✅ Nova capacidade técnica for adicionada
- ✅ Roadmap for revisado

### Como Atualizar

1. Edite o arquivo `bob-learning-hub-schema.jsonld`
2. Adicione/modifique entidades no `@graph`
3. Atualize relacionamentos se necessário
4. Valide o JSON-LD (use ferramentas como JSON-LD Playground)
5. Atualize este documento de documentação
6. Commit com mensagem descritiva

### Versionamento

O schema segue versionamento semântico:
- **Major** (1.x.x): Mudanças incompatíveis na estrutura
- **Minor** (x.1.x): Novas features/entidades
- **Patch** (x.x.1): Correções e melhorias na documentação

---

## Recursos Adicionais

### Ferramentas

- **JSON-LD Playground**: https://json-ld.org/playground/
- **Schema.org**: https://schema.org/
- **Hydra Core**: https://www.hydra-cg.com/
- **Dublin Core**: https://www.dublincore.org/

### Referências

- [JSON-LD Specification](https://www.w3.org/TR/json-ld11/)
- [Schema.org Documentation](https://schema.org/docs/documents.html)
- [Hydra Core Vocabulary](https://www.hydra-cg.com/spec/latest/core/)
- [RDF Schema](https://www.w3.org/TR/rdf-schema/)

---

**Última atualização**: 2026-05-21  
**Versão do schema**: 1.0.0  
**Mantenedores**: Equipe Bob-a-thon