# Design URL Shortener

## Problem Statement

Design a URL shortener like Bitly.

A URL shortener allows users to submit a long URL and receive a shorter URL. When someone opens the short URL, the system redirects them to the original long URL.

Example:

```text
Long URL:
https://example.com/articles/system-design/url-shortener?id=12345

Short URL:
https://short.ly/abc123
```

![Delivery Framework](image.png)

### 1. Functional Requirements

- Users should be able to submit a long URL and receive a shortened version.
  - Optionally, users should be able to specify a custom alias for their shortened URL (i.e., "www.short.ly/my-custom-alias")
  - Optionally, users should be able to specify an expiration date for their shortened URL.
- Users should be able to access the original URL by using the shortened URL.

Out of scope:

- User authentication & account management
- Analytics on link clicks (e.g., click counts, geographic data)

### 2. Non-functional Requirements

- System should ensure uniqueness for the short codes (each short code maps to exactly one long URL)
- The redirection should occur with minimal delay (< 100 ms)
- The system should be highly available - 99.99% of the time (availability > consistency)
- The system should support 1B shortened URLs and 100M DAU

![Requirements](image-1.png)

### 3. Core Entities

- Original URL: The long URL that user wants to shorten
- Short URL: The shortened URL that user receives and can share
- User: Represents a user who wants to create the short URL

### 4. API or Interface

- **Simply go one by one through the core requirements and define the APIs that are necessary to satisfy them. Usually, these map 1:1 to the functional requirements, but there are times when multiple endpoints are needed to satisfy an individual functional requirement.**

- To shorten a URL, we'll need a POST endpoint that takes in the long URL and optionally a custom alias and expiration date, and returns the shortened URL. We use POST here because we are creating a new entry in our database mapping the long URL to the newly created short URL.

```text
// Shorten a URL
POST /urls
{
  "long_url": "https://www.example.com/some/very/long/url",
  "custom_alias": "optional_custom_alias",
  "expiration_date": "optional_expiration_date"
}
->
{
  "short_url": "http://short.ly/abc123"
}
```

- For redirection, we'll need a GET endpoint that takes in the short code and redirects the user to the original long URL. GET is the right verb here because we are reading the existing long URL from our database based on the short code.

```text
// Redirect to Original URL
GET /{short_code}
-> HTTP 302 Redirect to the original long URL
```

- We can actually return 301 or 302 code from the URL, but 302 allows us to have more control because the browser does not permanently cache the URL. However, if we return 301, browser can cache the URL and then we won't have control if link expires, gets deleted or needs analytics tracking.

> Bonus: the database schema could look like this.

- We can have a table called `url_mappings` with columns like `short_code`, `long_url`, `is_active`, `user_id`, `created_at`, and `expires_at`.

![DATABASE SCHEMA OF SHORT URL](image-2.png)

### 5. High-Level Design

- **Go one by one through the functional requirements and design a single system to satisfy them.**

#### 1) Users should be able to submit a long URL and receive a short URL

- In a URL shortener, the main algorithmic question is: how do we generate a short code that is unique, small, and fast to create?
- We usually do not directly convert the long URL into a short URL. We first generate the short code, store it in a database, and map it to the long URL.

![example of short code generation](image-3.png)

```text
long_url
   |
   v
generate unique short_code
   |
   v
store short_code -> long_url
   |
   v
return https://short.ly/{short_code}
```

##### Best simple approach: Unique ID + Base62 encoding

###### Step 1: Generate a unique numeric ID

- We can generate a unique number using a database auto-increment ID, database sequence, or Redis atomic counter.
- Example: `10000001`, `10000002`, `10000003`, and so on. Every number is unique.

###### Step 2: Convert the number into Base62

- Base62 uses:
  - `0-9`: 10 characters
  - `a-z`: 26 characters
  - `A-Z`: 26 characters
- Total: 62 characters, so instead of using only digits, we use 62 possible characters.
- This helps make the short code shorter.
- Why Base62? Because it gives many combinations with fewer characters.

![Why Base62?](image-4.png)

- The flow would be to generate a unique number using a Redis atomic counter, database auto-increment ID, database sequence, etc., and then run `base62(unique_id)`. This gives us a unique short code.
- This makes sure that two records cannot have the same short code.

**But then what about custom aliases?**

- Sometimes a user may want `https://short.ly/kapil`.
- In this case, the system does not generate the code.
- Instead:
  - Check if `kapil` already exists.
  - If it exists, reject the request.
  - If it does not exist, store it as a mapping with the long URL.

**Why not hash the long URL?**

- Hashing long URLs can lead to collisions.

#### 2) Users should be able to access the long URL (original URL) by using the shortened URL

- Now our short URL is live, and users can access the original URL by using the shortened URL.
- Importantly, the short URL exists at a domain we own. For example, if our site is located at `short.ly`, then our short URLs look like `short.ly/abc123`, and all requests to that short URL go to our primary server.

![Redirect to original URL](image-5.png)

- There are two types of requests to our server:
  1. `POST /urls`: Generates a short URL.
  2. `GET /{short_code}`: Looks up the original URL in the database.
- When a user accesses a shortened URL, the following process occurs:
  1. The user's browser sends a GET request to our server with the short code (`GET /abc123`).
  2. Our primary server receives this request and looks up the short code in the database.
  3. If the short code is found and has not expired, the server retrieves the corresponding long URL. For expired URLs, return a `410 Gone` status.
  4. The server sends an HTTP redirect response to the user's browser, instructing it to navigate to the original long URL.

### Potential Deep Dives

#### 1. How can we ensure short URLs are unique?

- A good solution is to use a unique counter with Base62 encoding.
- One way to guarantee that there are no collisions is to increment a counter for each new URL. We can take the output of the counter and encode it using Base62 encoding to make it compact.
- **Redis is particularly well-suited for managing this counter because it is single-threaded and supports atomic operations. An atomic operation either completes entirely or does not complete at all. Because Redis is single-threaded, it processes one command at a time, eliminating race conditions. Its `INCR` command atomically increments the counter and returns the new value in a single operation.**

![Counter with Base62 encoding](image-6.png)

#### 2. How can we ensure that redirects are fast?

- Implement an in-memory cache, such as Redis or Memcached.
- We can introduce an in-memory cache between the application server and the database.
- The cache stores frequently accessed mappings of short codes to long URLs.
- When a redirect request comes in, the server checks the cache first. If the short code is found in the cache, the server retrieves the long URL from the cache, significantly reducing latency. If it is not found (cache miss), the server queries the database and stores the result in the cache for future requests.

![In-memory cache](image-7.png)
