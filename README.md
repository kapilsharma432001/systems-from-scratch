# Systems From Scratch

A structured system design learning repository focused on backend engineering, distributed systems, scalability, and interview preparation.

This repository is my personal system design playbook. The goal is to build strong fundamentals first, then apply those fundamentals to real-world system design problems like URL Shortener, News Feed, Chat System, Notification System, File Storage, Rate Limiter, and AI/RAG systems.

---

## Why This Repository Exists

System design is not about memorizing diagrams.

It is about understanding requirements, identifying bottlenecks, choosing the right components, and explaining trade-offs clearly.

This repository is created to:

- Build system design fundamentals from scratch
- Prepare for backend and full-stack engineering interviews
- Practice structured thinking for ambiguous problems
- Create reusable revision notes
- Document trade-offs, patterns, and architecture decisions
- Improve communication during system design interviews

---

## Learning Philosophy

Every topic in this repository follows a simple rule:

> Learn the concept deeply, explain it simply, connect it to real systems, and revise it repeatedly.

Each note should answer:

- What is this concept?
- Why does it exist?
- What problem does it solve?
- Where is it used in real systems?
- What are the trade-offs?
- How should I explain it in an interview?

---

## Repository Structure

```text
systems-from-scratch/
│
├── README.md
├── ROADMAP.md
├── REVISION_TRACKER.md
│
├── 00-foundations/
│   ├── 01-what-is-system-design.md
│   ├── 02-client-server-model.md
│   ├── 03-networking-basics.md
│   ├── 04-latency-throughput-bandwidth.md
│   ├── 05-scalability.md
│   ├── 06-availability-reliability.md
│   ├── 07-cap-theorem.md
│   └── 08-numbers-to-know.md
│
├── 01-databases/
│   ├── 01-sql-vs-nosql.md
│   ├── 02-indexing.md
│   ├── 03-replication.md
│   ├── 04-sharding.md
│   ├── 05-partitioning.md
│   ├── 06-transactions.md
│   └── 07-normalization-denormalization.md
│
├── 02-core-components/
│   ├── 01-load-balancer.md
│   ├── 02-cache.md
│   ├── 03-message-queues.md
│   ├── 04-kafka.md
│   ├── 05-cdn.md
│   ├── 06-object-storage.md
│   ├── 07-search.md
│   ├── 08-api-gateway.md
│   ├── 09-rate-limiting.md
│   └── 10-observability.md
│
├── 03-patterns/
│   ├── 01-scaling-reads.md
│   ├── 02-scaling-writes.md
│   ├── 03-consistent-hashing.md
│   ├── 04-event-driven-architecture.md
│   ├── 05-realtime-communication.md
│   ├── 06-backpressure.md
│   ├── 07-retries-and-idempotency.md
│   └── 08-data-consistency-patterns.md
│
├── 04-designs/
│   ├── 01-url-shortener.md
│   ├── 02-rate-limiter.md
│   ├── 03-notification-system.md
│   ├── 04-file-storage-system.md
│   ├── 05-chat-system.md
│   ├── 06-news-feed.md
│   ├── 07-video-streaming-platform.md
│   ├── 08-payment-system.md
│   └── 09-rag-system.md
│
├── 05-interview-framework/
│   ├── 01-requirements-gathering.md
│   ├── 02-capacity-estimation.md
│   ├── 03-api-design.md
│   ├── 04-data-modeling.md
│   ├── 05-high-level-design.md
│   ├── 06-deep-dives.md
│   ├── 07-failure-handling.md
│   └── 08-tradeoff-communication.md
│
└── assets/
    └── diagrams/