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

- Answer natural-language questions from structured data
- Answer questions from PDFs, documents, and Excel files
- Answer questions requiring both structured and unstructured data
- Return citations or source references
- Support conversational follow-up questions

Out of scope:

- Modifying structured data
- Fully autonomous workflows
- Training a foundation model

#### Non-functional Requirements

Focus only on the important ones:

- Low Latency: p95 response within approximately 8-10 seconds
- Scalability: query and ingestion workloads should scale independently
- Reliability: agent execution should survive server crashes
- Security: users should only retrieve authorized rows and documents
- Answer quality: responses should be grounded and cited
- Freshness: structured data should be near real-time; document indexing can be eventually consistent

#### Core Entities

- User
- Conversation
- Data Source
- Documents: represents an uploaded file
- Document chunk: represent the indexed portion of the document
- Query Execution: stores the current agent workflow
- Evidence: represents SQL results or retrieved document chunks
- Agent Checkpoint: enables crash recovery

#### APIs and Interfaces

1. `POST /queries` — Ask a question.
2. `POST /documents` — Upload or register a document.
3. `GET /documents/{document_id}/status` — Check whether ingestion is complete.

Internally the orchestrator is going to interact with 3 main tools:

- `StructuredQueryTool`
- `UnstructuredQueryTool`
- `EvidenceFusionTool`

`EvidenceFusionTool` combines results from the structured and unstructured paths into a single evidence set before sending it to the LLM.

#### High-Level Design

![Initial Version of the High-Level Design](rag-system-architecture.png)

> **Note:** This is the initial version of the high-level design. We will refine it as we work through the system.

- Structured data should be queried using SQL, while unstructured data should be retrieved using hybrid search. An orchestrator decides which path to use. This is the key design principle.
- But there is one check here: both services do not always execute in parallel.
  - **For an independent mixed question, both services can run in parallel.**
    - The meaning of an independent mixed question is—consider this: What was last quarter's revenue, and what does the policy say about refunds?
    - Here, both can run in parallel (the structured query service and the unstructured query service can both run in parallel).
  - But consider: Find customers with revenue above 1 crore and summarise their complaints.
    - Here, the document search depends on customer IDs returned by SQL: **Structured Query -> Get customer IDs -> Document search filtered by customer IDs -> Evidence fusion**.
  - Therefore, here, the orchestrator must generate a small execution plan or DAG, not merely choose one or two services.
  - It should support:
    - STRUCTURED_QUERY
    - UNSTRUCTURED_QUERY
    - MIXED_PARALLEL
    - MIXED_DEPENDENT
    - CLARIFICATION_REQUIRED
