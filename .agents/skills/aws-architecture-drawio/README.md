# AWS Architecture Draw.io Codex Skill

This package teaches Codex to create editable, client-ready AWS architecture diagrams in draw.io rather than generic flowcharts.

## Install the skill

User-wide:

```bash
mkdir -p ~/.agents/skills/aws-architecture-drawio
cp -R aws-architecture-drawio/* ~/.agents/skills/aws-architecture-drawio/
```

Or put the folder in a repository at:

```text
.agents/skills/aws-architecture-drawio/
```

Restart Codex if it was already running.

## Strongly recommended: add a draw.io MCP server

The skill defines the design and quality rules. A draw.io MCP gives Codex actual diagram-editing operations and access to the current shape catalog.

One useful AWS sample MCP can be registered with Codex like this:

```bash
codex mcp add drawio -- npx -y \
  https://github.com/aws-samples/sample-drawio-mcp/releases/latest/download/drawio-mcp-server-latest.tgz \
  --no-cache
```

Verify:

```bash
codex mcp list
```

## Example prompt

```text
$aws-architecture-drawio

Create a client-ready AWS architecture diagram for this system.

Requirements:
- editable draw.io source
- official AWS4 icons
- visually similar in quality and composition to AWS reference architecture diagrams
- left-to-right main request path
- separate lower lane for offline ingestion
- numbered steps where they improve the story
- short annotations near important transitions
- orthogonal connectors with minimal crossings
- no Mermaid as the final artifact

Architecture:
[describe the system here]

Return:
1. architecture.drawio
2. architecture.png if export is available
```

## Files

- `SKILL.md` — the main Codex instructions
- `references/visual-style.md` — spacing, connectors, labels, containers
- `references/aws4-common-shapes.md` — common verified AWS4 stencil names
- `templates/base.drawio.xml` — a minimal editable draw.io template
- `scripts/validate_drawio.py` — structural validator for generated files
