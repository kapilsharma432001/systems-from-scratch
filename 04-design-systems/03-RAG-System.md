### This is for applied AI engineering.

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
