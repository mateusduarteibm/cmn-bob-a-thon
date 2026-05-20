# Inventário — BFF (`bff-*`)

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
