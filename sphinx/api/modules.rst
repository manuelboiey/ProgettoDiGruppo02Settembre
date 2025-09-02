API Reference
============

This section provides detailed API documentation for all modules, classes, and functions in the RAG Search Flow system.

.. toctree::
   :maxdepth: 2
   :caption: Core Modules:

   search_flow
   crews
   tools

Search Flow Module
------------------

.. automodule:: search_flow.main
   :members:
   :undoc-members:
   :show-inheritance:

Search State
^^^^^^^^^^^

.. autoclass:: search_flow.main.SearchState
   :members:
   :undoc-members:
   :show-inheritance:

Search Flow
^^^^^^^^^^

.. autoclass:: search_flow.main.SearchFlow
   :members:
   :undoc-members:
   :show-inheritance:

Crews Module
------------

RAG Crew
^^^^^^^^

.. automodule:: search_flow.crews.rag_crew.rag_crew
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: search_flow.crews.rag_crew.rag_crew.RAGCrew
   :members:
   :undoc-members:
   :show-inheritance:

Search Crew
^^^^^^^^^^^

.. automodule:: search_flow.crews.search_crew.search_crew
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: search_flow.crews.search_crew.search_crew.SearchCrew
   :members:
   :undoc-members:
   :show-inheritance:

Tools Module
------------

RAG Tool
^^^^^^^^

.. automodule:: search_flow.tools.rag
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: search_flow.tools.rag.RAGTool
   :members:
   :undoc-members:
   :show-inheritance:

DuckDuckGo Search Tool
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: search_flow.tools.ddg_search
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: search_flow.tools.ddg_search.DuckDuckGoSearchTool
   :members:
   :undoc-members:
   :show-inheritance:

Utility Functions
----------------

.. automodule:: search_flow.crews.utils
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Loading
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: search_flow.crews.utils.load_config

Agent Creation
^^^^^^^^^^^^^

.. autofunction:: search_flow.crews.utils.create_agent

Task Creation
^^^^^^^^^^^^

.. autofunction:: search_flow.crews.utils.create_task

Class Diagrams
--------------

Search Flow Architecture
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   SearchFlow
   ├── SearchState
   ├── RAGCrew
   │   ├── document_searcher()
   │   ├── medical_expert()
   │   └── document_search_task()
   └── SearchCrew
       ├── web_researcher()
       ├── information_analyst()
       └── web_search_task()

Tool Hierarchy
^^^^^^^^^^^^^

.. code-block:: text

   BaseTool
   ├── RAGTool
   │   ├── _run(query: str) -> str
   │   └── _validate_input(query: str) -> bool
   └── DuckDuckGoSearchTool
       ├── _run(query: str, max_results: int) -> str
       └── _validate_input(query: str) -> bool

Method Reference
----------------

SearchFlow Methods
^^^^^^^^^^^^^^^^^

.. automethod:: search_flow.main.SearchFlow.detect_field
   :noindex:

.. automethod:: search_flow.main.SearchFlow.route_field
   :noindex:

.. automethod:: search_flow.main.SearchFlow.rag
   :noindex:

.. automethod:: search_flow.main.SearchFlow.run_research
   :noindex:

RAGTool Methods
^^^^^^^^^^^^^^

.. automethod:: search_flow.tools.rag.RAGTool._run
   :noindex:

.. automethod:: search_flow.tools.rag.RAGTool._validate_input
   :noindex:

DuckDuckGoSearchTool Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: search_flow.tools.ddg_search.DuckDuckGoSearchTool._run
   :noindex:

.. automethod:: search_flow.tools.ddg_search.DuckDuckGoSearchTool._validate_input
   :noindex:

Data Models
-----------

SearchState Fields
^^^^^^^^^^^^^^^^^

.. autodata:: search_flow.main.SearchState.question
   :noindex:

.. autodata:: search_flow.main.SearchState.type
   :noindex:

.. autodata:: search_flow.main.SearchState.result
   :noindex:

.. autodata:: search_flow.main.SearchState.raw_results
   :noindex:

.. autodata:: search_flow.main.SearchState.summary
   :noindex:

Configuration Schemas
--------------------

