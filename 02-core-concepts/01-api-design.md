## API - Application Programming Interface

- It allows different components of a software system to communicate with each other using a set of rules and protocols.
- API design means defining how clients and services talk to your system.

#### In an interview, you will typically choose between three main protocols: REST, GraphQL, and RPC (Remote Procedure Call)

1. **REST (Representational State Transfer):**
   - REST is usually resource-based.
   - REST uses standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) to manipulate resources identified by URLs.
   - A resource is a thing in your system, such as:
     - User
     - Product
     - Payment
     - Cart
     - Comment
     - Post

   Use nouns, not verbs.

   Good:

   ```text
   GET /products/123
   POST /orders
   DELETE /comments/456
   ```

   Avoid:

   ```text
   GET /getProduct
   POST /createOrder
   POST /deleteComment
   ```

   Different HTTP methods:

   - `GET`: Reads data.
   - `POST`: Creates a resource. `POST` is not idempotent, which means if you make the same request again and again, it may create different resources.
   - `PUT`: Updates or replaces a resource. `PUT` is idempotent, which means if you make the same request again and again, it should update the same resource instead of creating a new one.
   - `DELETE`: Deletes a resource.

   REST for CRUD operations:

   For standard CRUD operations, REST maps naturally to your database operations and HTTP semantics, making it the go-to protocol for most web services.

2. **GraphQL:**
   - GraphQL is a query language for APIs.
   - It allows the client to ask for exactly the data it needs.
   - With REST, you may have multiple endpoints. GraphQL usually uses a single endpoint with a query language that lets the client specify exactly what data it needs.
   - With GraphQL, you can request related data in one request.

   Example request:

   ```graphql
   {
     user(id: "123") {
       name
       email
       orders {
         id
         total
       }
     }
   }
   ```

   Example response:

   ```json
   {
     "data": {
       "user": {
         "name": "Alice",
         "email": "alice@example.com",
         "orders": [
           {
             "id": "ord_1",
             "total": 99
           }
         ]
       }
     }
   }
   ```

3. **RPC (Remote Procedure Call):**
   - RPC protocols like gRPC use binary serialization and HTTP/2 for efficient communication between services.
   - RPC shines in microservice architectures where services need to communicate frequently and efficiently.
   - RPC lets one service call another service using methods like `getUser()` or `chargePayment()`.
   - If the interviewer mentions internal service communication, high-performance requirements, or polyglot environments (different services in different languages), RPC is likely a good choice.
   - Binary serialization and HTTP/2 make RPC significantly faster than JSON-based REST in many internal service-to-service use cases.
   - For a Ticketmaster example, you may use REST APIs for public endpoints that mobile apps and web clients consume, but use gRPC for internal communication between your booking service, payment service, and inventory service.

### Common API Patterns

Whether you choose REST, GraphQL, or RPC, there are some common API patterns that apply across all API types.

#### Pagination

- When you are dealing with large datasets, you cannot return everything at once. Imagine an API that returns all events ever created. That could be millions of records and many gigabytes of data.
- Instead, you need pagination to break large result sets into manageable chunks. There are two main approaches to pagination: offset-based and cursor-based.

##### Offset-Based Pagination

Offset pagination uses:

- `offset`: how many records to skip.
- `limit`: how many records to return.
- For example, `/products?limit=10&offset=0` returns records 1 to 10.
- The next page, `/products?limit=10&offset=10`, returns records 11 to 20.

Advantages:

- Simple to understand.
- Easy to implement.
- Good when data is small and stable.
- Allows users to jump to page 5, page 10, etc.

Problems with offset-based pagination:

- **Slow with large offsets:** Suppose the offset is `1000000` and the limit is `20`. The database may have to scan or skip 1,000,000 rows before returning 20 rows.
- **Duplicate or missing results:** Suppose page 1 returns `A, B, C, D, E`. Before the user requests page 2, someone inserts a new item, `X`, at the top. Now, if the user requests page 2, page 2 may return `E, F, G, H, I`. The problem is that `E` appears twice.
- Some items may also be skipped because the data changed between requests.

##### Cursor-Based Pagination

- Cursor-based pagination uses a cursor to remember where the previous page ended.
- Instead of saying, "skip 100 rows," we say, "give me 100 rows after this last seen item."

Example first request:

```text
GET /orders?limit=10
```

Example response:

```json
{
  "items": [
    {
      "id": "ord_100",
      "createdAt": "2026-05-26T10:00:00Z"
    },
    {
      "id": "ord_099",
      "createdAt": "2026-05-26T09:59:00Z"
    }
  ],
  "nextCursor": "eyJjcmVhdGVkQXQiOiIyMDI2LTA1LTI2VDA5OjU5OjAwWiIsImlkIjoib3JkXzA5OSJ9"
}
```

Next request:

```text
GET /orders?limit=10&cursor=eyJjcmVhdGVkQXQiOiIyMDI2LTA1LTI2VDA5OjU5OjAwWiIsImlkIjoib3JkXzA5OSJ9
```

Meaning: give me 10 records after the cursor returned by the previous response.

- The cursor often looks like a random string because it is encoded.
- Internally, the cursor may contain the last seen sort key:

  ```json
  {
    "createdAt": "2026-05-26T09:59:00Z",
    "id": "ord_099"
  }
  ```

Advantages:

- Good for large datasets.
- Avoids duplicate or missing items better than offset-based pagination.
- Works well for feeds, chats, timelines, and order history.

Disadvantages:

- More complex than offset-based pagination.
- Harder to jump to page 10 directly.

Can you jump from page 1 to page 10?

- Not directly, because cursor-based pagination is designed for next/previous navigation.
- To reach page 10, the client usually follows cursors page by page until it reaches page 10.
- If direct page jumps are required, you can store a cursor map, such as `page 1 -> cursorA`, `page 2 -> cursorB`, and so on, after those pages have been visited or precomputed.
- For admin dashboards or tables where page jumps are important, offset-based pagination may be a better fit.

Used in:

- Instagram feed.
- Twitter/X timeline.
- Chat messages.
- Order history.

#### Interview note

In interviews, offset pagination is generally fine unless you are dealing with real-time data or the interviewer specifically asks you to handle a large volume of data.

### Versioning Strategies

- APIs evolve over time, and you need a strategy for handling changes without breaking existing clients.
- The most common approach is **URL versioning**, where you include the version number in the path, such as `/v1/events` or `/v2/events`.
  - Most common approach.
  - Simple to implement.
  - Clients know exactly which version they are using by looking at the URL.

- **Header versioning:** Header versioning puts the version in the HTTP header instead, such as `Accept-Version: v2` or `API-Version: 2`. This keeps URLs cleaner and follows HTTP standards better, but it is less obvious to developers and harder to test in the browser.
