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