Agent Configuration Schema
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   agent_name:
     name: str                    # Human-readable name
     role: str                    # Agent's role description
     goal: str                    # What the agent aims to accomplish
     backstory: str               # Agent's background and expertise
     verbose: bool                # Whether to provide detailed output
     allow_delegation: bool       # Whether agent can delegate tasks
     tools: List[str]             # List of tool names
     memory: bool                 # Whether agent maintains memory
     max_iter: Optional[int]      # Maximum reasoning iterations

Task Configuration Schema
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   task_name:
     description: str             # What the task accomplishes
     expected_output: str         # Format and content of expected results
     agent: str                   # Name of the assigned agent
     tools: List[str]             # List of required tool names
     context: Optional[str]       # Additional context or requirements
     async_execution: bool        # Whether task can run asynchronously
     max_iter: Optional[int]      # Maximum reasoning iterations

Error Handling
--------------

Common Exceptions
^^^^^^^^^^^^^^^^

.. autoexception:: search_flow.tools.rag.DocumentIndexError
   :noindex:

.. autoexception:: search_flow.tools.rag.SearchError
   :noindex:

.. autoexception:: search_flow.tools.ddg_search.SearchError
   :noindex:

.. autoexception:: search_flow.tools.ddg_search.RateLimitError
   :noindex:

Error Handling Patterns
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   try:
       result = tool.run(query)
   except DocumentIndexError:
       # Handle missing or corrupted document index
       result = "Error: Document index not available"
   except SearchError as e:
       # Handle general search errors
       result = f"Search error: {str(e)}"
   except Exception as e:
       # Handle unexpected errors
       result = f"Unexpected error: {str(e)}"

Logging and Debugging
---------------------

Logging Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import logging
   
   # Configure logging for the search flow
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   
   # Get logger for specific module
   logger = logging.getLogger('search_flow.tools.rag')

Debug Information
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Enable verbose mode for debugging
   agent = Agent(
       name="Debug Agent",
       verbose=True,  # Provides detailed output
       # ... other configuration
   )
   
   # Enable debug logging
   logging.getLogger('search_flow').setLevel(logging.DEBUG)

Performance Monitoring
---------------------

Timing Decorators
^^^^^^^^^^^^^^^^

.. code-block:: python

   import time
   from functools import wraps
   
   def timing_decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           start_time = time.time()
           result = func(*args, **kwargs)
           end_time = time.time()
           print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
           return result
       return wrapper
   
   @timing_decorator
   def search_function(query):
       # Search implementation
       pass

Memory Usage Monitoring
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import psutil
   import os
   
   def get_memory_usage():
       process = psutil.Process(os.getpid())
       return process.memory_info().rss / 1024 / 1024  # MB
   
   # Monitor memory before and after operations
   memory_before = get_memory_usage()
   # ... perform operation ...
   memory_after = get_memory_usage()
   print(f"Memory used: {memory_after - memory_before:.2f} MB")

Testing and Validation
---------------------

Unit Testing
^^^^^^^^^^^

.. code-block:: python

   import unittest
   from search_flow.tools.rag import RAGTool
   
   class TestRAGTool(unittest.TestCase):
       def setUp(self):
           self.rag_tool = RAGTool()
       
       def test_search_functionality(self):
           result = self.rag_tool.run("test query")
           self.assertIsInstance(result, str)
           self.assertGreater(len(result), 0)
   
   if __name__ == '__main__':
       unittest.main()

Integration Testing
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def test_search_flow_integration():
       """Test the complete search flow integration."""
       flow = SearchFlow()
       
       # Test medical query
       flow.state.question = "What are diabetes symptoms?"
       result = flow.detect_field()
       assert result.type == "medicina"
       
       # Test general query
       flow.state.question = "What's the weather like?"
       result = flow.detect_field()
       assert result.type == "altro"

Mock Testing
^^^^^^^^^^^

.. code-block:: python

   from unittest.mock import Mock, patch
   
   def test_rag_tool_with_mock():
       with patch('search_flow.tools.rag.faiss') as mock_faiss:
           mock_faiss.read_index.return_value = Mock()
           
           rag_tool = RAGTool()
           result = rag_tool.run("test query")
           
           mock_faiss.read_index.assert_called_once()

For more examples and usage patterns, see the :doc:`examples` section.
