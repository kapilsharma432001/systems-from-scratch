### This is for applied AI engineering.

Something similar has been designed in this AWS article: https://aws.amazon.com/blogs/machine-learning/boosting-rag-based-intelligent-document-assistants-using-entity-extraction-sql-querying-and-agents-with-amazon-bedrock/

## Designing a RAG System for Structured and Unstructured Data

#### Problem Statement

Design an enterprise question-answering system that can answer questions using:

- Structured Data: relational tables with proper columns and relationships
- Unstructured Data: PDFs, DOCX files, Excel workbooks, text files, scanned documents, and similar sources

The system should be reliable, secure, scalable, and able to answer questions that require information from either or both source types.

#### Functional Requirements

The system should:

- Answer questions from structured data.
- Answer questions from unstructured documents (data).
- Answer questions requiring both.
- Support follow-up questions.
- Return citations/sources.

#### Non-functional Requirements

Focus only on the important ones:

- Low latency: p95 under 8–10 seconds
- Scalability: query and ingestion workloads should scale independently
- Reliability: recovery if the agent/server crashes
- Security: multi-tenant and secure
- Grounding: answers should be grounded in evidence

> [!NOTE]
> #### Ingestion and Storage Prerequisite
>
> Before the system can answer a question, the source data must be ingested, processed, and stored in a form that the retrieval services can query. Ingestion is therefore a prerequisite for the query-serving path, even though the two workloads should scale independently.
>
> - Structured data is extracted and normalized into PostgreSQL, where the structured query service can retrieve it using SQL.
> - Unstructured data is extracted (using OCR when required), chunked, embedded, and indexed in OpenSearch, where the unstructured query service can retrieve it using hybrid search.
> - Document metadata such as `document_id`, version, content hash, `tenant_id`, and ingestion status is maintained so that updates are idempotent, traceable, and access-controlled.
>
> The complete ingestion flow—including S3 events, SQS, the ingestion worker, content routing, version handling, and storage—is described in [RAG System Prerequisites: Ingestion Pipeline](003-RAG-systems-prerequisites.md).

Once ingestion is complete, the query orchestrator can retrieve evidence from PostgreSQL, OpenSearch, or both, depending on the question.

Internally the orchestrator is going to interact with 3 main tools:

- `StructuredQueryTool`
- `UnstructuredQueryTool`
- `EvidenceFusionTool`

`EvidenceFusionTool` combines results from the structured and unstructured paths into a single evidence set before sending it to the LLM.

#### High-Level Design

![Enterprise RAG Query Flow](<../excalidraw-architecture-diagrams/Enterprise RAG Query Flow.svg>)
![Architecture Diagram](<../drawio-architecture-diagrams/RAG Query Architecture.png>)

##### Query Flow

- Suppose the user asks: Which customers with revenue above 1 crore are complaining about onboarding delays?
- The request enters, and the flow will be something like:
  - User -> API Gateway -> Authentication/Authorization -> Query Orchestrator
  - At this point, we resolve things like `user_id`, `tenant_id`, roles, and `conversation_id`.

###### Query Orchestrator

- This is the brain coordinating everything.
- First, it loads the relevant conversation history, and we can use a NoSQL database like DynamoDB here.
- Then its **planner/router** determines the route (we would be using an LLM in the planner/router):
  - `STRUCTURED_ONLY`: whether we need to have only a structured path (based on the user's query) -> for example, the query is: How many customers purchased product A?
  - `UNSTRUCTURED_ONLY`: whether we need to have only an unstructured path -> for example, the query is: What does our refund policy say?
  - `MIXED_PARALLEL`: whether the unstructured and structured paths can run in parallel -> the query here could be: What was the revenue last year, and what does our refund policy say? -> here, both paths can run in parallel.
  - `MIXED_DEPENDENT`: whether the structured and unstructured paths depend on each other -> for example, the query could be: Find customers earning more than one crore and summarise their complaints.
  - `CLARIFICATION_REQUIRED`

###### Path of Structured Query Service

- Suppose the structured query is: Find the customers with annual revenue above 1 crore.
- The flow is:

```text
Question -> Find the relevant schemas -> Generate SQL -> Validate SQL -> Execute SQL -> Return structured evidence
```

- Finding relevant database schemas means that we don't send the schemas of all 500 tables to the LLM. Instead, we need to maintain a **semantic schema catalog**:

  ![Semantic Schema Catalog](semantic-schema-catalog.png)

- Now, if there is a question, we need to convert that question into an embedding -> then find relevant tables and their columns and send them to the LLM to generate the SQL for us.
- But we do not want to execute that generated SQL directly. We need to validate that SQL:
  - Only `SELECT` (we are doing only "read")
  - It only contains allowed tables and allowed columns
  - The `tenant_id` condition should be present, etc.
- Then it must return a proper JSON response like this:

```json
[
  {
    "customer_id": "C101",
    "customer_name": "ABC Ltd",
    "annual_revenue": 14000000
  },
  {
    "customer_id": "C208",
    "customer_name": "XYZ Ltd",
    "annual_revenue": 12500000
  }
]
```
