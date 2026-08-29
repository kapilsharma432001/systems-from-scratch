# Technical accuracy

## Evidence ledger

Classify each material architectural decision:

- **Explicit:** directly named or visibly shown in the source.
- **Safely inferred:** necessary to represent an unambiguous relationship without selecting a new product or boundary.
- **Ambiguous:** multiple materially different interpretations are possible.
- **Suggested:** a best-practice improvement not present in the requested architecture.

Draw explicit and safely inferred content. Ask about ambiguous content when it would change service selection, security posture, network placement, data ownership, or flow direction. Do not add suggested content unless the user requests design recommendations.

## Service-mapping rules

- Do not map generic PostgreSQL, Redis, Kafka, Kubernetes, object storage, or an embedding model to an AWS managed service solely for styling.
- A product logo or explicit AWS service name is sufficient evidence for that service.
- When only a technology is explicit, use a generic editable shape and preserve the technology label.
- Use the parent AWS service icon for a named feature or model that lacks a dedicated verified stencil, and put the feature or model in the label.
- Do not invent VPCs, subnets, Availability Zones, endpoints, IAM roles, encryption, retries, dead-letter queues, monitoring, or high-availability topology.

## Boundary rules

- Boundary membership is an architectural claim, not decoration.
- Do not place an AWS service inside a VPC unless the source or architecture supports that placement. Some managed services deploy into or attach to a VPC, while others remain outside it and are reached through public or private endpoints.
- Keep actors and external systems outside AWS boundaries unless the source says otherwise.
- A section used only to explain a workflow should have a neutral label such as `Offline ingestion`; do not label it as a network boundary.

## Flow rules

- Preserve arrow direction exactly.
- Distinguish control flow, request/response, event publication, queue consumption, and read/write operations when the distinction matters.
- Use dashed lines only when they encode a stated semantic such as asynchronous, optional, or scheduled execution.
- Do not add bidirectional arrows merely because a service may technically return a response.
- Keep sequence numbers consistent across branches; use `4a`/`4b` only when the source or story actually branches at step 4.

## Completeness review

Before finalizing, account for authentication, observability, retry behavior, scheduling, secrets, encryption, model invocation, vector indexing, and structured storage as one of: shown, absent, unknown, or intentionally out of scope. This is a review aid, not permission to add missing services.
