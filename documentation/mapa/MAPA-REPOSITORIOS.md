# Mapa de Endpoints — Bob-a-thon Learning Platform

> **Gerado automaticamente** a partir dos inventários em `documentation/inventario/`
> **Data de geração**: 2026-05-20

---

## Índice

| # | Seção | Descrição |
|---|-------|-----------|
| 1 | [FED → BFF (Chamadas HTTP)](#1-fed--bff-chamadas-http) | Mapeamento de chamadas do frontend para o backend |
| 2 | [Cadeia Completa por BFF](#2-cadeia-completa-por-bff) | Visão consolidada end-to-end de cada BFF |

---

## 1. FED → BFF (Chamadas HTTP)

> Mapeamento de chamadas HTTP dos frontends para os backends

| FED | URL Base | BFF de Destino | Endpoints Chamados |
|-----|----------|----------------|-------------------|
| `fed-bob-a-thon` | `https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com` | `bff-bob-a-thon` | `GET /api/contents` |

---

## 2. Cadeia Completa por BFF

> Visão consolidada end-to-end de cada BFF, mostrando FEDs consumidores e endpoints expostos

### `bff-bob-a-thon`

**FED consumidor:**
- `fed-bob-a-thon`

**Endpoints expostos:**
- GET /api/contents
- GET /api/contents/{id}
- POST /api/contents
- DELETE /api/contents/{id}

**Descrição:**
Backend for Frontend da plataforma Bob-a-thon Learning Platform. Gerencia operações CRUD de conteúdos educacionais (cursos, tutoriais, etc.).

---
