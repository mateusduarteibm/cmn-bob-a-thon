# Inventário — BFF (`bff-*`)



## 🔄 Atualização Automática - 2026-05-21

**PR #3**: Added new endpoints so that users can favorite their courses

**Mudanças**: Added new endpoints so that users can favorite their courses

**Endpoints Afetados**:
- `/user/{userId}/content/{contentId}`
- `/{id}`
- `/user/{userId}/count`
- `/user/{userId}`

**Motivo**: Mudanças em controllers detectadas; Mudanças em DTOs/modelos detectadas; Mudanças em configuração OpenAPI; Mudanças em lógica de negócio

---

> Preenchido progressivamente com o prompt `PROMPT-INVENTARIO.md`.
> Ver índice geral: `INVENTARIO-REPOSITORIOS.md`
>
> **Última atualização**: 2026-05-20
> **Status**: ✅ Completo (todos os `bff-*` analisados)

---

## Legenda de Status

| Símbolo | Significado |
|---------|-------------|
| ✅ | Inventariado e completo |
| ⚠️ | Inventariado parcialmente (algum arquivo não encontrado) |
| 🔍 | Pendente de análise |
| ⛔ | Template vazio — sem configuração real |

---

## BFF (`bff-*`)

---

### `bff-bob-a-thon`

- **Type**: BFF
- **Status**: ✅
- **Scenarios**: —
- **Infrastructure**: —
- **Base path**: `/api`
- **Exposed endpoints**:
  | Method | Path | OperationId | Summary |
  |--------|------|-------------|---------|
  | GET | /api/contents | getAllContents | Listar conteúdos |
  | GET | /api/contents/{id} | getContentById | Buscar conteúdo por ID |
  | POST | /api/contents | createContent | Criar novo conteúdo |
  | DELETE | /api/contents/{id} | deleteContent | Deletar conteúdo |
- **Feign Clients (consumes)**:
  | Interface | URL (env var) | Called endpoints |
  |-----------|--------------|------------------|
  | None | — | — |
- **Kafka Topics**:
  None
- **Critical environment variables**:
  | Variable | Description |
  |----------|-------------|
  | SERVER_PORT | Porta HTTP da aplicação (default 8080) |

---
