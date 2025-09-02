==================================
Application Compliance
==================================

Application Owner
-----------------
Manuel Boi and Anna Setzu

Document Version
----------------
v0.1

Reviewers
---------
TBD



General Information
===================

Purpose and Intended Use
------------------------
The application routes user questions to one of two paths:

* **Medical intent → RAG path**: answer from a local Italian-language general medicine file
  using FAISS retrieval and an Azure OpenAI chat model, with inline source citations in
  the form ``[source:...]``.
* **Other intent → Web search path**: fetch top DuckDuckGo text results and summarize them.

The routing decision is performed by an Azure-backed LLM that returns either
``"medicina"`` or ``"altro"``. The RAG system is constrained to use **only** retrieved
context and explicitly say when information is not present in the context.

Operational Environment
-----------------------
* **Python packages** (as referenced in code): CrewAI (flow/agents/tasks), LangChain,
  FAISS, ddgs (DuckDuckGo), dotenv, Pydantic.
* **External services**: Azure OpenAI (chat + embeddings).
* **Environment variables required** (validated in code): ``AZURE_API_BASE``,
  ``AZURE_API_KEY``, ``AZURE_API_VERSION``.
* **Local artifacts**: single knowledge file under ``documents\medicina_generale.txt`` and
  a persisted FAISS index under ``faiss/``.


Application Functionality
=========================

Instructions for Use for Deployers
----------------------------------
* Provide a local medical knowledge file at ``documents\medicina_generale.txt``.
* Set Azure environment variables: ``AZURE_API_BASE``, ``AZURE_API_KEY``,
  ``AZURE_API_VERSION``.
* Run the interactive flow via ``kickoff()`` (CLI prompt) or generate a diagram via
  ``plot()`` (outputs ``search_flow_diagram.html``).

Model Capabilities and Limitations
----------------------------------
* **Capabilities (medical path)**: retrieval-augmented answers with mandatory
  citations drawn from the local file only; Italian output; explicit fallback when the
  answer is not in the provided context.
* **Capabilities (web path)**: query DuckDuckGo (region ``it-it``, safesearch ``off``,
  max 3 results) and produce a textual summary.
* **Limitations**: no supervised training; answers in the medical path are limited to
  the local document’s content; web summaries depend on third-party search results.

Input Data Requirements
-----------------------
* A **user question** (string). Medical questions trigger the RAG path; other questions
  trigger the web search + summarization path.

Output Explanation
------------------
* **Medical path**: concise Italian answers with inline citations (``[source:FILE]``).
* **Web path**: a textual synthesis of top DuckDuckGo results.

System Architecture Overview
----------------------------
* **Flow orchestration** (CrewAI Flow): ``SearchFlow`` with stages:
  1) detect field (LLM classification: ``"medicina"`` / ``"altro"``);
  2) router;
  3) medical listener → RAG;
  4) non-medical listeners → research (DuckDuckGo) → summarization.
* **Agents/Crews**:
  * ``SearchCrew``: researcher (uses DuckDuckGo tool) and resumer (summarizer).
* **Tools**:
  * ``RAG``: FAISS + Azure OpenAI (chat + embeddings).
  * ``DDGSearch``: DuckDuckGo text search via ``ddgs``.


Models and Datasets
===================

Models
------
* **Routing LLM**: Azure model identifier ``azure/gpt-4o-mini`` (via CrewAI LLM).
* **RAG chat model**: Azure OpenAI chat, deployment name ``gpt-4o``.
* **Embeddings**: Azure OpenAI embeddings, model ``text-embedding-ada-002``.

Datasets
--------
* **Local knowledge file (Italian)**: ``documents\medicina_generale._*
