# Systems From Scratch

A structured system design learning repository focused on backend engineering, distributed systems, scalability, and interview preparation.

This repository is my personal system design playbook. The goal is to build strong fundamentals first, then apply those fundamentals to real-world system design problems like URL Shortener, News Feed, Chat System, Notification System, File Storage, Rate Limiter, and AI/RAG systems.

Most of the learning material and structure here is inspired by [Hello Interview](https://www.hellointerview.com/). I use it as one of my main references, then rewrite the ideas in my own words as I learn and revise them.

This repo is inspired by Hello Interview, but all notes are written in my own words.

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
├── LICENSE
│
├── .agents/
│   └── skills/
│       └── aws-architecture-drawio/   # AWS draw.io diagram tooling
│
├── 00-foundations/
│   ├── 01-what-is-system-design.md
│   ├── 02-core-concepts.md
│   ├── 03-networking-essentials.md
│   ├── 04-application-layer-protocols.md
│   ├── 05-load-balancing.md
│   ├── 06-common-deep-dives-and-challanges.md
│   └── image*.png
│
├── 01-key-technologies/
│   ├── 01-key-techs.md
│   ├── 02-blob-storage.md
│   ├── 03-search-optimized-database.md
│   ├── 04-api-gateway.md
│   ├── 05-queues.md
│   ├── 06-load-balancer.md
│   ├── 07-steams-or-event-sourcing.md
│   ├── 08-distributed-lock.md
│   ├── 09-distributed-cache.md
│   ├── 10-CDN.md
│   └── image*.png
│
├── 02-core-concepts/
│   ├── README.md
│   ├── 01-api-design.md
│   ├── 02-data-modeling.md
│   ├── 03-caching.md
│   ├── 04-sharding.md
│   ├── 05-consistent-hashing.md
│   ├── 06-CAP-theorem.md
│   ├── 07-authenticaton.md
│   └── image*.png
│
├── 03-Common-Patterns/
│   ├── common-patterns.md
│   └── image*.png
│
├── 04-design-systems/
│   ├── 00-systems-to-learn.md
│   ├── 003-RAG-systems-prerequisites.md
│   ├── 01-url-shortener.md
│   ├── 02-rate-limiter.md
│   ├── 03-RAG-System.md
│   ├── 04-an-event-driven-architecture.md
│   └── *.png
│
└── drawio-architecture-diagrams/
    ├── File Ingestion Pipeline.drawio
    └── File Ingestion Pipeline.png
```

Image files inside the topic folders are supporting diagrams for the notes. The
`drawio-architecture-diagrams` folder contains editable diagram sources and their
rendered previews. The `.agents` folder contains repository tooling and is not
part of the learning sequence.

---

## Current Topics

### 00 - Foundations

- [What is System Design?](00-foundations/01-what-is-system-design.md)
- [Core Concepts](00-foundations/02-core-concepts.md)
- [Networking Essentials](00-foundations/03-networking-essentials.md)
- [Application Layer Protocols](00-foundations/04-application-layer-protocols.md)
- [Load Balancing](00-foundations/05-load-balancing.md)
- [Common Deep Dives and Challenges](00-foundations/06-common-deep-dives-and-challanges.md)

### 01 - Key Technologies

- [Key Technologies](01-key-technologies/01-key-techs.md)
- [Blob Storage](01-key-technologies/02-blob-storage.md)
- [Search-Optimized Database](01-key-technologies/03-search-optimized-database.md)
- [API Gateway](01-key-technologies/04-api-gateway.md)
- [Queues](01-key-technologies/05-queues.md)
- [Load Balancer](01-key-technologies/06-load-balancer.md)
- [Streams or Event Sourcing](01-key-technologies/07-steams-or-event-sourcing.md)
- [Distributed Lock](01-key-technologies/08-distributed-lock.md)
- [Distributed Cache](01-key-technologies/09-distributed-cache.md)
- [CDN](01-key-technologies/10-CDN.md)

### 02 - Core Concepts

- [Core Concepts](02-core-concepts/README.md)
- [API Design](02-core-concepts/01-api-design.md)
- [Data Modeling](02-core-concepts/02-data-modeling.md)
- [Caching](02-core-concepts/03-caching.md)
- [Sharding](02-core-concepts/04-sharding.md)
- [Consistent Hashing](02-core-concepts/05-consistent-hashing.md)
- [CAP Theorem](02-core-concepts/06-CAP-theorem.md)
- [Authentication](02-core-concepts/07-authenticaton.md)

### 03 - Common Patterns

- [Common Patterns](03-Common-Patterns/common-patterns.md)

### 04 - Design Systems

- [Systems to Learn](04-design-systems/00-systems-to-learn.md)
- [RAG System Prerequisites and Ingestion Pipeline](04-design-systems/003-RAG-systems-prerequisites.md)
- [URL Shortener](04-design-systems/01-url-shortener.md)
- [Rate Limiter](04-design-systems/02-rate-limiter.md)
- [RAG System](04-design-systems/03-RAG-System.md)
- [Event-Driven Architecture](04-design-systems/04-an-event-driven-architecture.md)

### Architecture Diagrams

- [File Ingestion Pipeline (editable draw.io source)](drawio-architecture-diagrams/File%20Ingestion%20Pipeline.drawio)
- [File Ingestion Pipeline (PNG preview)](drawio-architecture-diagrams/File%20Ingestion%20Pipeline.png)
