# Designing a Rate Limiter

## What Is a Rate Limiter?

- A rate limiter controls how many requests a client can make within a specific time frame.
- It acts like a traffic controller for your API. For example, it might allow a user to make 100 requests per minute, then reject excess requests with an HTTP 429 "Too Many Requests" response.
- It prevents abuse, protects your servers from being overwhelmed by traffic bursts, and ensures fair usage across all users.

> [!NOTE]
> This is an excellent system design problem. The main challenges are deciding where the limiter should live, which algorithm it should use, and how multiple servers can safely update the same counter.
