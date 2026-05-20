---
description: >
  Analyzes a batch of Bob-a-thon Learning Platform repositories and populates or updates
  the corresponding inventory files. Works for both new repositories (first analysis)
  and previously inventoried repositories that have been modified.
---

# Prompt: Repository Inventory Analysis

## Context

This is an educational project for learning microservices architecture patterns. The Bob-a-thon Learning Platform follows a standard architectural pattern:

- `bob-fed-*` → Frontend Angular applications
- `bob-bff-*` → Backend for Frontend: orchestrates calls to services via REST clients
- `bob-srv-*` → Backend services: business logic, external integrations, messaging, databases

**Target inventory files** (one per repository type):
- `bob-bff-*` → `documentation/inventario/INVENTARIO-BFF.md`
- `bob-fed-*` → `documentation/inventario/INVENTARIO-FED.md`

---

## Integration Scenarios Reference

Use the table below to populate the **Scenarios** field for each repository. Detect each scenario based on `pom.xml` dependencies, `application.yml` configurations, and source code.

| Scenario | Name | How to detect |
|---------|------|---------------|
| **A** | PostgreSQL Database | Dependencies `spring-boot-starter-data-jpa` + `postgresql` (or `h2` for dev) in `pom.xml`; `spring.datasource` in `application.yml` |
| **B** | MongoDB Database | Dependency `spring-boot-starter-data-mongodb` in `pom.xml`; `spring.data.mongodb` in `application.yml` |
| **C** | Redis Cache | Dependency `spring-boot-starter-data-redis` in `pom.xml`; `spring.data.redis` in `application.yml` |
| **D** | REST API Consumption (FeignClient) | Has `@FeignClient` in code or dependency `spring-cloud-starter-openfeign` in `pom.xml` |
| **E** | Kafka Messaging | Dependency `spring-kafka` in `pom.xml`; topics in `kafka.producer.*`, `kafka.consumer.*` or `spring.kafka.*` in `application.yml` |
| **F** | File Storage (Cloud Storage) | Dependencies like `azure-storage-blob`, `spring-cloud-azure-starter-storage-blob`, or similar cloud storage SDKs in `pom.xml` |

> If the repository is just a **template** (no real implementation — generic artifactId, example endpoints like `Book`), record the scenario as `Template` and don't apply the others.
>
> **Template detection:** A repository is a template **only** if the `groupId` is `com.example.template` AND the `artifactId` is `java-maven-template`. Repositories with their own `groupId` (e.g., `com.bobathon.learning`) are **never** templates, even if they don't use any scenarios A–F — in that case, record scenarios as `—` and document exposed endpoints normally.

---

## Repositories to Analyze in This Batch

> Analyze **all** listed repositories — don't skip any.

```
REPOSITORIES:
- bob-srv-example-service
- bob-bff-example-api
```

Repositories are located in: `repositories/` (workspace root folder).

---

## Analysis Instructions

For **each repository** in the list above, follow the appropriate guide based on repository type.
**Read all indicated files for each type. If a file doesn't exist, record as "not found".**

---

### Type: `bob-bff-*` (Backend for Frontend)

Read the following files **mandatory**:

1. **BFF OpenAPI file** — search in this order:
   - `src/main/resources/openapi/api-specification.yaml`
   - `src/main/resources/api-specification.yaml`
   - `src/main/resources/openapi/api-specification.json`
   
   Extract: for each path/method → `operationId`, HTTP method, full path, `summary`

2. **`src/main/resources/application.yml`** — extract:
   - `openapi.[*].base-path` → BFF path prefix
   - Configured URLs (e.g., `feign.client.config.[*].url`)
   - Kafka topics produced/consumed (look for `kafka.producer.*`, `kafka.consumer.*`, `topic.*`)

3. **All files `src/main/java/**/client/*.java`** (or `src/main/java/**/adapter/output/feign/*.java`) — for each `@FeignClient` found, extract:
   - Interface name (class)
   - Value of `url` or `name` from `@FeignClient` annotation
   - List of methods with `@GetMapping`/`@PostMapping`/etc. → HTTP method and path

