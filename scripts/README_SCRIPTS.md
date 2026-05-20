# Scripts — Bob-a-thon Learning Platform

This directory contains utility scripts for maintaining and operating the Bob-a-thon Learning Platform documentation.

## 📋 Available Scripts

### 🗺️ Repository Map Generation

#### `generate_mapa_endpoints.py`
Generates a repository map for the Bob-a-thon Learning Platform by parsing inventory files and creating relationship diagrams between frontend (FED) and backend (BFF) repositories.

**Usage:**
```bash
python scripts/generate_mapa_endpoints.py
```

**Optional dependency for HTML generation:**
```bash
pip install markdown
```

**Inputs (automatically read from `documentation/inventario/`):**
- `INVENTARIO-BFF.md` — Backend for Frontend repositories
- `INVENTARIO-FED.md` — Frontend repositories

**Outputs (written to `documentation/mapa/`):**

| File | Description |
|------|-------------|
| `MAPA-REPOSITORIOS.md` | Complete repository map with relationships |
| `MAPA-REPOSITORIOS-LISTAS.md` | Simplified list format |
| `MAPA-REPOSITORIOS.html` | Visual HTML map (requires `pip install markdown`) |

**Features:**
- 📊 Parses BFF and FED inventories
- 🔗 Maps FED → BFF relationships
- 📝 Generates markdown documentation
- 🌐 Creates interactive HTML visualization
- 🎨 Bob-a-thon branded styling

**Process:**
```
1. Read Inventory Files
   └─> INVENTARIO-BFF.md: Backend repositories
   └─> INVENTARIO-FED.md: Frontend repositories

2. Parse Repository Information
   └─> Extract endpoints from BFF
   └─> Extract API calls from FED
   └─> Identify FED → BFF connections

3. Generate Repository Map (MAPA-REPOSITORIOS.md)
   └─> Summary statistics
   └─> BFF repositories with endpoints
   └─> FED repositories with dependencies
   └─> Architecture diagram

4. Generate Repository List (MAPA-REPOSITORIOS-LISTAS.md)
   └─> Simplified list of all repositories
   └─> Grouped by type (BFF, FED)

5. Generate HTML Visualization (MAPA-REPOSITORIOS.html)
   └─> Converts markdown to HTML
   └─> Applies Bob-a-thon styling
   └─> Self-contained (no external dependencies)
```

**Example Output:**
```
🚀 Bob-a-thon Repository Map Generator
============================================================

📖 Reading inventory files...
🔍 Parsing BFF repositories...
   Found 1 BFF repositories
🔍 Parsing FED repositories...
   Found 1 FED repositories

📝 Generating repository map...
📝 Generating repository list...
📝 Generating HTML visualization...

💾 Writing output files...
   ✅ documentation/mapa/MAPA-REPOSITORIOS.md
   ✅ documentation/mapa/MAPA-REPOSITORIOS-LISTAS.md
   ✅ documentation/mapa/MAPA-REPOSITORIOS.html

✨ Done! Repository map generated successfully.
```

**Architecture Diagram Example:**
```
FED (Frontend)          BFF (Backend for Frontend)
─────────────────       ───────────────────────────

fed-bob-a-thon
  └─→ bff-bob-a-thon
```

**Notes:**
- 🎯 **Simple architecture**: Only 2 repository types (BFF, FED)
- 🔗 **Clear relationships**: Shows which FEDs consume which BFFs
- 📊 **Multiple formats**: Markdown, list, and HTML for different use cases
- 🌐 **HTML is optional**: Script works without the `markdown` package (falls back to `<pre>` tags)
- 🎨 **Bob-a-thon branding**: Custom styling in HTML output

---

## 📚 Documentation Structure

The scripts work with the following documentation structure:

```
documentation/
├── inventario/
│   ├── INVENTARIO-BFF.md          ← Input: BFF repositories
│   ├── INVENTARIO-FED.md          ← Input: FED repositories
│   └── INVENTARIO-REPOSITORIOS.md ← Index of all inventories
├── mapa/
│   ├── MAPA-REPOSITORIOS.md       ← Output: Complete map
│   ├── MAPA-REPOSITORIOS-LISTAS.md ← Output: List format
│   └── MAPA-REPOSITORIOS.html     ← Output: HTML visualization
└── prompts/
    └── PROMPT-INVENTARIO.md       ← Prompt for creating inventories
```

---

## 🚀 Quick Start

To generate the repository map:

```bash
# 1. Ensure inventory files are up to date
# (Edit INVENTARIO-BFF.md and INVENTARIO-FED.md as needed)

# 2. Run the map generator
python scripts/generate_mapa_endpoints.py

# 3. View the outputs
# - Markdown: documentation/mapa/MAPA-REPOSITORIOS.md
# - List: documentation/mapa/MAPA-REPOSITORIOS-LISTAS.md
# - HTML: documentation/mapa/MAPA-REPOSITORIOS.html (open in browser)
```

---

## 🛠️ Development

### Adding New Repository Types

To add support for new repository types (e.g., SRV, API):

1. Create a new inventory file: `INVENTARIO-{TYPE}.md`
2. Add a parser function in `generate_mapa_endpoints.py`: `parse_{type}s()`
3. Update the `generate_mapa()` function to include the new type
4. Update the architecture diagram generation

### Modifying Output Format

The output format is controlled by:
- `generate_mapa()`: Main markdown format
- `generate_lista_repos()`: List format
- `_HTML_TEMPLATE`: HTML styling and structure

---

## 📝 License

This is part of the Bob-a-thon Learning Platform, a public educational repository.
