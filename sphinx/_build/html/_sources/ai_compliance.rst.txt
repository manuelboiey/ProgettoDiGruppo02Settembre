====================
Model Compliance
====================

**Model Owner:** Manuel Boi and Anna Setzu
**Document Version:** v0.1 (2025-09-01)  
**Reviewers:** TBD  

Overview
--------

**Model Type:** Hybrid AI pipeline (Retrieval-Augmented Generation + Search Orchestration with LLMs)

Model Description
-----------------

**Description:**

This system integrates two modes of answering user queries:

- **RAG (Retrieval-Augmented Generation)** for medical-related questions, leveraging a FAISS vectorstore built on local documents and an Azure OpenAI LLM.
- **Web Search** for general questions, using DuckDuckGo as an external search engine and an agent that summarizes the results.

**Status:** Under Preparation → Regularly Updated  
**Status Date:** 2025-09-01  

**Developers:**

- Manuel Boi – Contributor  
- Anna Setzu – Contributor   

Version Details and Artifacts
-----------------------------

- **Current Model Version:** 0.1  
- **Release Date:** 2025-09-01  
- **Artifacts:**

  - FAISS vectorstore (``/faiss/index.faiss``, ``/faiss/index.pkl``)  
  - Medical knowledge file: ``documents/medicina_generale.txt``  
  - DuckDuckGo search results retrieved via ``ddgs`` package  

Intended and Known Usage
------------------------

**Intended Use:**

- Provide documented answers to medical questions based on a controlled corpus.  
- Perform general web search and summarize results.  

**Domain(s) of Use:**

- General medicine (with controlled sources and citations).  
- Informational searches on the internet.  

**Specific Tasks:**

- Automatic classification of query domain (“medical” vs “other”).  
- Retrieval and generation with citations.  
- Web search followed by summarization.  

**Instructions for Deployers:**

- Ensure Azure environment variables (``AZURE_API_BASE``, ``AZURE_API_KEY``, ``AZURE_API_VERSION``) are configured.  
- Provide valid input documents in the ``documents/`` directory.  
- Use with caution for medical queries → strictly informational, not diagnostic.  

**Out of Scope Uses:**

- Automated medical diagnosis.  
- Clinical decision-making without human supervision.  
- Any high-risk regulated applications without expert review.  

Known Applications
------------------

.. list-table::
   :header-rows: 1

   * - Application
     - Purpose
     - AI Act Risk
   * - Medical Q&A
     - Provide answers from medical documents
     - High
   * - General Search
     - Summarize results from web queries
     - Limited

Model Architecture
------------------

**Description:**

The system is structured as a **CrewAI flow orchestration**:

1. **Query Classification**: An Azure OpenAI LLM determines if the question is medical or general.  
2. **Routing**:  
   - Medical → RAG pipeline (FAISS + Azure OpenAI).  
   - Other → Web search via DuckDuckGo + summarizer agent.  

**Key Components:**

- ``SearchFlow`` orchestrator  
- ``RAG`` tool (FAISS, LangChain, Azure OpenAI)  
- ``DDGSearch`` tool (DuckDuckGo API)  
- ``SearchCrew`` and ``RAGCrew`` to manage agents and tasks  

**Hyperparameter Settings:**

- FAISS retrieval: ``k=5``, ``fetch_k=20``, ``lambda=0.6``  
- Embedding model: ``text-embedding-ada-002``  
- LLM model: ``gpt-4o`` (Azure OpenAI)  

**Training Methodology:**

- No supervised training: embeddings + prompt engineering only.  

**Compute Resources:**

- Azure OpenAI API (cloud-based)  
- Local CPU/GPU for FAISS indexing and query execution  

Data Collection and Preprocessing
--------------------------------

- **Data source:** Local documents (``medicina_generale.txt``).  
- **Cleaning:** Split into chunks (1500 tokens, 300 overlap).  
- **Transformations:** Embedded with Azure OpenAI → FAISS index.  
- **Splitting:** No supervised dataset (no train/val/test split).  

Model Training and Evaluation
-----------------------------

**Objective:**

- Deliver accurate answers with source citations.  
- Summarize web search results effectively.  

**Metrics:**

- Faithfulness  
- Answer relevancy  
- Context precision/recall (via RAGAS)  

**Evaluation:**

- Evaluation results stored in ``ragas_results.csv``.  
- No accuracy/precision metrics (unsupervised pipeline).  

Bias and Fairness Analysis
--------------------------

**Potential Biases:**

- Bias in local medical documents.  
- Bias from web search results (DuckDuckGo).  
- Bias inherited from Azure OpenAI LLM.  

**Mitigation Measures:**

- Always include citations for transparency.  
- Prompt instructions restrict responses to available context.  
- Explicit fallback message: *"Not available in the provided context."*  

Model Interpretability and Explainability
-----------------------------------------

**Techniques Used:**

- Source citations ``[source:FILE]`` in every answer.  
- Transparency in web summarization (raw results + synthesized summary).  
- Evaluation with RAGAS metrics (faithfulness, relevancy).  

EU Declaration of Conformity
----------------------------

**Standards Applied:**

- AI Act Article 11, Annex IV compliance structure.  
- Transparency obligations (citations, limited medical usage scope).  

Documentation Metadata
----------------------

- **Version:** 0.1  
- **Template Version:** AI Act Annex IV  
- **Authors:**
  
  - Manuel Boi – Contributor  
  - Anna Setzu – Contributor  
