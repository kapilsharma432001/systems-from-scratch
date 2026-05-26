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
