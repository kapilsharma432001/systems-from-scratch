### This is for applied AI engineering.
Here over AWS link, something similar has been designed: https://aws.amazon.com/blogs/machine-learning/boosting-rag-based-intelligent-document-assistants-using-entity-extraction-sql-querying-and-agents-with-amazon-bedrock/

## Designing a RAG System for Structured and Unstructured Data

#### Problem Statement

Design an enterprise question-answering system that can answer questions using:

- Structured Data: relational tables with proper columns and relationships
- Unstructured Data: PDFs, DOCX files, Excel Workbooks, text files, scanned documents, and similar sources

The system should be reliable, secure, scalable, and able to answer questions that require information from either or both source types.

#### Functional Requirements

The system should:

- Answer questions from structured data.
- Answer questions from unstructured documents (data).
- Answer questions requiring both.
- Support follow up questions.
- Return citations/sources.

#### Non-functional Requirements

Focus only on the important ones:

- Low Latency: p95 under 8-10 seconds
- Scalability: query and ingestion workloads should scale independently
- Reliable: if the agent/server crashes
- Multi tenant and secure
- Answer should be grounded in evidence


#### Ingestion and Storage Prerequisite

Before the system can answer a question, the source data must be ingested, processed, and stored in a form that the retrieval services can query. Ingestion is therefore a prerequisite for the query-serving path, even though the two workloads should scale independently.

- Structured data is extracted and normalized into PostgreSQL, where the structured query service can retrieve it using SQL.
- Unstructured data is extracted (using OCR when required), chunked, embedded, and indexed in OpenSearch, where the unstructured query service can retrieve it using hybrid search.
- Document metadata such as `document_id`, version, content hash, `tenant_id`, and ingestion status is maintained so that updates are idempotent, traceable, and access-controlled.

The complete ingestion flow—including S3 events, SQS, the ingestion worker, content routing, version handling, and storage—is described in [RAG System Prerequisites: Ingestion Pipeline](003-RAG-systems-prerequisites.md).

Once ingestion is complete, the query orchestrator can retrieve evidence from PostgreSQL, OpenSearch, or both, depending on the question.

Internally the orchestrator is going to interact with 3 main tools:

- `StructuredQueryTool`
- `UnstructuredQueryTool`
- `EvidenceFusionTool`

`EvidenceFusionTool` combines results from the structured and unstructured paths into a single evidence set before sending it to the LLM.

#### High-Level Design

![Initial Version of the High-Level Design](<../drawio-architecture-diagrams/RAG Query Architecture.png>)

> **Note:** This is the initial version of the high-level design. We will refine it as we work through the system.



