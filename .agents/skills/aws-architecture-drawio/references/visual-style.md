# Visual Style Reference

Use this file as the layout and styling contract for client-ready AWS diagrams.

## Canvas and containers

- Canvas: white or nearly white.
- Keep visible outer margins around the architecture.
- Section containers should have a thin neutral border and no decorative shadow.
- Section titles belong near the upper-left edge with enough padding.
- Prefer one large meaningful container over several nested decorative frames.
- Do not draw a visible outer border around the entire page unless the user asks for it.
- In reference-reconstruction mode, preserve the source's major zone arrangement and relative proportions when doing so does not compromise readability.
- Treat workflow sections and technical boundaries differently: workflow sections use neutral borders; Region, VPC, and subnet boundaries use their verified AWS conventions only when architecturally true.

Suggested section style:

```text
rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#879196;strokeWidth=1;fontSize=13;fontStyle=1;verticalAlign=top;align=left;spacingTop=8;spacingLeft=10;
```

## AWS service nodes

Use the exact style returned by the AWS4 shape catalog when possible.

The core AWS4 resource-icon pattern is:

```text
shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<verified_service_name>;
```

Typical dimensions are approximately 64–78 px. Keep the same icon size for peers at the same visual level.

Do not recolor official AWS service icons.

Generic processing components should be visually subordinate to AWS service icons. Use a restrained neutral fill and border; do not imitate an AWS service color or invent a product glyph.

## Labels

- Default label size: 12–14 px.
- Prefer labels under the icon.
- Center-align labels.
- Keep most labels to one or two lines.
- Avoid abbreviations the audience may not know.
- Keep descriptive paragraphs outside the icon node.

Suggested plain text style:

```text
text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=12;
```

## Primary connectors

Preferred:

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#545B64;strokeWidth=1.5;endArrow=open;endFill=0;
```

Use 90-degree routing and waypoints.

Avoid diagonal paths unless the user explicitly wants them.

## Secondary / asynchronous connectors

Only use dashes when the dash encodes real meaning:

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#687078;strokeWidth=1.2;endArrow=open;endFill=0;dashed=1;dashPattern=8 4;
```

## Numbered flow badges

Use small, unobtrusive badges close to the flow.

Suggested style:

```text
ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#232F3E;strokeColor=#232F3E;fontColor=#FFFFFF;fontStyle=1;fontSize=11;
```

A badge should be roughly 18–22 px.

Use the badge shape found in a supplied reference when reconstructing it. AWS reference diagrams commonly use compact square badges; circles remain suitable for net-new diagrams. Keep all badges in a diagram consistent unless branches require suffixes such as `4a` and `4b`.

## Annotations

Annotations explain the architecture but should not dominate it.

Suggested style:

```text
text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=11;
```

Keep annotation width narrow enough to avoid sprawling paragraphs.

## Spacing heuristics

These are guidelines, not hard constants:

- horizontal center-to-center spacing: about 180–240 px
- vertical center-to-center spacing: about 140–220 px
- clear gap around labels, borders, and connectors: about 24–40 px
- keep related peers aligned to a common baseline
- keep long background flows on a separate row or lower section

## Crossings

When two lines would cross:

1. rearrange nodes;
2. route one edge around the outside;
3. add waypoints;
4. only as a last resort accept a crossing.

Never route a line directly through an icon, service label, section heading, or step badge.

For long cross-boundary edges, reserve whitespace corridors before placing nodes. Use explicit waypoints for return paths, branch merges, and connections that span more than one section.

## Visual hierarchy

- Actors and external systems sit outside AWS or application boundaries.
- AWS services use official icons and short labels.
- Logical actions use neutral boxes or diamonds.
- Persistent stores and indexes sit at branch destinations or shared lane interfaces.
- Long explanations use standalone annotations anchored near the relevant node or edge.
- The primary path should be visually discoverable without reading every label.

## Composition

For AWS-reference-style diagrams:

- left side often contains actors/channels
- center contains orchestration/application services
- right side often contains data/AI/downstream systems
- lower lanes can contain ingestion, indexing, ETL, and batch work

This is a useful convention, not a rule. Technical truth wins over symmetry.
