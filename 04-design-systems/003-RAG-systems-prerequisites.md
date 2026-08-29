#### How Does Text Extraction Happen?

- Documents are typically stored in PDF format or as scanned images. They may have simple paragraph layouts or complex tables and may contain digital or handwritten text.
- **To extract information correctly, we need to transform these raw documents into plain text while preserving their original structure.**

- HNSW indexing (but go into detail on this)
- Hashing in case of updates
- What chunking strategy are we going to use?
- What embedding model are we going to use?

#### Ingestion Pipeline

- We won't make ingestion very complex and we will keep it simple.

![File Ingestion Pipeline Architecture](<File Ingestion Pipeline.png>)

- The flow could be something like this:

1. File uploaded/updated to S3
2. S3 sends an event to SQS
3. Ingestion worker picks up the message (we can keep this as AWS Lambda)
4. Checks `document_id` + content hash/version (this is to update the embeddings or create new embeddings—this has been explained later in this Markdown file)
5. Parse the file

    - Extract text
    - Extract tables
    - OCR if required

6. Content router separates the extracted content

    - Structured data goes to the structured data pipeline
        - Structured tables/data -> normalize -> PostgreSQL
    - Unstructured data goes to the unstructured data pipeline
        - Unstructured data (text/tables/notes) -> chunks -> generate embeddings -> OpenSearch (or any vector database)

7. Store/update document metadata:

    - `document_id`
    - `version`
    - `tenant_id`
    - `status`
    - Content hash

8. Mark ingestion complete

Now, if the same document is updated:

- You detect the changed version
- Process the new version
- Generate new embeddings
- Make the new version active
- Remove the old document embeddings

##### The ingestion worker and content router could be the same service; in fact, it's better to keep them as the same service.

For example:

```text
SQS -> Lambda: ingestion_worker()
       - parse_documents()
       - extract_tables()
       - classify_content()
       - process_structured_data()
       - process_unstructured_data()
```

- So 'Content Router' is more of a logical component/function inside the ingestion worker, not necessarily another deployed microservice.
- We can simply deploy SQS -> ingestion Lambda and use the following internally:

```python
def lambda_handler(event):
    document = parse_document(event)

    structured_data = extract_structured_data(document)
    unstructured_data = extract_unstructured_data(document)

    save_structured_data(structured_data)
    save_unstructured_data(unstructured_data)
```

- At large scales, parsing, embedding generation, etc., can be handled by separate workers.

![File Ingestion Pipeline Architecture](<../drawio-architecture-diagrams/File Ingestion Pipeline.png>)
