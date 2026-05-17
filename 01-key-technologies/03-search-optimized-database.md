## Search Optimized Database

### What is search optimized database and when should you use it?

- Sometimes you're asked with implementing **full-text search** as a feature for your design.
- Full-text search is the ability to search through a large amount of text data and find relevant results.
- This is different from a traditional database query, which is usually based on exact matches or ranges. Without a search optimized database, you will write a query that will look something like this:

```sql
SELECT * FROM documents WHERE document_text LIKE '%search_term%'
```

- This query is slow and ineffiecient and it does not scale well because it requires a full table scan. That means the database has to grab each record and test it against your predicate rather than relying on an index or lookup. Slow!

- **Search Optimized Database** on the other hand, are specifically designed to handle full-text search. They use techniques like indexing, tokenization, stemming to make search queries fast and effiecient.

- In short, they work by building what are called **inverted indexes**. Inverted indexes are a data structure that maps the words to the documents that contain them. This allows you to quickly find documents that contain a given word. A simple example of an inverted index might look like this:

```json
{
    "word1": ["doc1", "doc2", "doc3"],
    "word2": ["doc2", "doc3", "doc4"],
    "word3": ["doc1", "doc3", "doc4"]
}
```

- Now instead of searching the entire table, the database can quickly look up the word in the query and find all matching documents. Fast!
