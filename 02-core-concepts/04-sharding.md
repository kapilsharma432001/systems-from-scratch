## Sharding

> **Definition:** Sharding is the process of splitting data across multiple machines or databases.

Instead of storing all users in one large database, you can split them across multiple shards:

- **Shard 1:** Users A-H
- **Shard 2:** Users I-P
- **Shard 3:** Users Q-Z

The goal of sharding is to handle more data, more traffic, and more write operations.

### When to Shard

Consider sharding when a single database cannot handle:

- The volume of data
- The number of reads and writes
- Storage requirements
- Hot tables
- High latency caused by large indexes

> 💡 **Interview Tip**
>
> "I would first scale vertically, add read replicas, caching, and indexing. If writes or storage still become bottlenecks, I would shard the database."
>
> This demonstrates maturity: do not jump directly to sharding.

### Choosing a Shard Key

- A shard key determines where data is stored.
- Example: `shard = hash(user_id) % number_of_shards`
- Common shard keys include `user_id`, `tenant_id`, `organization_id`, `region`, and `order_id`.
- A good shard key should have high cardinality, distribute data evenly, appear frequently in queries, and be unlikely to create hot shards.
- **Potentially poor shard key:** `country`, if a few countries such as India or the United States generate significantly more traffic than others. This uneven distribution can create hot shards.

### Main Sharding Strategies

1. **Hash-Based Sharding**
   - Formula: `hash(user_id) % N`
   - Advantage: distributes data evenly.
   - Disadvantage: does not support range queries efficiently.
   - Example use cases: users, posts, and likes.
2. **Range-Based Sharding**
   - `user_id` 1-999,999: Shard 1
   - `user_id` 1,000,000-1,999,999: Shard 2
   - `user_id` 2,000,000-2,999,999: Shard 3
   - Advantage: supports range queries efficiently.
   - Disadvantage: some ranges can become hot. For example, the latest orders may all go to the newest shard.
3. **Geographic Sharding**
   - Users in India: India shard
   - Users in the United States: US shard
   - Users in the European Union: EU shard
   - Advantage: improves latency and helps meet data residency requirements.
   - Disadvantage: makes global queries more difficult.

### Rebalancing Is Painful

- Rebalancing is an important point to discuss in system design interviews.
- When you add a new shard, data may need to move. For example, if you use `hash(user_id) % N` and increase `N` from 4 to 5, many keys will map to different shards.
- **Consistent hashing** reduces the amount of data that must move when shards are added or removed.

> 💡 **Interview Tip**
>
> "I would use consistent hashing or virtual shards to reduce data movement during resharding."

### Hot Shard Problem

- A hot shard receives significantly more traffic than the other shards.
- Example: If you shard by `celebrity_user_id`, all traffic for a celebrity may go to one shard.
- Solutions include choosing a better or composite shard key, caching heavily accessed data, using write queues, and isolating hot users on separate shards.

### Joins Become Harder

- If related data is on different shards, joins become expensive.
- For example, if the `users` table is sharded by `user_id` and the `orders` table is sharded by `order_id`, retrieving a user and their orders may require queries across multiple shards.
- A common solution is to shard related data using the same key:
  - `users` sharded by `user_id`
  - `orders` sharded by `user_id`
  - `payments` sharded by `user_id`
- This approach is called **co-location**.
