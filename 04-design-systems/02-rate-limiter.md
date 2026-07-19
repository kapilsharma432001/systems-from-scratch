# Designing a Rate Limiter

## What Is a Rate Limiter?

- A rate limiter controls how many requests a client can make within a specific time frame.
- It acts like a traffic controller for your API. For example, it might allow a user to make 100 requests per minute, then reject excess requests with an HTTP 429 "Too Many Requests" response.
- It prevents abuse, protects your servers from being overwhelmed by traffic bursts, and ensures fair usage across all users.

> [!NOTE]
> This is an excellent system design problem. The main challenges are deciding where the limiter should live, which algorithm it should use, and how multiple servers can safely update the same counter.

## Design Framework

We will follow the same framework used by Hello Interview:

`Requirements → Core Entities → API or Interface → Data Flow → High-Level Design → Deep Dives`

> [!NOTE]
> The data-flow step is not applicable to this scenario.

### Key Topics

- Rate limiter placement
- Client identification by API key, IP address, or client ID
- Token bucket algorithm
- Shared state in Redis
- Atomic updates
- Redis sharding
- Fail-open versus fail-closed behavior

## Simplest Mental Model

Suppose the rule allows a user to make 100 requests per minute.

For every incoming request, the rate limiter asks:

- Who is making the request?
- Which rule applies?
- Has the client exceeded the limit?
- Should the request be allowed or rejected?

The simple request flow is:

```text
    → Request arrives
    → Identify the client
    → Find the applicable rule
    → Check and update usage
    → Allow the request or return HTTP 429 Too Many Requests
```
