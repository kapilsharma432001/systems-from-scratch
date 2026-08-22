## SQL vs. NoSQL

- SQL databases are relational and table-based, and they use a fixed schema.
- NoSQL databases are non-relational, document-based or key-value-based, and typically use a flexible schema.

For a system design interview, we need to understand the trade-offs involving data models, consistency, transactions, scalability, availability, query patterns, and concurrency.

### Main Difference

![Core difference between SQL and NoSQL databases](image-17.png)

### When Should We Use SQL?

Use SQL when the data has strong relationships, such as:

```text
Users -> Orders -> Order Items -> Products
```

SQL is also a natural choice when queries frequently require joins:

```sql
SELECT ...
FROM orders
JOIN users ON ...
JOIN products ON ...;
```

Another reason to use SQL is when the system requires strong transactional guarantees. Consider a transfer of ₹1,000 from Account A to Account B:

```text
Account A: -₹1,000
Account B: +₹1,000
```

Both operations must happen, or neither should happen:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 'A';

UPDATE accounts
SET balance = balance + 1000
WHERE account_id = 'B';

COMMIT;
```

If either operation fails, the transaction is rolled back. This behavior is supported by ACID guarantees.

> [!NOTE]
> ### ACID Properties
>
> **ACID** stands for **Atomicity, Consistency, Isolation, and Durability**. These four properties make database transactions reliable and safe, especially when multiple operations or users are involved.
>
> A transaction is a group of database operations treated as one logical unit. For example, transferring ₹1,000 from Account A to Account B involves deducting ₹1,000 from Account A and depositing ₹1,000 into Account B. ACID helps ensure that this transaction happens correctly.
>
> #### 1. Atomicity
>
> - Either every operation in a transaction succeeds, or none of the operations are applied.
> - **All or nothing.**
>
> ![Atomic transaction](<atomic transaction.png>)
>
> #### 2. Consistency
>
> A transaction must move the database from one valid state to another while respecting all constraints and business rules.
>
> Suppose the following rule applies:
>
> ```text
> balance >= 0
> ```
>
> If Account A has ₹500 and someone tries to transfer ₹1,000, the operation should fail when overdrafts are not allowed.
>
> Other consistency rules include:
>
> - `PRIMARY KEY`
> - `FOREIGN KEY`
> - `UNIQUE`
> - `NOT NULL`
> - `CHECK` constraints
>
> For example:
>
> ```sql
> age INTEGER CHECK (age >= 18)
> ```
>
> The database should reject a value such as `age = 15` because it violates the constraint.
>
> **Consistency ensures that all database constraints and integrity rules remain satisfied before and after a transaction.**
>
> #### 3. Isolation
>
> Many transactions may run at the same time, but they should behave as though they were executing in isolation from one another.
>
> Imagine that an account has a balance of ₹10,000 and two transactions simultaneously attempt to withdraw ₹7,000:
>
> 1. Transaction 1 reads the ₹10,000 balance.
> 2. Transaction 2 also reads the ₹10,000 balance.
> 3. Transaction 1 withdraws ₹7,000.
> 4. Transaction 2 also withdraws ₹7,000.
>
> Without proper isolation, both transactions may incorrectly conclude that enough money is available.
>
> Isolation helps prevent concurrency problems such as:
>
> - **Dirty read:** Reading uncommitted data.
> - **Non-repeatable read:** Reading the same row twice but receiving different values.
> - **Lost update:** One transaction overwrites another transaction's update.
>
> ##### Locks and Isolation
>
> One common mechanism databases use to provide isolation is locking. Locks can be acquired on rows, tables, or pages (groups of rows).
>
> The two basic lock types are:
>
> - **Shared lock (S):** Used when a transaction reads data; multiple readers can usually coexist.
> - **Exclusive lock (X):** Used when a transaction modifies data; other conflicting reads or writes may have to wait.
>
> #### 4. Durability
>
> Durability means that once a transaction is committed, it remains committed. The committed data survives failures such as an application crash or a database restart.
