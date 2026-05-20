# 📚 Bob-a-thon Documentation Hub

> **Central repository for documentation generation tools and AI context management**

This repository contains prompts, scripts, and documentation tools to help developers generate comprehensive technical contexts for AI-assisted development. It's designed to maintain consistent, up-to-date documentation across multiple projects.

---

## 🎯 Purpose

This repository serves as a **documentation toolkit** that:

- 📝 Provides standardized prompts for generating technical documentation
- 🤖 Creates AI-ready context files for development assistance
- 🗺️ Generates repository maps and relationship diagrams
- 📊 Maintains inventories of project components
- 🔄 Automates documentation updates

**Use Case**: When starting a new development task or onboarding to a project, use these tools to generate comprehensive context files that can be provided to AI assistants (like GitHub Copilot, ChatGPT, Claude, etc.) for more accurate code generation and suggestions.

---

## 📋 Table of Contents

- [Repository Structure](#-repository-structure)
- [Documentation Types](#-documentation-types)
- [Prompts](#-prompts)
- [Scripts](#-scripts)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)

---

## 📁 Repository Structure

```
cmn-bob-a-thon/
├── documentation/
│   ├── inventario/          # Component inventories
│   │   ├── INVENTARIO-BFF.md
│   │   ├── INVENTARIO-FED.md
│   │   └── INVENTARIO-REPOSITORIOS.md
│   ├── mapa/                # Relationship maps
│   │   ├── MAPA-REPOSITORIOS.md
│   │   ├── MAPA-REPOSITORIOS-LISTAS.md
│   │   └── MAPA-REPOSITORIOS.html
│   ├── contextos/           # Complete technical contexts
│   │   └── CONTEXTO-BOB-LEARNING-HUB.md
│   └── prompts/             # Documentation generation prompts
│       ├── PROMPT-INVENTARIO.md
│       └── PROMPT-GERAR-CONTEXTO.md
├── scripts/
│   ├── generate_mapa_endpoints.py
│   └── README_SCRIPTS.md
└── README.md
```

---

## 📖 Documentation Types

### 1. 📦 Inventories (`documentation/inventario/`)

**Purpose**: Detailed technical inventories of project components.

| File | Description |
|------|-------------|
| `INVENTARIO-BFF.md` | Backend for Frontend repositories inventory |
| `INVENTARIO-FED.md` | Frontend repositories inventory |
| `INVENTARIO-REPOSITORIOS.md` | Master index of all inventories |

**Contains**:
- Repository structure
- Endpoints and APIs
- Dependencies and configurations
- Technical specifications

**Generated with**: `PROMPT-INVENTARIO.md`

### 2. 🗺️ Maps (`documentation/mapa/`)

**Purpose**: Visual and textual maps of relationships between components.

| File | Description |
|------|-------------|
| `MAPA-REPOSITORIOS.md` | Complete repository relationship map |
| `MAPA-REPOSITORIOS-LISTAS.md` | Simplified list format |
| `MAPA-REPOSITORIOS.html` | Interactive HTML visualization |

**Contains**:
- FED → BFF relationships
- Endpoint mappings
- Architecture diagrams
- Integration flows

**Generated with**: `generate_mapa_endpoints.py` script

### 3. 🎯 Contexts (`documentation/contextos/`)

**Purpose**: Complete technical contexts for AI-assisted development.

| File | Description |
|------|-------------|
| `CONTEXTO-BOB-LEARNING-HUB.md` | Full platform technical context |

**Contains**:
- Architecture overview
- Technology stack
- Development patterns
- API contracts
- Configuration details
- Best practices

**Generated with**: `PROMPT-GERAR-CONTEXTO.md`

**Use Case**: Provide this file as context to AI tools when starting new development tasks for accurate, context-aware code generation.

---

## 📝 Prompts

Prompts are located in `documentation/prompts/` and are designed to be used with AI assistants to generate consistent documentation.

### Available Prompts

#### 1. `PROMPT-INVENTARIO.md`

**Purpose**: Generate detailed technical inventories of repositories.

**Usage**:
1. Copy the prompt content
2. Provide it to your AI assistant along with the repository code
3. The AI will generate a structured inventory following the template

**Output**: `INVENTARIO-{TYPE}.md` files

**What it generates**:
- Repository metadata
- File structure
- Endpoints and APIs
- Dependencies
- Configuration details

#### 2. `PROMPT-GERAR-CONTEXTO.md`

**Purpose**: Generate comprehensive technical context documents.

**Usage**:
1. Copy the prompt content
2. Provide it to your AI assistant along with existing inventories
3. The AI will consolidate information into a complete context file

**Output**: `CONTEXTO-{PROJECT}.md` files

**What it generates**:
- Platform overview
- Architecture diagrams
- Technology stack
- Development patterns
- API documentation
- Configuration guides

---

## 🤖 Scripts

Scripts are located in `scripts/` and automate documentation generation tasks.

### `generate_mapa_endpoints.py`

**Purpose**: Automatically generate repository maps from inventory files.

**Requirements**:
```bash
# Python 3.6+
# Optional: pip install markdown (for HTML generation)
```

**Usage**:
```bash
# Run from repository root
python scripts/generate_mapa_endpoints.py
```

**Process**:
1. 📖 Reads inventory files from `documentation/inventario/`
2. 🔍 Parses repository information and endpoints
3. 🔗 Maps relationships between components
4. 📝 Generates three output formats:
   - Markdown (`.md`)
   - List format (`-LISTAS.md`)
   - HTML visualization (`.html`)

**Output Files**:
- `documentation/mapa/MAPA-REPOSITORIOS.md`
- `documentation/mapa/MAPA-REPOSITORIOS-LISTAS.md`
- `documentation/mapa/MAPA-REPOSITORIOS.html`

**Example Output**:
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

For detailed script documentation, see **[scripts/README_SCRIPTS.md](scripts/README_SCRIPTS.md)**.

---

## 🚀 Quick Start

### For New Projects

**Step 1: Generate Inventories**

```bash
# 1. Copy the inventory prompt
cat documentation/prompts/PROMPT-INVENTARIO.md

# 2. Provide the prompt to your AI assistant along with your project code
# 3. Save the generated inventory to documentation/inventario/
```

**Step 2: Generate Repository Map**

```bash
# Run the map generator script
python scripts/generate_mapa_endpoints.py
```

**Step 3: Generate Complete Context**

```bash
# 1. Copy the context generation prompt
cat documentation/prompts/PROMPT-GERAR-CONTEXTO.md

# 2. Provide the prompt to your AI assistant along with the inventories
# 3. Save the generated context to documentation/contextos/
```

**Step 4: Use Context for Development**

```bash
# Provide the context file to your AI assistant when coding
# Example: "Here's the technical context for this project: [paste CONTEXTO-*.md]"
```

---

## 💡 Usage Examples

### Example 1: Starting a New Feature

```bash
# 1. Get the latest context
cat documentation/contextos/CONTEXTO-BOB-LEARNING-HUB.md

# 2. Provide to AI assistant with your request
"Using this context: [paste context]

I need to add a new endpoint for user authentication.
Please generate the code following the existing patterns."
```

### Example 2: Onboarding a New Developer

```bash
# Share these files for quick onboarding:
# 1. CONTEXTO-*.md - Complete technical overview
# 2. MAPA-REPOSITORIOS.html - Visual architecture map
# 3. INVENTARIO-*.md - Detailed component documentation
```

### Example 3: Updating Documentation

```bash
# After code changes:

# 1. Regenerate inventory using PROMPT-INVENTARIO.md
# 2. Run map generator
python scripts/generate_mapa_endpoints.py

# 3. Regenerate context using PROMPT-GERAR-CONTEXTO.md
# 4. Commit updated documentation
```

---

## 🔄 Documentation Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. Code Changes in Project                             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. Use PROMPT-INVENTARIO.md with AI                    │
│     → Generate updated INVENTARIO-*.md                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. Run generate_mapa_endpoints.py                      │
│     → Generate MAPA-*.md and .html                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. Use PROMPT-GERAR-CONTEXTO.md with AI                │
│     → Generate updated CONTEXTO-*.md                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  5. Use CONTEXTO-*.md for AI-Assisted Development       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Benefits

### For Developers

- ⚡ **Faster Onboarding**: Complete technical context in one file
- 🤖 **Better AI Assistance**: Accurate code generation with proper context
- 📚 **Always Up-to-Date**: Automated documentation generation
- 🔍 **Easy Navigation**: Visual maps and structured inventories

### For Teams

- 📖 **Consistent Documentation**: Standardized format across projects
- 🔄 **Maintainable**: Scripts automate repetitive tasks
- 🎓 **Knowledge Sharing**: Easy to share technical knowledge
- 🏗️ **Architecture Clarity**: Visual representation of system structure

---

## 🤝 Contributing

### Adding New Prompts

1. Create a new prompt file in `documentation/prompts/`
2. Follow the naming convention: `PROMPT-{PURPOSE}.md`
3. Include clear instructions and expected output format
4. Update this README with the new prompt documentation

### Improving Scripts

1. Fork the repository
2. Create a feature branch
3. Make your changes to scripts in `scripts/`
4. Test thoroughly
5. Update `scripts/README_SCRIPTS.md` with changes
6. Submit a pull request

### Updating Documentation

1. Use the existing prompts to regenerate documentation
2. Run scripts to update maps
3. Commit all updated files together
4. Include a clear commit message explaining what changed

---

## 📊 Documentation Standards

### File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Inventory | `INVENTARIO-{TYPE}.md` | `INVENTARIO-BFF.md` |
| Map | `MAPA-{SCOPE}.md` | `MAPA-REPOSITORIOS.md` |
| Context | `CONTEXTO-{PROJECT}.md` | `CONTEXTO-BOB-LEARNING-HUB.md` |
| Prompt | `PROMPT-{PURPOSE}.md` | `PROMPT-INVENTARIO.md` |

### Markdown Standards

- Use clear, descriptive headings
- Include tables for structured data
- Add code blocks with language specification
- Use emojis sparingly for visual organization
- Keep line length reasonable (80-120 characters)

---

## 🛠️ Requirements

### For Using Prompts
- Access to an AI assistant (ChatGPT, Claude, GitHub Copilot, etc.)
- Project code to analyze

### For Running Scripts
- Python 3.6 or higher
- Optional: `markdown` package for HTML generation
  ```bash
  pip install markdown
  ```

---

## 📄 License

This documentation toolkit is provided as-is for educational and development purposes.

---

## 🙏 Acknowledgments

This documentation system is designed to:
- Improve developer productivity
- Enhance AI-assisted development
- Maintain consistent technical documentation
- Facilitate knowledge sharing

---

<div align="center">

**⭐ Star this repository if you find these tools helpful!**

Made with 💻 and 📚 for better documentation

</div>
