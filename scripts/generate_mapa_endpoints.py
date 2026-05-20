#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_mapa_endpoints.py

Generates a repository map for the Bob-a-thon Learning Platform by parsing
inventory files (INVENTARIO-BFF.md and INVENTARIO-FED.md) and creating
relationship diagrams between frontend and backend repositories.

Output files:
  - MAPA-REPOSITORIOS.md (detailed markdown format)
  - MAPA-REPOSITORIOS-LISTAS.md (list format)
  - MAPA-REPOSITORIOS.html (visual HTML map)
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict
from datetime import date

# Configure UTF-8 encoding for stdout/stderr on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

try:
    import markdown
    _HAS_MARKDOWN = True
except ImportError:
    markdown = None  # type: ignore
    _HAS_MARKDOWN = False

os.environ["PYTHONIOENCODING"] = "utf-8"

# Directory paths
INVENTARIO_DIR = Path(__file__).parent.parent / "documentation" / "inventario"
MAPA_DIR = Path(__file__).parent.parent / "documentation" / "mapa"
OUTPUT_FILE = MAPA_DIR / "MAPA-REPOSITORIOS.md"
OUTPUT_LISTA_FILE = MAPA_DIR / "MAPA-REPOSITORIOS-LISTAS.md"
OUTPUT_HTML_FILE = MAPA_DIR / "MAPA-REPOSITORIOS.html"

