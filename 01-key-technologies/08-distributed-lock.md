## What are distributed locks and when should you use them?

- When you are dealing with online systems like Ticketmaster, you need a way to lock a resource, like a concert ticket, for a short time (~10 minutes in this case).
- This ensures that while one user is in the middle of buying a ticket, no one else can grab it.
- Traditional databases with ACID properties use transaction locks to keep data consistent, which is great for ensuring that while one user is updating a record, no one else can update it. However, they are not designed for longer-term locking. This is where distributed locks come in handy.

### When to use distributed locks

- They are useful when you need to lock something across different systems or processes for a reasonable period of time.
- They are often implemented using a distributed key-value store like Redis or ZooKeeper.
- For example, if you have a Redis instance and want to lock `ticket-123`, a process can create the `ticket-123` key only if it does not already exist. If another process tries to create the same key, it will fail because the lock is already held.
- Once the first process is done with the lock, it can release the lock by removing the `ticket-123` key, and another process can acquire it.

### Expiration

Another handy feature of distributed locks is that they can be set to expire after a certain amount of time. This makes sure that the lock does not get stuck in a locked state if a process crashes or is killed.

#### Common examples

1. **E-commerce Checkout System:**
2. **Ride-Sharing Management System:** A distributed lock could be used here to store the assignment of drivers to riders. For example, locking a driver prevents them from being matched with multiple riders simultaneously. This lock can be held until the driver accepts or declines the ride, or until a certain amount of time has passed.

#### Other common examples

Payment processing, inventory reservation, ticket booking, cron jobs running on multiple servers, etc.