4. **`pom.xml`** — extract:
   - `<artifactId>` and `<groupId>` (to detect if it's a generic template)
   - Infrastructure dependencies: `spring-boot-starter-data-jpa`, `postgresql`, `h2`, `spring-boot-starter-data-mongodb`, `spring-boot-starter-data-redis`, `spring-kafka`, `azure-storage-blob`, `spring-cloud-azure-starter-storage-blob`
   - Use these dependencies to populate **Infrastructure** and **Scenarios**

**Output format for `bob-bff-*`:**

```markdown
---

### `[REPO-NAME]`

- **Type**: BFF
- **Status**: ✅
- **Scenarios**: [A, B, C, D, E, F | Template | —]
- **Infrastructure**: [PostgreSQL · Redis · MongoDB · Kafka · Cloud Storage · —]
- **Base path**: `[base-path from openapi or "/v1"]`
- **Exposed endpoints**:
  | Method | Path | OperationId | Summary |
  |--------|------|-------------|---------|
  | [POST] | [/v1/...] | [operationId] | [summary] |
- **Feign Clients (consumes)**:
  | Interface | URL (env var) | Called endpoints |
  |-----------|--------------|------------------|
  | [ClientName] | `[ENV_VAR_URL]` | [METHOD /path/to/service, ...] |
- **Kafka Topics**:
  | Direction | Topic (env var) |
  |-----------|-----------------|
  | Produces | `[KAFKA_TOPIC_VAR]` |
  | Consumes | `[KAFKA_TOPIC_VAR]` |
  > [or "None" if not using Kafka]
- **Critical environment variables**:
  | Variable | Description |
  |----------|-------------|
  | `[SERVICE_URL]` | URL to downstream service |
```

---

### Type: `bob-srv-*` (Backend Service)

Read the following files **mandatory**:

1. **Service OpenAPI file** — search in this order:
   - `src/main/resources/openapi/api-specification.yaml`
   - `src/main/resources/api-specification.yaml`
   
   Extract: for each path/method → `operationId`, HTTP method, full path, `summary`

2. **`src/main/resources/application.yml`** — extract:
   - `server.port` or default value
   - Configured external client URLs
   - Kafka topics (`kafka.producer.*`, `kafka.consumer.*`, `topic.*`, `spring.kafka.*`)
   - Configured datasource / Redis / MongoDB (type only, not credentials)

3. **All files `src/main/java/**/client/*.java`** — for each `@FeignClient`:
   - Interface name, `url` or `name` from annotation
   - HTTP methods and paths

4. **`pom.xml`** — extract:
   - `<artifactId>` and `<groupId>` (to detect if it's a generic template)
   - Infrastructure dependencies: `spring-boot-starter-data-jpa`, `postgresql`, `h2`, `spring-boot-starter-data-mongodb`, `spring-boot-starter-data-redis`, `spring-kafka`, `azure-storage-blob`, `spring-cloud-azure-starter-storage-blob`
   - Use these dependencies together with `application.yml` and code to populate **Infrastructure** and **Scenarios**

**Output format for `bob-srv-*`:**

```markdown
---

### `[REPO-NAME]`

- **Type**: SRV
- **Status**: ✅
- **ArtifactId**: `[com.bobathon.learning.srv:name]`
- **Scenarios**: [A, B, C, D, E, F | Template | —]
- **Infrastructure**: [PostgreSQL · MongoDB · Redis · Kafka · Cloud Storage · —]
- **Exposed endpoints**:
  | Method | Path | OperationId | Summary |
  |--------|------|-------------|---------|
  | [POST] | [/api/v1/...] | [operationId] | [summary] |
- **Feign Clients (consumes)**:
  | Interface | URL (env var) | Called endpoints |
  |-----------|--------------|------------------|
  | [ClientName] | `[ENV_VAR_URL]` | [METHOD /path, ...] |
- **Kafka Topics**:
  | Direction | Topic (env var) |
  |-----------|-----------------|
  | Produces | `[KAFKA_TOPIC_VAR]` |
  | Consumes | `[KAFKA_TOPIC_VAR]` |
  > [or "None" if not using Kafka]
- **Critical environment variables**:
  | Variable | Description |
  |----------|-------------|
  | `[EXTERNAL_API_URL]` | URL to external API |
```

---

### Type: `bob-fed-*` (Frontend Angular)

Read the following files **mandatory**:

1. **All `*.service.ts` files in the entire `src/` tree** — execute **two** complementary searches to ensure full coverage:

   **Search 1 — direct HttpClient injection** (covers services that import and inject `HttpClient` in the class itself):
   ```powershell
   Get-ChildItem -Path "...\src" -Recurse -Filter "*.ts" |
     Where-Object { $_.Name -notlike "*.spec.ts" -and $_.Name -notlike "*.test.ts" } |
     Select-String -Pattern "HttpClient" -List |
     Select-Object -ExpandProperty Path
   ```

   **Search 2 — HTTP base class inheritance** (covers services that use inherited `this.http` from `BaseHttpService` or similar, without directly importing `HttpClient`):
   ```powershell
   Get-ChildItem -Path "...\src" -Recurse -Filter "*.service.ts" |
     Where-Object { $_.Name -notlike "*.spec.ts" -and $_.Name -notlike "*.test.ts" } |
     Select-String -Pattern "extends\s+\w*Http\w*Service|baseUrl|#baseUrl" -List |
     Select-Object -ExpandProperty Path
   ```

   > ⚠️ **Common pitfall**: Services that `extends BaseHttpService` **won't appear in the `HttpClient` grep** because they inherit `this.http` from the parent class. Search 2 is mandatory to capture them.

   For each file found in both searches (excluding duplicates and `BaseHttpService` itself), read the file and extract:
   - Service name
   - Base URL used (e.g., `this.#appConfig?.apiUrl + "/api/..."`, or via `buildBaseUrl(this.basePath, ...)`)
   - Called HTTP methods (GET, POST, PUT, DELETE, PATCH) and full paths

2. **`src/environments/environment.ts`** and `environment.development.ts` (if they exist) — or **`config/`** — extract configured URL keys (e.g., `apiUrl`, `apiGateway`)

3. **`package.json`** — extract `name` and `version`

4. **`proxy.conf.json`** (if exists) — extract proxy rules (path → target)

**Output format for `bob-fed-*`:**

```markdown
---

### `[REPO-NAME]`

- **Type**: FED
- **Status**: ✅
- **Package name**: `[name from package.json]`
- **Used URL keys** (from APP_CONFIG/environments):
  `[apiUrl]`, `[other key]`
- **Consumed APIs**:
  | Angular Service | Base URL (env key + path) | Called endpoints |
  |-----------------|--------------------------|------------------|
  | `[ServiceName]` | `apiUrl + "/api/[path]"` | [POST /v1/..., GET /v1/...] |
```

---

## Final Instructions

After analyzing **all** repositories in the list:

1. For each generated entry, determine the target file by repository type:
   - Repos `bob-bff-*` → **`INVENTARIO-BFF.md`**, in section `## BFF`
   - Repos `bob-fed-*` → **`INVENTARIO-FED.md`**, in section `## FED`

   If the batch mixes different types, write entries to the corresponding files for each type.

   **For each entry, check if the repository is already inventoried:**
   - **If exists** a section `### \`[repo-name]\`` in the file: **replace** the complete existing block (from previous `---` separator to next `---` separator, inclusive) with the newly generated entry.
   - **If doesn't exist**: **add** the new entry at the end of the file.

2. Update the `**Last updated**` field in the header of modified file(s) with today's date.

3. If any repository **doesn't exist** in the `repositories/` folder, record as:
   `| [name] | — | ⚠️ | Repository not found in workspace |`

---

## Educational Notes

This inventory system helps you:
- **Understand architecture patterns**: See how BFFs orchestrate services, how services handle data persistence
- **Learn integration patterns**: Identify common scenarios (databases, caching, messaging, REST APIs)
- **Practice documentation**: Create clear, structured technical documentation
- **Explore microservices**: Understand service boundaries and communication patterns

When analyzing repositories, focus on:
- **Separation of concerns**: How each layer (FED, BFF, SRV) has distinct responsibilities
- **Configuration management**: How environment-specific settings are handled
- **API contracts**: How OpenAPI specifications define service interfaces
- **Integration patterns**: How services communicate (REST, messaging, databases)
