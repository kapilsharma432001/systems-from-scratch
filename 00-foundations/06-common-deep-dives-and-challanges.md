## Regionalization & Latency
- Think of it as: where should my servers and data live so users get fast responses?
- If a user is in India and it has to talk to server in the US, the request physically travels a long distance (even with the speed of light, it can add unavoidable latency)
- In system design - it matters because latency is not caused by slow code or slow database. It can come from a network distance.

### Important Idea: Data Locality - performance is best when the data is close to the computation that needs it.

## CDNs
- A CDN or content delivery network, is a network of servers placed around the world. These CDN servers are often called edge locations. They are closed to users and can serven cached content quickly.
### CDNs are commonly used when the data is cacheable and queried globally. So, the user get the content faster and your backend gets less traffic.
- Example: for YouTube thumbnails, a CDN is great. For "Kapil's bank balance," a CDN caching is dangerous unless done with strict private caching controls.

## Regional Partitioning
- Regional partitioning means splitting your system by geography.
- Instead of one giant global system, you may have US Region, Europe Region, India Region, Southeast Asia Region.
- Each region has its own servers, caches and databases.
- Regional paritioning improves: latency, scalability, fault isolation, local compliance.
- But it makes these harder: cross-region consistency, global search, user migration between regions etc.

## Timeouts
- A timeout means - I will wait only this long for a response. After that, I stop waiting.
- Without timeouts, one slow dependency can make your system hang forever.

![timeouts](image-6.png)

- AWS builder library recommends setting timeouts for remote calls, including connection timeouts and request timeouts, because waiting too long consumes resources, while setting timeouts too low can cause un-ncessary retries and backend loads.

## Idempotency

- Retries are cool except when they have side effects. Imagine a payment system where we're trying to charge a user $10 or something. If we retry the same request multiple times, we're going to charge the user $20 (or $2000) instead of $10.
- This is why we need to make sure that our APIs are **idempotent**. 
- Idempotent APIs are the APIs that can be called multiple times but they always return the same result.
- GET requests are the common examples of idempotent keys. But reading data is okay, how about writing data? For these cases, it's common for us to introduce an idempotency key to our APIs. The idempotency key is a unique identifier for a request that we can use to make sure the same request is idempotent.
- For our payment example, if we know a user is only ever going to buy one item per day, we can set an idempotency to the user's ID and the current date. On the server side, we can check to see if we've already processed (or are currently processing) a request with that that idempotency key and process it only once.

## Circuit Breakers

- A fault - tolerance pattern used to stop repeatedly calling a failing sevice.
- Without a circuit breaker, order service keeps calling payment service, every request waits and fails, threads get stuck, order service also becomes slow or crashes.
- With a circuit breaker, after 5 failures, circuit opens - order service stops calling payment service temporarily and it immediately returns fallback response.