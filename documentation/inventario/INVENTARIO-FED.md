# Inventário — FED (`fed-*`)

> Preenchido progressivamente com o prompt `PROMPT-INVENTARIO.md`.
> Ver índice geral: `INVENTARIO-REPOSITORIOS.md`
>
> **Última atualização**: 2026-05-20
> **Status**: ✅ Completo (todos os `fed-*` analisados + Bob-a-thon Learning Platform)

---

## Legenda de Status

| Símbolo | Significado |
|---------|-------------|
| ✅ | Inventariado e completo |
| ⚠️ | Inventariado parcialmente (algum arquivo não encontrado) |
| 🔍 | Pendente de análise |

---

## FED (`fed-*`)

---

### `fed-bob-a-thon`

- **Type**: FED
- **Status**: ✅
- **Package name**: `fed-bob-a-thon-app` · version `0.0.0`
- **Angular version**: 17.3.0
- **Architecture**: Standalone Components (no NgModules)
- **Description**: Frontend application for the Bob-a-thon Learning Platform. Displays a catalog of educational courses with filtering by category. Uses Angular Signals for reactive state management.
- **Routes**: 
  - `/` (root) — Main course catalog page (no lazy-loaded routes configured)
- **Used URL keys** (hardcoded in component):
  - BFF base URL: `https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com`
- **Consumed APIs**:
  | Component/Service | Base URL | Called endpoints |
  |-------------------|----------|------------------|
  | `AppComponent` (direct HttpClient) | `https://bff-bob-a-thon-env.eba-kipvpqnj.us-east-1.elasticbeanstalk.com` | `GET /api/contents` |
- **Key Features**:
  - Course catalog display with dynamic categories
  - Featured course highlight
  - Category-based filtering (reactive with computed signals)
  - Error handling with retry mechanism
  - Loading states
  - Responsive card-based layout
- **State Management**: Angular Signals (no NgRx or external state library)
- **HTTP Client**: Direct `HttpClient` injection in `AppComponent` (no dedicated service layer)
- **Design System**: Custom SCSS styling (no external UI framework detected)
- **Environment Configuration**: No environment files — API URL is hardcoded in component
- **Proxy Configuration**: None (no `proxy.conf.json`)
- **Notes**: 
  - Simple single-component application (no feature modules or lazy loading)
  - API response mapping handles multiple field name variations (`title`/`name`, `description`/`summary`, etc.)
  - Fallback data generation for missing API fields (categories, authors, durations, images, ratings)
  - Uses modern Angular 17 features: standalone components, signals, computed values, inject() function

---
