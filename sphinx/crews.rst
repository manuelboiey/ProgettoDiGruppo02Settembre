Crews System
============

The RAG Search Flow uses a multi-agent crew system built on the `crewAI <https://crewai.com>`_ framework. This section explains how the different crews work together to provide intelligent search capabilities.

Overview
--------

The system consists of two main crews that specialize in different types of search:

1. **RAG Crew**: Handles medical document search using vector similarity
2. **Search Crew**: Manages web search and result summarization

Each crew is composed of specialized agents that work together to accomplish specific tasks.

RAG Crew
--------

The RAG (Retrieval-Augmented Generation) Crew specializes in searching through local medical documents using vector similarity and AI-powered retrieval.

Components
^^^^^^^^^^

**Agent:**
- **document_searcher**: Document consultant (Consultatore di documenti)

**Task:**
- **document_search_task**: Consults documents and responds to user questions

**Configuration:**
- Located in `src/search_flow/crews/rag_crew/config/agents.yaml`
- Located in `src/search_flow/crews/rag_crew/config/tasks.yaml`

Actual RAG Crew Configuration:

.. code-block:: yaml

   # agents.yaml
   document_searcher:
     role: "Consultatore di documenti"
     goal: "Consultare i documenti forniti tramite il tool e rispondere alle domande dell'utente"
     backstory: >
       Sei molto bravo a usare il tool per cercare ciò che l'utente chiede, e rispondi in modo chiaro e conciso.
     llm: azure/gpt-4o-mini

   # tasks.yaml
   document_search_task:
     description: >
       Consulta i documenti forniti tramite il tool e rispondi alle domande dell'utente.
     expected_output: >
       Risposta chiara e concisa basata sui documenti trovati.
     agent: document_searcher

Workflow
^^^^^^^^

1. **Document Consultation**: Uses the RAG tool to search through medical documents
2. **Question Processing**: Analyzes user questions and retrieves relevant information
3. **Response Generation**: Provides clear and concise answers based on found documents

Search Crew
-----------

The Search Crew handles general web searches and result summarization for non-medical queries.

Components
^^^^^^^^^^

**Agents:**
- **researcher**: Web Researcher - searches topics on the internet
- **resumer**: Resume Writer - summarizes search results

**Tasks:**
- **research_task**: Uses search tool to find information and shows top 3 results
- **resume_task**: Summarizes research results into concise text

**Configuration:**
- Located in `src/search_flow/crews/search_crew/config/agents.yaml`
- Located in `src/search_flow/crews/search_crew/config/tasks.yaml`

Actual Search Crew Configuration:

.. code-block:: yaml

   # agents.yaml
   researcher:
     role: "Web Researcher"
     goal: "Cercare un argomento su internet e riassumere i primi 3 risultati"
     backstory: >
       Sei un ricercatore esperto: cerchi informazioni su DuckDuckGo.
     llm: azure/gpt-4o-mini

   resumer:
     role: "Resume Writer"
     goal: "Riassumere risultati ricevuti da internet in un testo conciso"
     backstory: >
       Riassimi i risultati di una ricerca web in un testo conciso.
     llm: azure/gpt-4o-mini

   # tasks.yaml
   research_task:
     description: >
       Usa il tool di ricerca per trovare informazioni su "{topic}".
       Mostra i primi 3 risultati con titolo, url e snippet.
     expected_output: >
       Elenco dei 3 risultati principali.
     agent: researcher

   resume_task:
     description: >
       Riassumi i risultati della ricerca in un testo conciso.
     expected_output: >
       Riassunto della ricerca.
     agent: resumer

Workflow
^^^^^^^^

1. **Web Search**: The researcher agent performs searches using DuckDuckGo
2. **Result Collection**: Gathers the top 3 search results with title, URL, and snippet
3. **Summarization**: The resumer agent creates a concise summary of the research results

Crew Collaboration
-----------------

The crews are orchestrated by `SearchFlow` using a router. For each query, only one branch runs and specific `SearchState` fields are updated:

- "medicina" → `rag()` runs `document_search_task` → updates `state.result`
- "altro" → `run_research()` runs `research_task` → updates `state.raw_results` → `run_summary()` runs `resume_task` → updates `state.summary`

.. code-block:: text

   User Query
        ↓
   start: detect_field
        ↓
   router: route_field
        ↓ medicina                         ↓ altro
   listen('medicina'): rag            listen('altro'): run_research
        ↓                                   ↓
   state.result                         state.raw_results
                                              ↓
                           listen(run_research): run_summary
                                              ↓
                                         state.summary

Agent Communication
------------------

Within each crew, agents work sequentially:

**RAG Crew:**
- The `document_searcher` agent handles the `document_search_task`
- Uses the RAG tool to search through medical documents
- Returns clear and concise responses based on found documents

**Search Crew:**
- The `researcher` agent performs the `research_task`
- Searches the web and returns the top 3 results
- The `resumer` agent then performs the `resume_task`
- Takes the research results and creates a concise summary

Customizing Crews
-----------------

You can customize crew behavior by modifying the configuration files:

**Agent Customization:**
- Modify agent roles and goals in the `agents.yaml` files
- Customize agent backstories 
- Change the LLM model (currently using `azure/gpt-4o-mini`)

**Task Customization:**
- Modify task descriptions in the `tasks.yaml` files
- Adjust expected outputs
- Customize the agent assigned to each task

**Configuration Files:**
- `src/search_flow/crews/rag_crew/config/agents.yaml` - RAG crew agents
- `src/search_flow/crews/rag_crew/config/tasks.yaml` - RAG crew tasks
- `src/search_flow/crews/search_crew/config/agents.yaml` - Search crew agents  
- `src/search_flow/crews/search_crew/config/tasks.yaml` - Search crew tasks

For detailed configuration options, see the :doc:`configuration` section.
