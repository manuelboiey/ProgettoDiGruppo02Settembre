Search Flow Architecture
========================

The RAG Search Flow is the core orchestration system that intelligently routes user queries between different search mechanisms. This section explains the architecture, components, and how they work together.

Overview
--------

The Search Flow implements a state machine pattern using the `crewAI Flow <https://docs.crewai.com/how-to/flows/>`_ framework. It automatically detects user intent and routes queries to the most appropriate search mechanism:

- **Medical Queries** → RAG Document Search
- **General Queries** → Web Search + Summarization

Architecture Diagram
-------------------

.. code-block:: text

   User Input
        ↓
   [Intent Detection]
        ↓
   ┌─────────────────┐    ┌─────────────────┐
   │   Medical Query │    │  General Query  │
   │        ↓        │    │        ↓        │
   │   RAG Crew      │    │  Search Crew    │
   │   (FAISS + AI)  │    │ (DuckDuckGo +   │
   │        ↓        │    │  Summarization) │
   │  Local Docs     │    │        ↓        │
   │   Results       │    │  Web Results    │
   └─────────────────┘    └─────────────────┘
        ↓                        ↓
   ┌─────────────────────────────────────────┐
   │           Combined Output               │
   └─────────────────────────────────────────┘

Core Components
---------------

SearchState
^^^^^^^^^^

The central state object that maintains information throughout the search process:

.. code-block:: python

   class SearchState(BaseModel):
       question: str = ""      # User's original question
       type: str = ""          # Detected intent ("medicina" or "altro")
       result: str = ""        # RAG search results
       raw_results: str = ""   # Raw web search results
       summary: str = ""       # Summarized web results

SearchFlow
^^^^^^^^^^

The main flow orchestrator that manages the entire search process:

.. code-block:: python

   class SearchFlow(Flow[SearchState]):
       rag_crew = RAGCrew()        # Handles medical document search
       search_crew = SearchCrew()  # Handles web search

Flow Steps
----------

1. **Intent Detection** (`detect_field`)
   - Prompts user for input
   - Uses AI to classify query as medical or general
   - Updates state with question and detected type

2. **Routing** (`route_field`)
   - Routes to appropriate search mechanism based on intent
   - Returns route identifier for flow control

3. **Medical Search** (`rag`)
   - Executes when route is "medicina"
   - Uses RAG crew to search local medical documents
   - Updates state with document search results

4. **Web Search** (`run_research`)
   - Executes when route is "altro"
   - Uses search crew to perform web search
   - Summarizes results and updates state

Intent Detection
---------------

The system uses a sophisticated AI model to automatically detect query intent:

.. code-block:: python

   @start()
   def detect_field(self):
       self.state.question = input("Chiedimi quello che vuoi!\n> ")
       
       llm = LLM(model="azure/gpt-4o-mini")
       messages = [
           {
               "role": "system",
               "content": (
                   "Sei un assistente che capisce se l'utente ti sta facendo una domanda "
                   "relativa al campo della medicina, oppure qualche altro campo. Se è relativo "
                   "alla medicina, rispondi solo 'medicina', altrimenti rispondi solo 'altro'."
               ),
           },
           {"role": "user", "content": self.state.question},
       ]
       
       self.state.type = llm.call(messages)
       return self.state

The AI model is trained to recognize:
- **Medical terms**: symptoms, diseases, treatments, medications
- **Medical contexts**: health, wellness, diagnosis, prognosis
- **General queries**: news, weather, recipes, technology, etc.

Routing Logic
-------------

The routing system uses the detected intent to determine the search path:

.. code-block:: python

   @router(detect_field)
   def route_field(self):
       if self.state.type.lower() == "medicina":
           return 'medicina'
       if self.state.type.lower() == "altro":
           return 'altro'
       print("\n⚠️ Non ho capito cosa vuoi fare.")
       return None

This ensures that:
- Medical queries go to the RAG system for document search
- General queries go to the web search system
- Unclear queries are handled gracefully with user feedback

State Management
---------------

The SearchState object maintains consistency throughout the flow:

- **Immutable updates**: Each step returns a new state
- **Context preservation**: Previous results are maintained
- **Flow control**: State determines which routes are available

Error Handling
--------------

The system includes robust error handling:

- **Intent detection failures**: Graceful fallback with user feedback
- **Search failures**: Error messages and retry options
- **API failures**: Connection timeout handling
- **Invalid inputs**: Input validation and sanitization

Performance Considerations
-------------------------

- **Async operations**: Non-blocking search operations
- **Caching**: FAISS index for fast document retrieval
- **Resource management**: Efficient memory usage for large document sets
- **Timeout handling**: Prevents hanging on slow operations

Extending the Flow
------------------

The flow architecture is designed for extensibility:

1. **Add new intent types**: Extend the detection logic
2. **New search mechanisms**: Add new crews and routes
3. **Custom state fields**: Extend SearchState with new attributes
4. **Middleware**: Add pre/post-processing steps

Example extension:

.. code-block:: python

   @listen('specialized')
   def specialized_search(self):
       """Custom search for specialized domains."""
       # Add your custom search logic here
       return self.state

Integration Points
-----------------

The Search Flow integrates with:

- **RAG Crew**: For medical document search
- **Search Crew**: For web search and summarization
- **External APIs**: OpenAI, Azure, DuckDuckGo
- **Document Systems**: FAISS vector database
- **User Interfaces**: Command line, web, or API endpoints

For detailed implementation, see the :doc:`api/modules` section.