# HTML template with Bob-a-thon branding
_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6; max-width: 1280px; margin: 0 auto; padding: 2rem 2.5rem; color: #24292e; }}
    h1 {{ font-size: 2rem; border-bottom: 2px solid #0969da; padding-bottom: 0.5rem; color: #0969da; }}
    h2 {{ font-size: 1.5rem; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.3rem; margin-top: 2.5rem; }}
    h3 {{ font-size: 1.15rem; margin-top: 3rem; padding: 0.6rem 1rem;
          background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px;
          border-left: 4px solid #0969da; }}
    code {{ background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 3px;
            padding: 0.15em 0.4em; font-family: SFMono-Regular, Consolas, monospace; font-size: 85%; }}
    pre  {{ background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px;
            padding: 1rem; overflow-x: auto; }}
    pre code {{ background: none; border: none; padding: 0; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.9rem; }}
    th {{ background: #f6f8fa; border: 1px solid #d0d7de; padding: 0.5rem 0.75rem;
          text-align: left; font-weight: 600; white-space: nowrap; }}
    td {{ border: 1px solid #d0d7de; padding: 0.4rem 0.75rem; vertical-align: top; }}
    tr:hover td {{ background: #f0f7ff; }}
    blockquote {{ border-left: 4px solid #0969da; color: #57606a; margin: 1rem 0;
                  padding: 0.25rem 1rem; background: #f6f8fa; border-radius: 0 4px 4px 0; }}
    hr {{ border: none; border-top: 1px solid #e1e4e8; margin: 2rem 0; }}
    a {{ color: #0969da; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    ul li {{ margin: 0.15rem 0; }}
    ul ul {{ margin: 0.1rem 0; }}
    .badge {{ display: inline-block; padding: 0.2em 0.6em; font-size: 0.85em;
              font-weight: 600; border-radius: 12px; margin-right: 0.5em; }}
    .badge-bff {{ background: #ddf4ff; color: #0969da; }}
    .badge-fed {{ background: #dafbe1; color: #1a7f37; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def split_into_sections(content: str, prefix: str = "") -> dict[str, str]:
    """
    Splits markdown content into sections by heading '### `repo-name`'.
    Returns dict {repo_name: section_text}.
    
    Args:
        content: Markdown content to parse
        prefix: Optional prefix to filter repository names (e.g., "bff-", "fed-")
    """
    pattern = re.compile(r'^### `([^`]+)`', re.MULTILINE)
    matches = list(pattern.finditer(content))
    sections = {}
    
    for i, m in enumerate(matches):
        repo_name = m.group(1).strip()
        
        # Filter by prefix if provided
        if prefix and not repo_name.startswith(prefix):
            continue
            
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_text = content[start:end].strip()
        sections[repo_name] = section_text
    
    return sections


def parse_table_after(text: str, anchor: str) -> list[list[str]]:
    """
    Parses a markdown table that appears after a specific anchor text.
    Returns list of rows, where each row is a list of cell values.
    
    Args:
        text: Section text to search
        anchor: Text to search for (e.g., "**Exposed endpoints**:")
    """
    idx = text.find(anchor)
    if idx == -1:
        return []
    
    rest = text[idx + len(anchor):]
    
    # Find table lines (start with |)
    lines = [line.strip() for line in rest.split('\n') if line.strip().startswith('|')]
    
    if len(lines) < 2:  # Need at least header + separator
        return []
    
    # Skip header and separator, parse data rows
    rows = []
    for line in lines[2:]:  # Skip header and separator
        if not line.strip():
            break
        cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last
        rows.append(cells)
    
    return rows


# ---------------------------------------------------------------------------
# Repository parsers
# ---------------------------------------------------------------------------

def parse_bffs(content: str) -> list[dict]:
    """
    Parses BFF inventory and extracts repository information.
    
    Returns list of dicts with structure:
    {
        'repo': str,
        'status': str,
        'base_path': str,
        'description': str,
        'endpoints': [{'method': str, 'path': str, 'operation_id': str, 'summary': str}],
        'feign_clients': [{'interface': str, 'url': str, 'endpoints': str}],
        'kafka_topics': list[str]
    }
    """
    sections = split_into_sections(content, prefix="bff-")
    results = []
    
    for repo, section in sections.items():
        # Extract status
        status_match = re.search(r'\*\*Status\*\*:\s*([^\n]+)', section)
        status = status_match.group(1).strip() if status_match else "Unknown"
        
        # Extract description (if exists)
        desc_match = re.search(r'\*\*Description\*\*:\s*([^\n]+)', section)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Extract base path
        base_path_match = re.search(r'\*\*Base path\*\*:\s*`([^`]+)`', section)
        base_path = base_path_match.group(1) if base_path_match else ""
        
        # Parse endpoints table
        endpoints = []
        endpoint_rows = parse_table_after(section, "**Exposed endpoints**:")
        for row in endpoint_rows:
            if len(row) >= 4 and row[0] != '—':
                endpoints.append({
                    'method': row[0],
                    'path': row[1],
                    'operation_id': row[2],
                    'summary': row[3]
                })
        
        # Parse Feign Clients table
        feign_clients = []
        feign_rows = parse_table_after(section, "**Feign Clients (consumes)**:")
        for row in feign_rows:
            if len(row) >= 3 and row[0] != 'None' and row[0] != '—':
                feign_clients.append({
                    'interface': row[0],
                    'url': row[1],
                    'endpoints': row[2]
                })
        
        # Parse Kafka topics
        kafka_topics = []
        kafka_match = re.search(r'\*\*Kafka Topics\*\*:\s*\n\s*(.+)', section)
        if kafka_match:
            kafka_text = kafka_match.group(1).strip()
            if kafka_text.lower() != 'none':
                kafka_topics = [t.strip() for t in kafka_text.split(',')]
        
        results.append({
            'repo': repo,
            'status': status,
            'base_path': base_path,
            'description': description,
            'endpoints': endpoints,
            'feign_clients': feign_clients,
            'kafka_topics': kafka_topics
        })
    
    return results


def parse_feds(content: str) -> list[dict]:
    """
    Parses FED inventory and extracts repository information.
    
    Returns list of dicts with structure:
    {
        'repo': str,
        'status': str,
        'description': str,
        'angular_version': str,
        'api_calls': [{'component': str, 'base_url': str, 'endpoints': str, 'bff_repo': str}]
    }
    """
    sections = split_into_sections(content, prefix="fed-")
    results = []
    
    for repo, section in sections.items():
        # Extract status
        status_match = re.search(r'\*\*Status\*\*:\s*([^\n]+)', section)
        status = status_match.group(1).strip() if status_match else "Unknown"
        
        # Extract description
        desc_match = re.search(r'\*\*Description\*\*:\s*([^\n]+)', section)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Extract Angular version
        angular_match = re.search(r'\*\*Angular version\*\*:\s*([^\n]+)', section)
        angular_version = angular_match.group(1).strip() if angular_match else ""
        
        # Parse Consumed APIs table
        api_calls = []
        api_rows = parse_table_after(section, "**Consumed APIs**:")
        for row in api_rows:
            if len(row) >= 3:
                # Extract BFF repo name from URL if possible
                base_url = row[1]
                bff_repo = None
                
                # Try multiple patterns to extract BFF name from URL
                # Pattern 1: bff-name-env.domain.com or bff-name.domain.com
                bff_match = re.search(r'(bff-[a-z0-9-]+?)(?:-env)?\.', base_url)
                if bff_match:
                    bff_repo = bff_match.group(1)
                # Pattern 2: /bff-name/ in path
                elif '/bff-' in base_url:
                    bff_match = re.search(r'/(bff-[a-z0-9-]+)', base_url)
                    if bff_match:
                        bff_repo = bff_match.group(1)
                
                api_calls.append({
                    'component': row[0],
                    'base_url': base_url,
                    'endpoints': row[2],
                    'bff_repo': bff_repo
                })
        
        results.append({
            'repo': repo,
            'status': status,
            'description': description,
            'angular_version': angular_version,
            'api_calls': api_calls
        })
    
    return results


# ---------------------------------------------------------------------------
# Map generation
# ---------------------------------------------------------------------------

def generate_mapa(bffs: list[dict], feds: list[dict]) -> str:
    """
    Generates the main repository map in markdown format.
    Shows relationships between FED and BFF repositories.
    """
    lines = []
    
    # Header
    lines.append("# Mapa de Endpoints — Bob-a-thon Learning Platform")
    lines.append("")
    lines.append(f"> **Gerado automaticamente** a partir dos inventários em `documentation/inventario/`")
    lines.append(f"> **Data de geração**: {date.today().isoformat()}")
    lines.append("")
    
    # Build FED → BFF mapping
    fed_to_bff = defaultdict(list)
    for fed in feds:
        for call in fed['api_calls']:
            if call['bff_repo']:
                if call['bff_repo'] not in fed_to_bff[fed['repo']]:
                    fed_to_bff[fed['repo']].append(call['bff_repo'])
    
    # Build BFF → FED reverse mapping
    bff_to_fed = defaultdict(list)
    for fed_repo, bff_list in fed_to_bff.items():
        for bff_repo in bff_list:
            if fed_repo not in bff_to_fed[bff_repo]:
                bff_to_fed[bff_repo].append(fed_repo)
    
    # Index section
    lines.append("---")
    lines.append("")
    lines.append("## Índice")
    lines.append("")
    lines.append("| # | Seção | Descrição |")
    lines.append("|---|-------|-----------|")
    lines.append("| 1 | [FED → BFF (Chamadas HTTP)](#1-fed--bff-chamadas-http) | Mapeamento de chamadas do frontend para o backend |")
    lines.append("| 2 | [Cadeia Completa por BFF](#2-cadeia-completa-por-bff) | Visão consolidada end-to-end de cada BFF |")
    lines.append("")
    
    # Section 1: FED → BFF (HTTP Calls)
    lines.append("---")
    lines.append("")
    lines.append("## 1. FED → BFF (Chamadas HTTP)")
    lines.append("")
    lines.append("> Mapeamento de chamadas HTTP dos frontends para os backends")
    lines.append("")
    lines.append("| FED | URL Base | BFF de Destino | Endpoints Chamados |")
    lines.append("|-----|----------|----------------|-------------------|")
    
    for fed in sorted(feds, key=lambda x: x['repo']):
        for call in fed['api_calls']:
            if call['bff_repo']:
                lines.append(f"| `{fed['repo']}` | {call['base_url']} | `{call['bff_repo']}` | {call['endpoints']} |")
    
    lines.append("")
    
    # Section 2: Complete Chain per BFF
    lines.append("---")
    lines.append("")
    lines.append("## 2. Cadeia Completa por BFF")
    lines.append("")
    lines.append("> Visão consolidada end-to-end de cada BFF, mostrando FEDs consumidores e endpoints expostos")
    lines.append("")
    
    for bff in sorted(bffs, key=lambda x: x['repo']):
        lines.append(f"### `{bff['repo']}`")
        lines.append("")
        
        # FED consumers
        if bff['repo'] in bff_to_fed:
            lines.append("**FED consumidor:**")
            for fed_repo in sorted(bff_to_fed[bff['repo']]):
                lines.append(f"- `{fed_repo}`")
        else:
            lines.append("**FED consumidor:**")
            lines.append("- None")
        
        lines.append("")
        
        # Exposed endpoints
        lines.append("**Endpoints expostos:**")
        if bff['endpoints']:
            for ep in bff['endpoints']:
                lines.append(f"- {ep['method']} {ep['path']}")
        else:
            lines.append("- None")
        
        lines.append("")
        
        # Description
        if bff['description']:
            lines.append("**Descrição:**")
            lines.append(bff['description'])
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


def generate_lista_repos(bffs: list[dict], feds: list[dict]) -> str:
    """
    Generates a list format showing BFF chains with their FED consumers.
    Only includes BFFs that have identified FED consumers.
    """
    lines = []
    
    # Build FED → BFF mapping
    fed_to_bff = defaultdict(set)
    for fed in feds:
        for call in fed['api_calls']:
            if call['bff_repo']:
                fed_to_bff[fed['repo']].add(call['bff_repo'])
    
    # Build BFF → FED reverse mapping
    bff_to_fed = defaultdict(list)
    for fed_repo, bff_set in fed_to_bff.items():
        for bff_repo in bff_set:
            if fed_repo not in bff_to_fed[bff_repo]:
                bff_to_fed[bff_repo].append(fed_repo)
    
    # Sort FEDs for each BFF
    for bff_repo in bff_to_fed:
        bff_to_fed[bff_repo].sort()
    
    # Count BFFs with FED consumers
    bffs_with_fed = len(bff_to_fed)
    total_bffs = len(bffs)
    
    # Header
    lines.append("# Lista de Repositórios por Funcionalidade — Bob-a-thon Learning Platform")
    lines.append("")
    lines.append("> Derivado da Seção 2 do MAPA-REPOSITORIOS.md")
    lines.append("> **Apenas BFFs com FED consumidor identificado estão listados.**")
    lines.append(f"> **Gerado em**: {date.today().isoformat()} — **{bffs_with_fed} BFF com fluxo FED** (de {total_bffs} no inventário)")
    lines.append("")
    
    # Process each BFF that has FED consumers
    for bff in sorted(bffs, key=lambda x: x['repo']):
        if bff['repo'] not in bff_to_fed:
            continue
        
        # Count total repositories in chain (FEDs + BFF + dependencies)
        # For now, simplified: just FEDs + BFF
        fed_consumers = bff_to_fed[bff['repo']]
        total_repos = len(fed_consumers) + 1  # FEDs + BFF itself
        
        lines.append("---")
        lines.append("")
        lines.append(f"## `{bff['repo']}`")
        lines.append("")
        lines.append(f"> **{total_repos} repositórios** na cadeia completa")
        lines.append("")
        lines.append("| Repositório | Tipo | Papel na Cadeia |")
        lines.append("|-------------|------|-----------------|")
        
        # Add FED consumers (sorted alphabetically)
        for fed_repo in sorted(fed_consumers):
            lines.append(f"| `{fed_repo}` | FED | FED consumidor |")
        
        # Add BFF principal
        lines.append(f"| `{bff['repo']}` | BFF | BFF principal |")
        
        lines.append("")
    
    return '\n'.join(lines)


def generate_html(md_content: str) -> str:
    """
    Converts markdown content to HTML using the template.
    """
    if _HAS_MARKDOWN and markdown is not None:
        try:
            body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        except Exception:
            # Fallback if markdown conversion fails
            body = f"<pre>{md_content}</pre>"
    else:
        # Fallback: wrap in <pre> if markdown library not available
        body = f"<pre>{md_content}</pre>"
    
    return _HTML_TEMPLATE.format(
        title="Bob-a-thon Repository Map",
        body=body
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Main execution function."""
    print("🚀 Bob-a-thon Repository Map Generator")
    print("=" * 60)
    print()
    
    # Read inventory files
    print("📖 Reading inventory files...")
    
    bff_file = INVENTARIO_DIR / "INVENTARIO-BFF.md"
    fed_file = INVENTARIO_DIR / "INVENTARIO-FED.md"
    
    if not bff_file.exists():
        print(f"❌ Error: {bff_file} not found")
        return 1
    
    if not fed_file.exists():
        print(f"❌ Error: {fed_file} not found")
        return 1
    
    bff_content = bff_file.read_text(encoding='utf-8')
    fed_content = fed_file.read_text(encoding='utf-8')
    
    # Parse inventories
    print("🔍 Parsing BFF repositories...")
    bffs = parse_bffs(bff_content)
    print(f"   Found {len(bffs)} BFF repositories")
    
    print("🔍 Parsing FED repositories...")
    feds = parse_feds(fed_content)
    print(f"   Found {len(feds)} FED repositories")
    print()
    
    # Generate outputs
    print("📝 Generating repository map...")
    mapa_content = generate_mapa(bffs, feds)
    
    print("📝 Generating repository list...")
    lista_content = generate_lista_repos(bffs, feds)
    
    print("📝 Generating HTML visualization...")
    html_content = generate_html(mapa_content)
    
    # Ensure output directory exists
    MAPA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write output files
    print()
    print("💾 Writing output files...")
    
    OUTPUT_FILE.write_text(mapa_content, encoding='utf-8')
    print(f"   ✅ {OUTPUT_FILE}")
    
    OUTPUT_LISTA_FILE.write_text(lista_content, encoding='utf-8')
    print(f"   ✅ {OUTPUT_LISTA_FILE}")
    
    OUTPUT_HTML_FILE.write_text(html_content, encoding='utf-8')
    print(f"   ✅ {OUTPUT_HTML_FILE}")
    
    print()
    print("✨ Done! Repository map generated successfully.")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
