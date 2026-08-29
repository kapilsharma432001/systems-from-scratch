# Layout patterns

Select the smallest pattern that tells the architecture clearly. Adapt the pattern to technical truth rather than forcing services into fixed positions.

## Request/response

Use one primary horizontal lane:

```text
Actor -> Entry point -> Application/orchestration -> Data or downstream services
```

Place authentication near the entry point and supporting services above or below the component they affect.

## Event-driven

Keep producers, event infrastructure, consumers, and destinations in successive columns. Use dashed connectors only if the diagram's legend or labels make their asynchronous meaning clear. Place retries and dead-letter handling in a secondary lane only when present in the source.

## File ingestion

Use a horizontal or lower offline lane:

```text
Source -> Event/queue -> Parse/OCR -> Route -> Transform/chunk -> Persist/index
```

After a content router, align structured and unstructured branches on separate rows. Keep their storage destinations at the same right-side boundary.

## RAG with online and offline paths

Use two strongly separated lanes:

- **Upper lane:** user request, API, orchestration, retrieval, model response
- **Lower lane:** documents, extraction, chunking, embedding, indexing

Place shared indexes or databases at the interface between the lanes when both paths use them. Do not duplicate a shared service merely for symmetry.

## Multi-zone reference architecture

Use a small number of large sections, such as frontend, real-time backend, document storage, metadata extraction, and semantic indexing. Put actors outside the sections. Use section headers in the upper-left with sufficient padding for nearby icons.

Long cross-zone edges should travel through whitespace corridors. Route return paths around the outside of the primary flow when necessary. Prefer one clean additional bend to a connector crossing an icon or annotation.

## Layout acceptance checks

- Major flow begins at the left or top and has a clear destination.
- Peer services align to common baselines.
- Branches separate immediately after the decision point and do not weave back together visually unless they truly join.
- Boundary titles remain unobstructed.
- Labels have at least 20–30 px clearance from unrelated connectors.
- Long annotations occupy whitespace rather than widening every service label.
- The full diagram remains legible at approximately 70% zoom.
