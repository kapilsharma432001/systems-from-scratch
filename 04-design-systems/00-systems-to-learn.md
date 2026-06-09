# Systems to Learn

We need to start building systems that repeatedly teach the core patterns: API design, schema design, caching, queues, sharding, fan-out, idempotency, consistency, contention, search, and observability.

## Learning Order

Here is the order that we are going to follow:

1. URL Shortener
2. Rate Limiter
3. Notification System
4. File Storage / Dropbox
5. News Feed
6. Chat / WhatsApp
7. Post Search / Search System
8. Ticket Booking / Ticketmaster
9. Metrics Monitoring / Datadog
10. Web Crawler
11. Video Streaming / YouTube
12. Ride Sharing / Uber

## Eight Most Important Systems

- `01-url-shortener.md`
- `02-rate-limiter.md`
- `03-notification-system.md`
- `04-file-storage-system.md`
- `05-news-feed.md`
- `06-chat-system.md`
- `07-search-system.md`
- `08-ticket-booking-system.md`

## Systems and Topics to Learn

| Order | System                            | Why this first?                                                      | Main concepts you will master                                                           |
| ----: | --------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
|     1 | **URL Shortener**                 | Best first design. Small scope, but teaches the full interview flow. | APIs, DB schema, short-code generation, cache, redirects, analytics, sharding           |
|     2 | **Rate Limiter**                  | Teaches infrastructure design and edge protection.                   | Redis, token bucket/sliding window, API gateway, race conditions, fail-open/fail-closed |
|     3 | **Notification System**           | Teaches asynchronous architecture very well.                         | Queues, retries, priority, fan-out, delivery status, provider failure                   |
|     4 | **File Storage / Dropbox**        | Teaches blob storage and metadata separation.                        | S3 / blob storage, presigned URLs, CDN, file metadata, permissions                      |
|     5 | **News Feed**                     | One of the most important senior-level problems.                     | Fan-out on write/read, feeds, ranking, cache, graph relationships                       |
|     6 | **Chat / WhatsApp**               | Teaches real-time systems.                                           | WebSockets, message ordering, delivery status, offline users, presence                  |
|     7 | **Post Search / Search System**   | Teaches indexing and read/write scaling.                             | Inverted index, ingestion pipeline, query service, ranking, caching                     |
|     8 | **Ticket Booking / Ticketmaster** | Teaches high-contention systems.                                     | Transactions, locking, double-booking prevention, payments, consistency                 |
|     9 | **Metrics Monitoring / Datadog**  | Teaches time-series and ingestion-heavy systems.                     | Metrics ingestion, aggregation, time-series DB, alerting                                |
|    10 | **Web Crawler**                   | Teaches large-scale distributed workers.                             | Queues, deduplication, politeness, robots.txt, scheduling                               |
|    11 | **Video Streaming / YouTube**     | Do after File Storage. It is advanced.                               | Upload pipeline, transcoding, CDN, adaptive streaming                                   |
|    12 | **Ride Sharing / Uber**           | Do later. It combines many hard problems.                            | Geospatial indexing, matching, real-time location, queues, state machines               |


## Delivery Framework to Follow
- This is the delivery framework we are going to follow in each and every problem that we are going to take.
- Requirements -> Core Entities -> API or Interface -> Data flow -> High-Level Design -> Deep Dives
![Delivery Framework](image.png)