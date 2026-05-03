- Core concepts are the fundamental principle and techniques that form the foundation of system design interview.
- These are the technology-agnostic (not tied to any specific technology) that show up across every design problem you'll encounter.
- Before designing anything - we need to understand what caching is, when to shard a database, how networks actually work? Interviewers will assume that you know them and will probe your understanding when you propose using them.


## Networking Essentials
- At high level, networking means how different components of system (servers, clients, services) communicate with each other.
- In system design, every request flows like: Client (browsers/app) -> Internet -> Load Balancer -> Servers -> Databases -> Response back
- So networking effects: Latency (how fast things respond?), Reliablity (does uit fail?), scalability (can it handle millions of users?)
- I cover networking in more detail here: [Networking Essentials](../03-networking-essentials.md).
