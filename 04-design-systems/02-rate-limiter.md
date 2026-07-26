# Designing Rate Limiter

## What is rate limiter?

- A rate limiter controls how many requests a client can make within a specific time frame.
- It acts like a traffic controller for your API—allowing, for example, "100 requests per minute" from a user, then rejecting excess requests with an HTTP 429 "Too Many Requests" response.
- Prevents abuse, protects your servers from being overwhelmed by bursts of traffic, and ensure fair usage across all users.

> [!NOTE]
> Excellent problem—the main difficulty here is: where the limiter lives, which algorithm it uses, and how multiple servers update the same counter safely.

## We will follow the exact same framework from Hello Interview which is:

`Requirements -> Core Entities -> API or Interface -> Data Flow (it is not applicable for this scenario) -> High-Level Design -> Deep Dives`

### The most important topics going to be are:

- Rate Limiter Placement
- Client Identification (by API key, IP, `client_id`, etc.)
- Token-bucket Algorithm
- Redis Shared State
- Atomic Updates
- Redis Sharding
- Fail-open vs Fail-closed

## Simplest Mental Model

**Suppose the rule is:**

A user can make 100 requests per minute.

**For every incoming request, the rate limiter asks:**

- Who is making the request?
- Which rule applies?
- Has the client crossed the limit?
- Return the success or error response (should I allow or reject the request?)

**The simple mental model will be:**

```text
Request arrives -> Identify client -> Find applicable rules -> Check and update usage -> Allow request or return HTTP 429 (429 Too Many Requests)
```

## Requirements

### Functional Requirements

- Identify the client (using user ID, API key, IP address, etc.)
- Limit HTTP requests based on the configurable rules (e.g., 100 API requests per minute per user)
- Reject excess requests using `429 Too Many Requests`
- Return useful information such as limits remaining (remaining requests), current limit, time until retry, etc.

### Non-functional Requirements

Let's assume that we are designing it for substantial but realistic load: 1 million requests per second across 100 million daily active users.

- Availability >> consistency (from CAP theorem—limiter should be highly available): eventual consistency is okay as slight delays across nodes are acceptable
- The system should introduce minimum latency overhead (< 10 ms per request check)
- The system should handle 1M requests/second across 100M DAU.

### Out of Scope:

- Billing
- Handling DDoS attack
- Complex machine learning abuse detection
- Detailed analytics, etc.

## Core Entities

- **Requests:** the incoming API request that need to be evaluated against rate-limiting rules. The request can carry context like client identity, etc.
- **Clients:** the entities being rate limited.
- **Rules:** the rate limit policy.

## System Interface

- A rate limiter is a infrastructure component that other services call to check if a request should be allowed. The interface is straightforward:

isRequestAllowed(client_id, rule_id, current_time) -> RateLimitResult

-> This method takes an identifier (userId, IP address, or API key) and a rule identifier, then returns whether the request should be allowed based on the current usage. It also provides information for response headers like X-RateLimit-Remaining and X-RateLimit-Reset
