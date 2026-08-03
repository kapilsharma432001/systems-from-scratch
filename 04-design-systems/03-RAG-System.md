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

1. `POST /queries`
2. `POST /documents`
3. `GET /documents/{document_id}/status`

Internally the orchestrator is going to interact with 3 main tools:

- `StructuredQueryTool`
- `UnstructuredQueryTool`
- `EvidenceFusionTool`

EvidenceFusionTool combines the result coming from structured or unstructured paths into one clean evidence set before sending it to LLM.

#### High Level Design

- Structured data should be queries using SQL. Unstructured data should be retrived using hybrid search. An orchestrator will decide which path to choose.
