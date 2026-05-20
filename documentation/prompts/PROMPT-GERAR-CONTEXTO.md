---
description: >
  Generates a comprehensive context file for a feature by analyzing all involved repositories
  and consolidating their technical details into a single reference document.
---

# Prompt: Generate Feature Context

## Repositories to Analyze in This Batch

> List **all** repositories involved in the feature's communication chain.

```
REPOSITORIES:
- fed-bob-a-thon
- bff-bob-a-thon
```

---

## Instructions for AI

You must generate a complete technical context file for the feature implemented by the repositories listed above, following the pattern established in `CONTEXTO-BOB-LEARNING-HUB.md`.

### Step 1: Analyze Repositories

Read the inventory files for all listed repositories:
- `documentation/inventario/INVENTARIO-FED.md` (for `fed-*` repos)
- `documentation/inventario/INVENTARIO-BFF.md` (for `bff-*` repos)
- `documentation/inventario/INVENTARIO-SRV.md` (for `srv-*` repos, if applicable)
- `documentation/inventario/INVENTARIO-API.md` (for `api-*` repos, if applicable)

Also read:
- `documentation/mapa/MAPA-REPOSITORIOS.md` — to understand the complete communication flow
- `documentation/mapa/MAPA-REPOSITORIOS-LISTAS.md` — to confirm repository relationships

### Step 2: Determine Feature Name

Based on the repositories' purposes and exposed endpoints, **automatically generate** a descriptive feature name. Examples:
- If repos handle course catalog → "Catálogo de Cursos" or "Bob Learning Hub"
- If repos handle user authentication → "Autenticação de Usuários"
- If repos handle payment processing → "Processamento de Pagamentos"

The feature name should be:
- **Descriptive**: Clearly indicates what the feature does
- **Concise**: 2-4 words maximum
- **Portuguese**: Use Brazilian Portuguese for consistency

### Step 3: Generate Context File

Create a file named `CONTEXTO-[FEATURE-NAME-KEBAB-CASE].md` in `documentation/contextos/`.

The generated file must follow this structure:

```markdown
# Contexto: [Nome da Funcionalidade]

> **Uso deste documento**: Forneça este arquivo como contexto único em novas solicitações relacionadas a [funcionalidade]. Ele consolida a arquitetura, os detalhes técnicos de todos os repositórios e o contexto geral da demanda — servindo tanto como referência para novas conversas com IA quanto como base para criar especificações técnicas, descrições de histórias de desenvolvimento e critérios de aceite.

---

## 1. Visão Geral da Demanda

[Descrição da funcionalidade, objetivos, propósito]

---

## 2. Arquitetura dos Componentes

[Diagrama ASCII mostrando fluxo entre repositórios]

### Repositórios

| Repositório | Tipo | Responsabilidade |
|-------------|------|------------------|
| ... | ... | ... |

---

## 3. Stack Tecnológica

[Tecnologias usadas em cada repositório]

### Frontend (se aplicável)
- Angular: versão
- TypeScript: características
- State Management: abordagem
- etc.

### Backend (BFF/SRV)
- Java: versão
- Spring Boot: versão
- Arquitetura: padrão
- etc.

---

## 4. [Para cada repositório BFF/SRV]

### Responsabilidade
[O que este serviço faz]

### Estrutura de Código
[Organização de pastas e arquivos principais]

### Endpoints Expostos
[Tabela com método, path, operationId, descrição]

### Contratos Principais
[Request/Response de endpoints críticos]

### Feign Clients (se aplicável)
[Tabela com interface, URL, endpoints chamados]

### Kafka Topics (se aplicável)
[Tabela com tópico, conteúdo, formato]

### Configurações Técnicas
[Tabela com propriedades, valores, observações]

---

## 5. Frontend (se aplicável)

### Responsabilidade
[O que o frontend faz]

### Estrutura do Projeto
[Organização de componentes, serviços, etc.]

### Arquitetura do Frontend
[Padrões, state management, etc.]

### Integração com Backend
[Como consome APIs, URLs, endpoints]

### Funcionalidades Implementadas
[Lista numerada de features]

---

## 6. Fluxo Principal [da Funcionalidade]

[Diagrama ASCII mostrando fluxo end-to-end de uma operação típica]

---

## 7. Padrões de Desenvolvimento

### Frontend (se aplicável)
[Convenções, estrutura, boas práticas]

### Backend
[Arquitetura, convenções, boas práticas]

---

## 8. Configuração de Ambiente

### Pré-requisitos
[Ferramentas necessárias]

### Executando Localmente
[Comandos para cada repositório]

### Variáveis de Ambiente
[Lista de variáveis críticas]

---

## 9. Testes

### Frontend (se aplicável)
[Estratégia, cobertura, comandos]

### Backend
[Estratégia, cobertura, comandos]

---

## 10. Documentação Complementar

### Arquivos de Referência
[Links para inventários, mapas, etc.]

### Diagramas
[Diagramas de arquitetura e fluxo]

---

## 11. Contribuindo

### Processo de Desenvolvimento
[Workflow de contribuição]

### Padrões de Commit
[Conventional Commits]

### Code Review
[Critérios de aprovação]

---

## 12. Requisitos Não Funcionais

[Tabela com requisito e especificação]

---

## 13. Glossário

[Tabela com termos e definições específicas da funcionalidade]

---

## 14. Contatos e Suporte

### Repositórios
[Lista de repositórios]

### Recursos
[Issues, Discussions, Wiki]

---

**Última atualização**: [data]
**Versão do documento**: [versão]
**Mantenedores**: [equipe]
```

