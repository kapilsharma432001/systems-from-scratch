# Load Balancing

- Load balancer distributes incoming traffic across multiple servers.
- Load balancing means distributing incoming traffic across multiple servers.
- A load balancer sits between clients and backend servers.
- It decides which server should handle each request.
- It helps with scalability, high availability and fault tolerance.

Basic flow:

```text
Client -> Load Balancer -> Server 1
                      -> Server 2
                      -> Server 3
```

System design insight: once one server is not enough, we usually add more servers and place a load balancer in front of them.
-> The goal is to avoid overloading one machine and make the system more available.

## Why Load Balancing Exists

Without a load balancer:

- One server can become overloaded.
- If the server goes down, the whole system may be unavailable.
- It is harder to add or remove servers safely.

With a load balancer:

- Traffic can be spread across many servers.
- Unhealthy servers can be removed from rotation.
- New servers can be added without changing the client.
- The system can handle more users.

## Vertical Scaling

- Vertical scaling means making one machine bigger.
- This usually means adding more CPU, RAM, disk or network capacity to the same server.

Example:

```text
Small server -> Bigger server
4 CPU, 8 GB RAM -> 32 CPU, 128 GB RAM
```

Vertical scaling is simple because the application usually does not need major architecture changes.

Vertical scaling tradeoffs:

- It is easy to start with.
- It has a hardware limit.
- Bigger machines become expensive.
- A single machine can still be a single point of failure.

System design insight: vertical scaling is often the first step, but large systems usually need horizontal scaling.

## Horizontal Scaling

- Horizontal scaling means adding more machines.
- Instead of making one server bigger, we run the same service on multiple servers.
- A load balancer distributes traffic across those servers.

Example:

```text
One app server -> Three app servers

Client -> Load Balancer -> App Server 1
                      -> App Server 2
                      -> App Server 3
```

Horizontal scaling tradeoffs:

- It can handle much more traffic.
- It improves availability because one server can fail while others continue serving traffic.
- It requires the application to work correctly across multiple servers.
- Shared state becomes harder to manage.

Important design point:

- Horizontally scaled application servers should usually be stateless.
- Session data, user state and shared data should live in external systems like Redis, databases or object storage (S3).

## Load Balancer Responsibilities

A load balancer usually handles:

- Routing requests to backend servers.
- Checking whether servers are healthy.
- Removing unhealthy servers from traffic rotation.
- Adding new healthy servers back into rotation.
- Optionally terminating TLS/HTTPS.
- Optionally doing request routing based on host, path or headers.

Health check example:

```text
Load Balancer -> GET /health -> App Server
```

If the health check fails repeatedly, the load balancer stops sending traffic to that server.

## Layer 4 Load Balancing (this is very important for interviews - layer 4 vs layer 7 load balancing)

- Layer 4 load balancing works at the transport layer.
- It routes traffic using IP address and port (it looks at IP address, port, TCP/UDP - it does not understand the actual HTTP request).
- It does not deeply inspect HTTP paths, headers or request bodies.
- It can route based on the source IP, destination IP, source port, destination port or protocol (TCP/UDP)

Example:

```text
Client TCP connection -> Load Balancer -> Backend server
```

Layer 4 load balancing is useful when:

- You need very fast routing.
- You are balancing TCP or UDP traffic.
- You do not need application-level routing decisions.

Layer 4 tradeoffs:

- It is fast and simple.
- It has less application awareness.
- It cannot route `/api/orders` and `/api/users` differently based on HTTP path.

## Layer 7 Load Balancing

- Layer 7 load balancing works at the application layer (it understands HTTP/HTTPS)
- It understands protocols like HTTP and HTTPS.
- It can route based on host, path, headers, cookies or other request details (it can inspect URL path, headers, cookies, hostnames, HTTP method, request body sometimes)
- Layer 7 load balancing is smarter than layer 4

Example:

```text
api.example.com/users  -> User Service
api.example.com/orders -> Order Service
```

Layer 7 load balancing is useful when:

- You need path-based routing.
- You need host-based routing.
- APi routing
- You want smarter traffic control.

Layer 7 tradeoffs:

- It is more flexible than Layer 4.
- It has more overhead because it understands application-level data.
- It can become more complex to configure.

### Interview Rule:: Use L4 for simple, fast TCP/UDP routing. Use L7 for HTTP-aware routing and microservices.

## Common Load Balancing Algorithms

### Round Robin

- Requests are sent to servers one by one in order.

Example:

```text
Request 1 -> Server A
Request 2 -> Server B
Request 3 -> Server C
Request 4 -> Server A
```

Tradeoff:

- Simple and common.
- Does not consider server load or request complexity.

### Weighted Round Robin

- Servers get traffic based on assigned weights.
- Bigger or more powerful servers can receive more requests.

Example:

```text
Server A weight = 3
Server B weight = 1

Server A receives about 3x more traffic than Server B.
```

Tradeoff:

- Better than normal round robin when servers have different capacity.
- Still does not always know the real current load.

### Least Connections

- The load balancer sends the next request to the server with the fewest active connections.

Example:

```text
Server A: 20 active connections
Server B: 5 active connections

Next request -> Server B
```

Tradeoff:

- Good when requests have different durations.
- Requires tracking active connections.

### Least Response Time

- The load balancer sends traffic to the server with the best response time and low active load.

Tradeoff:

- More adaptive than round robin.
- Requires measuring server response times.

### IP Hash

- The load balancer uses the client's IP address to choose a backend server.
- The same client usually goes to the same server.

Example:

```text
hash(client_ip) -> Server B
```

Tradeoff:

- Useful for sticky behavior.
- Can create uneven distribution if many users come from the same network or proxy.


## Load Balancer High Availability

The load balancer itself should not become a single point of failure.

Common approach:

```text
Clients -> Primary Load Balancer
        -> Backup Load Balancer
```

In managed cloud systems, this is usually handled by the cloud provider.

System design insight: if you add a load balancer to remove server-level single points of failure, make sure the load balancer is also highly available.

## Quick Comparison

```text
Vertical scaling       -> Make one server bigger
Horizontal scaling     -> Add more servers
Layer 4 load balancing -> Route by IP and port
Layer 7 load balancing -> Route by HTTP details
Round robin            -> Send requests in order
Weighted round robin   -> Send more traffic to stronger servers
Least connections      -> Send traffic to server with fewer active connections
IP hash                -> Route same client to same server
Sticky sessions        -> Keep user attached to same backend
```

Interview answer:

- Start with one server and vertical scaling for simplicity.
- Move to horizontal scaling when traffic grows.
- Put a load balancer in front of stateless application servers.
- Use health checks to avoid unhealthy servers.
- Use Layer 7 load balancing for HTTP APIs when path or host based routing is needed.
- Use Layer 4 load balancing for simpler high-performance TCP/UDP routing.
- Store shared state outside the application server so any server can handle any request.
