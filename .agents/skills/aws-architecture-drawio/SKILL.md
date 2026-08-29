---
name: aws-architecture-drawio
description: Create or reconstruct accurate AWS architecture diagrams as editable draw.io files using verified AWS4 icons, explicit technical-evidence tracking, deliberate connector routing, and render-based visual QA. Use for AWS architecture, infrastructure, ingestion, event-driven, RAG, or reference-image-to-draw.io requests. Do not use Mermaid as the final artifact unless the user explicitly requests it.
---

# AWS Architecture Draw.io

Create technically truthful, editable `.drawio` diagrams that are visually comparable to polished AWS reference architectures.

## Select the operating mode

- **Text-to-architecture:** derive the architecture from prose, code, or configuration.
- **Sketch conversion:** preserve the sketch's components and relationships while improving layout and labels.
- **Reference reconstruction:** reproduce the supplied diagram's zones, nodes, flows, annotations, and reading order. Read [references/reference-reconstruction.md](references/reference-reconstruction.md).
- **Existing draw.io edit:** preserve correct content and established visual conventions unless the user requests a redesign.

For every mode, read [references/technical-accuracy.md](references/technical-accuracy.md). Read [references/layout-patterns.md](references/layout-patterns.md) when the architecture has multiple lanes, online/offline paths, branches, or more than one major boundary. Follow [references/visual-style.md](references/visual-style.md) for layout and styling.

## Required workflow

### 1. Build an architecture spec before drawing

Inventory:

- actors and external systems
- AWS services and generic logical components
- storage, queues, events, models, and background jobs
- boundaries and execution lanes
- every directed edge, including labels and sync/async meaning
- branches, joins, feedback paths, and step numbers
- annotations that explain non-obvious behavior

Record whether each service mapping is explicit, safely inferred, ambiguous, or merely suggested. Do not silently resolve an ambiguity that changes the architecture.

### 2. Choose the visual story

Prefer a left-to-right primary path. Put batch, ingestion, ETL, and indexing work in a separate lower lane when that separation clarifies the system. Use a small number of meaningful boundaries, not a container per service.

Plan long or cross-boundary connectors before generating XML. Add explicit waypoints when automatic orthogonal routing could cross an icon, label, title, or unrelated edge.

### 3. Use verified shapes

Use the built-in AWS4 draw.io library. Consult [references/aws4-common-shapes.md](references/aws4-common-shapes.md) and use only cataloged `resIcon` names. If a service is absent, verify it against the current draw.io AWS4 catalog before adding it to both the diagram and catalog.

Do not replace a generic technology with a particular AWS managed service merely to obtain an AWS icon. Generic application logic may use restrained neutral shapes.

### 4. Generate the editable artifact

Prefer a draw.io/diagram-editing tool when available. Otherwise generate uncompressed draw.io XML using [templates/base.drawio.xml](templates/base.drawio.xml). For architectures with an upper real-time path and lower ingestion/indexing path, start from [templates/aws-reference-multilane.drawio.xml](templates/aws-reference-multilane.drawio.xml) when its zones fit the source.

Use:

- official AWS icons at a consistent 64–78 px visual scale
- labels normally at least 12 px
- thin neutral boundaries
- solid primary flows and semantically meaningful dashed secondary/asynchronous flows
- compact edge labels only when they add meaning
- numbered badges only when a real sequence exists
- short annotations near, rather than inside, service icons

### 5. Validate structure and layout

Run:

```bash
python3 scripts/validate_drawio.py <diagram.drawio>
```

Treat errors as blocking. Review warnings rather than ignoring them. The validator checks XML, IDs, edge references, AWS stencils, basic geometry, canvas bounds, and likely node overlaps.

### 6. Render and inspect

Visual QA is required whenever a renderer is available:

```bash
python3 scripts/render_drawio.py <diagram.drawio> --format png
```

Inspect the rendered PNG or SVG and iterate until:

- no labels or icons are clipped
- no important connector crosses a node or label
- boundaries contain their intended children
- major lanes and branch directions are immediately clear
- icon sizes, baselines, and spacing are consistent
- the reference's major topology and reading order are preserved

If rendering is unavailable, state that only structural and geometric validation was completed. Never claim visual validation without inspecting a render.

## Technical boundaries

Show Region, VPC, Availability Zone, subnet, account, and trust boundaries only when supported by the source or explicitly requested. Do not place managed AWS services inside a VPC merely for visual symmetry.

## Output

Always deliver the editable `<name>.drawio`. Also deliver the inspected PNG or SVG preview when it was generated or requested.

The reader should be able to identify the entry point, main path, storage destinations, asynchronous/background work, AI/ML participation, and major system boundaries within five seconds.