---

---

## How to Use This Prompt

Simply **edit the repository list** at the top of this file and provide it to the AI. The AI will:

1. ✅ Read the inventory files for all listed repositories
2. ✅ Analyze the communication flow between them
3. ✅ Automatically determine an appropriate feature name
4. ✅ Generate the complete context file with proper naming
5. ✅ Save it to `documentation/contextos/CONTEXTO-[FEATURE-NAME].md`

**Example:**

If you list:
```
REPOSITORIES:
- fed-bob-a-thon
- bff-bob-a-thon
```

The AI will:
- Analyze both repositories
- Determine the feature is "Bob Learning Hub" (or similar)
- Generate `CONTEXTO-BOB-LEARNING-HUB.md`
- Populate all 14 sections with relevant technical details

---

## Diretrizes Importantes

### O que INCLUIR no contexto:

✅ **Arquitetura completa** — diagrama mostrando todos os repositórios e suas interações
✅ **Detalhes técnicos** — endpoints, contratos, configurações de cada repositório
✅ **Fluxos end-to-end** — como uma requisição percorre toda a cadeia
✅ **Stack tecnológica** — versões, frameworks, bibliotecas de cada repo
✅ **Padrões de código** — convenções estabelecidas em cada repositório
✅ **Configuração de ambiente** — como rodar localmente, variáveis necessárias
✅ **Testes** — estratégias e comandos para cada repositório
✅ **Documentação complementar** — links para inventários e mapas
✅ **Glossário** — termos específicos da funcionalidade

### O que NÃO INCLUIR no contexto:

❌ **Roadmap ou melhorias futuras** — o contexto documenta o estado atual, não planos futuros
❌ **Histórico de mudanças** — não é um changelog
❌ **Decisões de design antigas** — foque no estado atual da arquitetura
❌ **Código-fonte completo** — apenas estrutura e trechos relevantes
❌ **Informações sensíveis** — senhas, tokens, credenciais reais

### Formato e Estilo:

- Use **Markdown** com formatação consistente
- Inclua **diagramas ASCII** para visualização de arquitetura e fluxos
- Use **tabelas** para informações estruturadas (endpoints, configurações, etc.)
- Use **blocos de código** com syntax highlighting apropriado
- Mantenha **seções numeradas** para fácil referência
- Seja **técnico e preciso** — este documento é para desenvolvedores
- Seja **conciso mas completo** — evite redundância, mas não omita informações críticas

### File Naming Convention

Pattern: `CONTEXTO-[FEATURE-NAME-KEBAB-CASE].md`

The AI must automatically generate the filename based on the determined feature name:
- Feature: "Bob Learning Hub" → `CONTEXTO-BOB-LEARNING-HUB.md`
- Feature: "Catálogo de Cursos" → `CONTEXTO-CATALOGO-CURSOS.md`
- Feature: "Gestão de Usuários" → `CONTEXTO-GESTAO-USUARIOS.md`
- Feature: "Relatórios Financeiros" → `CONTEXTO-RELATORIOS-FINANCEIROS.md`

---

## Validação do Contexto Gerado

Após gerar o contexto, verifique se ele responde estas perguntas:

- [ ] Qual é o propósito da funcionalidade?
- [ ] Quais repositórios estão envolvidos e como se comunicam?
- [ ] Quais tecnologias são usadas em cada repositório?
- [ ] Quais são os endpoints expostos e seus contratos?
- [ ] Como executar cada repositório localmente?
- [ ] Quais são as variáveis de ambiente necessárias?
- [ ] Como rodar os testes?
- [ ] Quais são os padrões de código estabelecidos?
- [ ] Onde encontrar documentação complementar?

Se todas as perguntas forem respondidas claramente no documento, o contexto está completo.

---

## Manutenção do Contexto

O arquivo de contexto deve ser atualizado quando:

- ✏️ Novos repositórios são adicionados à cadeia
- ✏️ Endpoints são criados, modificados ou removidos
- ✏️ Stack tecnológica é atualizada (versões, frameworks)
- ✏️ Padrões de código são alterados
- ✏️ Configurações críticas mudam

**Importante**: Sempre atualize a data e versão no rodapé do documento após modificações.

---

## Exemplo Completo

Para ver um exemplo completo de contexto gerado, consulte:

- `documentation/contextos/CONTEXTO-BOB-LEARNING-HUB.md` — exemplo com 2 repositórios (FED, BFF)

---

**Versão do prompt**: 1.0.0  
**Última atualização**: 2026-05-20