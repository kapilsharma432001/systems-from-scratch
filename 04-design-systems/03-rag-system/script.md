Intro
    - We will cover :-
        - what does it mean by golden dataset
        - deterministic evaluation,
        - LLM-as-a-judge and
        - RAGAS
    - What RAG evaluation is? RAG evaluation is the process of measuring how well a RAG system retrieves the right information and uses it to generate a correct, relevant, and grounded answer.
    - Most important thing is we do not only evaluate the final answer, we eveluate our RAG pipeline at different stages.
    - One simple example throughout this video for understanding.
    - HR chatbot

Explain golden dataset with proper example
{
    'question': 'how many casual leaves do employee get every year?'
    'expected_answer': 'Employee receive 12 casual leaves per year.'
    'expected_citation': ['leave_chunk_8', 'leave_chunk_10']
}
- CI/CD pipeline
- We can start with normal 50-100 questios in the starting and later we can production faolures, ambigous questions, unanswerable questions, hard-retrieval questions, new features, new document types when product evolves etc
Explain deterministic evaluation
- Using normal code/rules for the evaluation.
- We mainly use it where we already know what correct means.
- We can use it for:-

A. Retrieval Evaluation
B. Exact answer evaluation
    - mainly for structured query answers
C. for citation validation
