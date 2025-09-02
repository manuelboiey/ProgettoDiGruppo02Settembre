Tools System
============

The RAG Search Flow includes specialized tools that provide core functionality for document search, web search, and information processing. This section explains how these tools work and how to use them.

Overview
--------

The system includes several specialized tools:

1. **RAG Tool**: Handles medical document search using FAISS
2. **DuckDuckGo Search Tool**: Performs web searches
3. **Utility Tools**: Support functions for text processing and data management

Each tool is designed to work seamlessly with the crewAI framework and can be easily integrated into agent workflows.

RAG Tool
--------

The RAG (Retrieval-Augmented Generation) tool is the core component for searching through local medical documents using vector similarity.

Features
^^^^^^^^

- **Vector Search**: Uses FAISS for fast similarity search
- **Document Chunking**: Intelligent text segmentation for optimal retrieval
- **Medical Focus**: Optimized for medical terminology and concepts
- **Caching**: Efficient storage and retrieval of document embeddings

Implementation
^^^^^^^^^^^^^

The RAG tool is implemented in `src/search_flow/tools/rag.py`:

.. code-block:: python

   class RAGTool(BaseTool):
       name: str = "rag_search_tool"
       description: str = "Search medical documents using vector similarity"
       
       def _run(self, query: str) -> str:
           # Vector search implementation
           # Document retrieval and processing
           # Response generation
           pass

Configuration
^^^^^^^^^^^^

The tool uses several configuration options:

- **FAISS Index Path**: Location of the vector database
- **Document Directory**: Source of medical documents
- **Chunk Size**: Text segmentation parameters
- **Similarity Threshold**: Minimum relevance score for results
- **Max Results**: Maximum number of results to return

Example Configuration:

.. code-block:: yaml

   rag_tool:
     faiss_index_path: "faiss/index.faiss"
     documents_path: "documents/"
     chunk_size: 1000
     similarity_threshold: 0.7
     max_results: 5

Usage Example
^^^^^^^^^^^^

.. code-block:: python

   from search_flow.tools.rag import RAGTool
   
   # Initialize the tool
   rag_tool = RAGTool()
   
   # Search for medical information
   results = rag_tool.run("diabetes symptoms")
   
   # Process results
   print(results)

DuckDuckGo Search Tool
----------------------

The DuckDuckGo search tool provides web search capabilities for general queries.

Features
^^^^^^^^

- **Web Search**: Access to current web information
- **Result Filtering**: Intelligent filtering of search results
- **Content Extraction**: Retrieval of relevant content from web pages
- **Rate Limiting**: Respectful API usage with built-in delays

Implementation
^^^^^^^^^^^^

Located in `src/search_flow/tools/ddg_search.py`:

.. code-block:: python

   class DuckDuckGoSearchTool(BaseTool):
       name: str = "ddg_search_tool"
       description: str = "Search the web using DuckDuckGo"
       
       def _run(self, query: str, max_results: int = 5) -> str:
           # Web search implementation
           # Result filtering and ranking
           # Content extraction
           pass

Configuration
^^^^^^^^^^^^

Configurable parameters include:

- **Max Results**: Maximum number of search results
- **Search Region**: Geographic location for localized results
- **Result Type**: Web, news, images, or mixed results
- **Language**: Search language preference
- **Safe Search**: Content filtering options

Example Configuration:

.. code-block:: yaml

   ddg_search_tool:
     max_results: 5
     search_region: "it-IT"
     result_type: "web"
     language: "it"
     safe_search: true

Usage Example
^^^^^^^^^^^^

.. code-block:: python

   from search_flow.tools.ddg_search import DuckDuckGoSearchTool
   
   # Initialize the tool
   search_tool = DuckDuckGoSearchTool()
   
   # Perform web search
   results = search_tool.run("latest AI technology news", max_results=3)
   
   # Process results
   print(results)

Tool Integration
---------------

Tools are integrated into the crew system through configuration files:

**Agent Configuration:**

.. code-block:: yaml

   document_searcher:
     name: "Medical Document Searcher"
     tools: ["rag_search_tool"]
     # ... other configuration

   web_researcher:
     name: "Web Research Specialist"
     tools: ["ddg_search_tool"]
     # ... other configuration

**Task Configuration:**

.. code-block:: yaml

   document_search_task:
     description: "Search medical documents for relevant information"
     expected_output: "Comprehensive medical information based on query"
     agent: "document_searcher"
     tools: ["rag_search_tool"]

Custom Tool Development
----------------------

You can create custom tools by extending the BaseTool class:

.. code-block:: python

   from crewai.tools import BaseTool
   
   class CustomMedicalTool(BaseTool):
       name: str = "custom_medical_tool"
       description: str = "Custom medical information tool"
       
       def _run(self, query: str, **kwargs) -> str:
           # Your custom implementation here
           # Process the query and return results
           return "Custom medical information"
       
       def _validate_input(self, query: str) -> bool:
           # Validate input parameters
           return len(query.strip()) > 0

Tool Registration
----------------

Custom tools must be registered with the crew system:

1. **Add to Configuration**: Include in agents.yaml
2. **Import in Crew**: Make sure the tool is available
3. **Test Integration**: Verify tool works with agents

Example Registration:

.. code-block:: yaml

   custom_medical_agent:
     name: "Custom Medical Agent"
     tools: ["rag_search_tool", "custom_medical_tool"]
     # ... other configuration

Performance Optimization
-----------------------

**RAG Tool Optimization:**
- Efficient FAISS index management
- Document chunking optimization
- Caching of frequently accessed embeddings
- Parallel processing for large document sets

**Search Tool Optimization:**
- Intelligent result caching
- Efficient content extraction
- Rate limiting and connection pooling
- Result ranking and filtering

**General Optimization:**
- Tool result caching
- Lazy loading of heavy resources
- Memory management for large datasets
- Error handling and retry logic

Error Handling
--------------

Each tool includes comprehensive error handling:

- **Input Validation**: Parameter checking and sanitization
- **API Failures**: Graceful handling of external service issues
- **Resource Errors**: Management of file and database issues
- **Timeout Handling**: Prevention of hanging operations

Example Error Handling:

.. code-block:: python

   def _run(self, query: str) -> str:
       try:
           # Tool implementation
           return results
       except FileNotFoundError:
           return "Error: Document index not found"
       except Exception as e:
           return f"Error: {str(e)}"

Monitoring and Logging
---------------------

Tools provide detailed logging for debugging and monitoring:

- **Operation Logging**: Track tool usage and performance
- **Error Logging**: Capture and log any issues
- **Performance Metrics**: Measure response times and success rates
- **Usage Statistics**: Monitor tool utilization patterns

For detailed API documentation, see the :doc:`api/modules` section.
