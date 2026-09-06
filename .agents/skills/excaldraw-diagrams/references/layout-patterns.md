# Layout Patterns

Choose the smallest pattern that makes the requested relationship obvious. Do not add a diagram type merely because the source has many items.

## System architecture

Use left-to-right request flow with vertical semantic zones such as Client, Edge, Application, Data, and External Services.

- Put the principal path near the visual center.
- Put state stores below their owning compute unless a data-centric story requires a dedicated data lane.
- Keep cross-zone connectors horizontal where possible.
- Route feedback and response lines through a top or bottom return corridor.
- Use frames only for actual system, network, account, region, team, or deployment boundaries.

## Data or ingestion pipeline

Use left-to-right phases: source, intake, validation, processing, storage/indexing, and status/observability.

- Show the success path as one continuous spine.
- Put rejection, retry, dead-letter, and reprocessing paths below it.
- Number steps when order matters.
- Split fan-out only after the shared validation stage and rejoin it explicitly when downstream work requires all branches.

## Flowchart or decision process

Use top-to-bottom for procedural reading and left-to-right only when the process is short.

- Rectangles are actions; diamonds are decisions; ellipses are starts/ends.
- Label outgoing decision branches directly, such as `yes` and `no`.
- Keep the dominant/success branch straight. Bend the exception branch.
- Avoid crossing a branch back through the decision diamond.

## Sequence or interaction diagram

Arrange participants left to right and time top to bottom.

- Keep participant columns fixed.
- Align each message row.
- Use dashed return arrows only when returns add useful information.
- Group repeated or conditional interactions in a frame with a clear condition.
- Do not use a sequence layout for a static dependency graph.

## Comparison

Use parallel columns with shared row headings or mirrored structures.

- Align equivalent components.
- Keep text density and node scale comparable.
- Use color only for meaningful differences, not to decorate each column.

## Concept map

Place the central concept near the center and arrange first-level branches radially or in balanced quadrants.

- Limit first-level branches to a readable number.
- Use curved connectors only when they reduce crossings.
- Prefer relationship labels over arrowheads when direction is not central.

## Reference reconstruction

1. Measure the source's outer bounds and major zones.
2. Record node centers, relative sizes, and reading direction.
3. Reconstruct topology and grouping with plain shapes.
4. Reserve connector corridors and place all route labels.
5. Add styling, badges, icons, and annotations.
6. Compare the render against the reference at the same aspect ratio.

## Connector corridor planning

Use direct pairwise arrows for nearby steps. Plan a corridor only when the relationship cannot remain local. For the remaining routes, identify:

- horizontal lanes between node rows;
- vertical gutters between columns or frames;
- one outer corridor for feedback/return paths;
- dedicated fan-in and fan-out trunks;
- label landing areas on long segments.

An explicit waypoint belongs at every necessary turn. If an ordinary edge needs more than one dogleg, first move its source, destination, or obstacle. If a route still crosses an unrelated node or label, move the route, move the label, or change the layout—do not hide the problem with color.
