## Data Modeling

- A data model describes how your data is structured, stored, and related.
- In practice, it means defining the entities and tables in your data, how you will find them, and how they relate to one another.

![Hello Interview System Design Framework](image.png)

- In the delivery framework, it comes up twice.
    - First, during requirements gathering, you'll identify your core entities.
    - Later, in the high-level design step, you will sketch a basic schema alongside your database component. Include the key fields, relationships, and a note on how you'd index or partition to support the main query patterns.

![A schema design](image-1.png)

### Database Model Options

- Relational Database
    - Almost always the answer in a system design interview.
    - Great at handling complex queries and relationships.
    - Multi-table joins can become performance traps.
    - The usual knock on relational databases is scalability, but that is often exaggerated. Modern SQL databases scale with techniques like **read replicas**, **sharding**, **connection pooling**, and **caching**.
    - PostgreSQL, MySQL, SQLite

- Document Databases - MongoDB
    - Often used because of **schema flexibility**.
    - Stores data as JSON-like documents with flexible schemas, making them good for rapidly evolving applications where you don't know all your field inputs upfront.
    - Your data modeling becomes more about nesting and embedding related information within documents rather than normalizing across tables.
    - **Consider over SQL** when your schema changes frequently.

- Key-value Stores - Redis
    - Provides simple lookup where you fetch values by exact key match.
    - **Consider over SQL** when you need to look up data by a single identifier, such as for caching or session storage. However, "over SQL" is misleading here; in practice, you often use both together.

    ![using relational database and key-value database together](image-2.png)

- Graph Database - Neo4j, Amazon Neptune
    - Stores data as nodes and edges, optimizing for traversing relationships between entities.
    - **When to consider over SQL**: almost never in interviews.

    ![Graph Database](image-3.png)

### Schema Design Fundamentals

#### Entities, Keys, and Relationships

- Once you have identified your core entities, the next step is to map them into tables (or collections) with clear identifiers and relationships.
- For a social media app, you might have `users`, `posts`, `comments`, and `likes`. Each entity needs a **primary key** to uniquely identify records.
- Use system-generated IDs like `user_id` or `post_id` instead of business data like email addresses.

```text
users: id (PK), username, email
posts: id (PK), user_id (FK -> users.id), content, created_at
comments: id (PK), user_id (FK -> users.id), post_id (FK -> posts.id), content
likes: user_id (FK -> users.id), post_id (FK -> posts.id)

Because user_id is a foreign key in posts, a user can have multiple posts. Similarly, because post_id is a foreign key in the comments table, a post can have multiple comments.
```

- This shows the core relationships: each post belongs to one user (posts.user_id), each comment belongs to one post and one user, likes connect users to posts.

- With entities defined, connect them with relationships:-
    - One-to-Many (1:N): a user has many posts, a post has many comments.
    - Many-to-Many (M:N): users like many posts, posts are liked by many users.
    - One-to-One(1:1): this is very rare in practice but often a sign that two tables should just be merged.