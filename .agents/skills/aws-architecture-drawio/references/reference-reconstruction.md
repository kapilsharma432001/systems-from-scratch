# Reference-image reconstruction

Use this workflow when the user supplies a diagram or sketch that should become editable draw.io content.

## Extract before drawing

Inspect the source at the highest useful resolution and create a compact spec containing:

```yaml
canvas:
  orientation: landscape
  reading_order: left-to-right
zones:
  - id: realtime
    label: Serverless real-time backend
nodes:
  - id: api
    source_label: API Gateway
    kind: aws_service
    aws_service: Amazon API Gateway
    zone: realtime
    evidence: explicit
edges:
  - source: api
    target: executor
    direction: forward
    step: 2
    semantics: synchronous invocation
annotations:
  - anchor: executor
    text: The agent decides which tools to use
```

The spec need not be written to disk, but it must be complete enough to account for every meaningful source element.

## Fidelity order

Preserve these in priority order:

1. Components and directed relationships
2. Boundary membership and online/offline separation
3. Branches, joins, feedback paths, and sequence numbering
4. Service identity and labels
5. Explanatory annotations
6. Relative placement and visual style

Do not preserve a visual mistake that would make the reconstructed diagram misleading. Correct it conservatively and mention the deviation when material.

## Reference comparison pass

After rendering, compare source and output side by side. Check:

- every source node is represented or intentionally omitted
- every arrow has the correct source, target, and direction
- no AWS service or boundary was invented
- step numbers remain attached to the correct interaction
- top-level zones and their relative arrangement match
- online and offline paths remain visually distinct
- annotations are associated with the correct service or edge
- important return paths are not mistaken for forward paths

For complex references, count the source and output nodes and edges. A count mismatch is a prompt to re-inspect, not automatic proof of an error.

## Unclear source content

Use the visible label as written when it is readable. If a label, icon, arrow direction, or boundary is genuinely ambiguous and materially affects the architecture, ask the user rather than guessing. Minor unreadable prose may be conservatively summarized if its architectural meaning is clear.
