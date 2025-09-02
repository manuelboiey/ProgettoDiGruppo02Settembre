Development Guide
=================

This section provides comprehensive guidance for developers who want to extend, modify, or contribute to the RAG Search Flow system.

Development Environment Setup
----------------------------

Prerequisites
^^^^^^^^^^^^

- **Python**: 3.10+ (but < 3.14)
- **Git**: For version control
- **UV**: For dependency management
- **IDE**: VS Code, PyCharm, or similar with Python support

Initial Setup
^^^^^^^^^^^^

1. **Clone the Repository**

   .. code-block:: bash

      git clone <repository-url>
      cd rag_search

2. **Create Virtual Environment**

   .. code-block:: bash

      python -m venv venv
      
      # Activate on Windows
      venv\Scripts\activate
      
      # Activate on macOS/Linux
      source venv/bin/activate

3. **Install Dependencies**

   .. code-block:: bash

      uv sync
      # or
      pip install -e .

4. **Install Development Dependencies**

   .. code-block:: bash

      pip install -e ".[dev]"
      pip install pytest pytest-cov black isort mypy

5. **Install Pre-commit Hooks**

   .. code-block:: bash

      pre-commit install

Project Structure
----------------

.. code-block:: text

   rag_search/
   ├── src/
   │   └── search_flow/
   │       ├── __init__.py
   │       ├── main.py              # Main flow orchestration
   │       ├── crews/               # Agent crew implementations
   │       │   ├── __init__.py
   │       │   ├── rag_crew/        # Medical document search crew
   │       │   │   ├── __init__.py
   │       │   │   ├── rag_crew.py
   │       │   │   └── config/      # YAML configuration files
   │       │   │       ├── agents.yaml
   │       │   │       └── tasks.yaml
   │       │   └── search_crew/     # Web search crew
   │       │       ├── __init__.py
   │       │       ├── search_crew.py
   │       │       └── config/
   │       │           ├── agents.yaml
   │       │           └── tasks.yaml
   │       ├── tools/               # Tool implementations
   │       │   ├── __init__.py
   │       │   ├── rag.py          # RAG search tool
   │       │   └── ddg_search.py   # DuckDuckGo search tool
   │       └── utils.py            # Utility functions
   ├── documents/                  # Medical documents for RAG
   ├── faiss/                     # FAISS vector database
   ├── tests/                     # Test suite
   ├── docs/                      # Documentation
   ├── config/                    # Configuration files
   ├── pyproject.toml            # Project configuration
   └── README.md                 # Project overview

Code Style and Standards
------------------------

Python Style Guide
^^^^^^^^^^^^^^^^^

The project follows PEP 8 with some modifications:

- **Line Length**: 120 characters maximum
- **Import Order**: Standard library, third-party, local
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style docstrings for all public functions

Code Formatting
^^^^^^^^^^^^^^

Use the provided tools for consistent formatting:

.. code-block:: bash

   # Format code with black
   black src/ tests/
   
   # Sort imports with isort
   isort src/ tests/
   
   # Check types with mypy
   mypy src/

Example Code Style:

.. code-block:: python

   """RAG Search Tool implementation.
   
   This module provides the RAGTool class for searching medical documents
   using vector similarity search with FAISS.
   """
   
   from typing import Optional, List
   import faiss
   from crewai.tools import BaseTool
   
   
   class RAGTool(BaseTool):
       """Tool for searching medical documents using RAG."""
       
       name: str = "rag_search_tool"
       description: str = "Search medical documents using vector similarity"
       
       def _run(self, query: str) -> str:
           """Execute the RAG search.
           
           Args:
               query: The search query string.
               
           Returns:
               Search results as a formatted string.
               
           Raises:
               DocumentIndexError: If the document index is not available.
               SearchError: If the search operation fails.
           """
           if not self._validate_input(query):
               raise ValueError("Invalid query input")
           
           try:
               # Implementation here
               return "Search results"
           except Exception as e:
               raise SearchError(f"Search failed: {e}")
       
       def _validate_input(self, query: str) -> bool:
           """Validate the input query.
           
           Args:
               query: The query to validate.
               
           Returns:
               True if valid, False otherwise.
           """
           return isinstance(query, str) and len(query.strip()) > 0

Testing Guidelines
------------------

Test Structure
^^^^^^^^^^^^^

Tests should be organized to mirror the source code structure:

.. code-block:: text

   tests/
   ├── __init__.py
   ├── conftest.py              # Shared fixtures
   ├── unit/                    # Unit tests
   │   ├── __init__.py
   │   ├── test_main.py
   │   ├── test_rag_crew.py
   │   ├── test_search_crew.py
   │   └── test_tools.py
   ├── integration/             # Integration tests
   │   ├── __init__.py
   │   ├── test_flow.py
   │   └── test_crews.py
   └── fixtures/                # Test data and fixtures
       ├── sample_documents/
       └── test_configs/

Writing Tests
^^^^^^^^^^^^

Follow these guidelines for writing tests:

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Arrange-Act-Assert**: Structure tests with clear sections
3. **Mocking**: Use mocks for external dependencies
4. **Coverage**: Aim for high test coverage (>90%)
5. **Edge Cases**: Test boundary conditions and error cases

Example Test:

.. code-block:: python

   """Tests for the RAGTool class."""
   
   import pytest
   from unittest.mock import Mock, patch
   from search_flow.tools.rag import RAGTool, DocumentIndexError
   
   
   class TestRAGTool:
       """Test suite for RAGTool."""
       
       @pytest.fixture
       def rag_tool(self):
           """Create a RAGTool instance for testing."""
           return RAGTool()
       
       def test_rag_tool_initialization(self, rag_tool):
           """Test RAG tool initialization."""
           assert rag_tool.name == "rag_search_tool"
           assert "medical document" in rag_tool.description.lower()
       
       def test_validate_input_valid_query(self, rag_tool):
           """Test input validation with valid query."""
           assert rag_tool._validate_input("diabetes symptoms") is True
       
       def test_validate_input_empty_query(self, rag_tool):
           """Test input validation with empty query."""
           assert rag_tool._validate_input("") is False
       
       def test_validate_input_none_query(self, rag_tool):
           """Test input validation with None query."""
           assert rag_tool._validate_input(None) is False
       
       @patch('search_flow.tools.rag.faiss')
       def test_run_success(self, mock_faiss, rag_tool):
           """Test successful RAG search execution."""
           # Arrange
           mock_faiss.read_index.return_value = Mock()
           
           # Act
           result = rag_tool._run("diabetes symptoms")
           
           # Assert
           assert isinstance(result, str)
           assert len(result) > 0
       
       def test_run_invalid_input(self, rag_tool):
           """Test RAG search with invalid input."""
           with pytest.raises(ValueError, match="Invalid query input"):
               rag_tool._run("")

Running Tests
^^^^^^^^^^^^

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=src/search_flow --cov-report=html
   
   # Run specific test file
   pytest tests/unit/test_tools.py
   
   # Run tests matching pattern
   pytest -k "test_rag_tool"
   
   # Run tests in parallel
   pytest -n auto

Extending the System
--------------------

Adding New Tools
^^^^^^^^^^^^^^^

1. **Create the Tool Class**

   .. code-block:: python

      """Custom medical validation tool."""
      
      from crewai.tools import BaseTool
      from typing import Dict, Any
      
      
      class MedicalValidatorTool(BaseTool):
          """Tool for validating medical information."""
          
          name: str = "medical_validator_tool"
          description: str = "Validate medical information accuracy"
          
          def _run(self, medical_text: str, validation_criteria: Dict[str, Any] = None) -> str:
              """Validate medical information.
              
              Args:
                  medical_text: The medical text to validate.
                  validation_criteria: Optional validation criteria.
                  
              Returns:
                  Validation results and recommendations.
              """
              # Implementation here
              return "Validation results"
          
          def _validate_input(self, medical_text: str, **kwargs) -> bool:
              """Validate input parameters."""
              return isinstance(medical_text, str) and len(medical_text.strip()) > 0

2. **Register the Tool**

   Add to the appropriate crew configuration:

   .. code-block:: yaml

      medical_expert:
        name: "Medical Expert"
        tools: ["rag_search_tool", "medical_validator_tool"]

3. **Import in Crew**

   .. code-block:: python

      from search_flow.tools.medical_validator import MedicalValidatorTool
      
      class RAGCrew:
          def __init__(self):
              # ... existing code ...
              self.medical_validator_tool = MedicalValidatorTool()

Adding New Agents
^^^^^^^^^^^^^^^^

1. **Define Agent Configuration**

   .. code-block:: yaml

      specialized_agent:
        name: "Specialized Medical Agent"
        role: "Expert in specific medical field"
        goal: "Provide specialized medical information"
        backstory: "Specialized background and expertise"
        verbose: true
        allow_delegation: true
        tools: ["rag_search_tool", "specialized_tool"]

2. **Create Agent Method**

   .. code-block:: python

      def specialized_agent(self) -> Agent:
          """Create a specialized medical agent."""
          config = self.config["agents"]["specialized_agent"]
          return Agent(**config)

3. **Add to Crew Workflow**

   .. code-block:: python

      def specialized_search(self, query: str) -> str:
          """Execute specialized medical search."""
          agent = self.specialized_agent()
          task = self.specialized_search_task()
          return agent.execute_task(task, context=query)

Adding New Search Types
^^^^^^^^^^^^^^^^^^^^^^

1. **Extend Intent Detection**

   .. code-block:: python

      @start()
      def detect_field(self):
          # ... existing code ...
          
          # Add new intent types
          if "specialized" in self.state.type.lower():
              return 'specialized'
          
          return self.state

2. **Add New Route**

   .. code-block:: python

      @listen('specialized')
      def specialized_search(self):
          """Execute specialized search."""
          # Implementation here
          return self.state

3. **Update Routing Logic**

   .. code-block:: python

      @router(detect_field)
      def route_field(self):
          # ... existing code ...
          if self.state.type.lower() == "specialized":
              return 'specialized'
          return None

Configuration Management
-----------------------

Environment-Specific Configs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create configuration files for different environments:

.. code-block:: yaml

   # config/development.yaml
   system:
     log_level: "DEBUG"
     verbose: true
     cache_enabled: false
   
   agents:
     document_searcher:
       verbose: true
       max_iter: 5

.. code-block:: yaml

   # config/production.yaml
   system:
     log_level: "WARNING"
     verbose: false
     cache_enabled: true
   
   agents:
     document_searcher:
       verbose: false
       max_iter: 3

Dynamic Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   """Configuration manager for dynamic settings."""
   
   import yaml
   import os
   from pathlib import Path
   from typing import Dict, Any
   
   
   class ConfigManager:
       """Manages configuration loading and merging."""
       
       def __init__(self, config_dir: str = "config"):
           self.config_dir = Path(config_dir)
           self.config: Dict[str, Any] = {}
       
       def load_config(self, environment: str = None) -> Dict[str, Any]:
           """Load configuration for a specific environment."""
           if environment is None:
               environment = os.getenv("ENVIRONMENT", "development")
           
           # Load base configuration
           self._load_base_config()
           
           # Load environment-specific configuration
           self._load_environment_config(environment)
           
           # Override with environment variables
           self._override_from_env()
           
           return self.config
       
       def _load_base_config(self):
           """Load base configuration file."""
           base_config = self.config_dir / "base.yaml"
           if base_config.exists():
               with open(base_config) as f:
                   self.config = yaml.safe_load(f)
       
       def _load_environment_config(self, environment: str):
           """Load environment-specific configuration."""
           env_config = self.config_dir / f"{environment}.yaml"
           if env_config.exists():
               with open(env_config) as f:
                   env_settings = yaml.safe_load(f)
                   self._merge_config(self.config, env_settings)
       
       def _merge_config(self, base: dict, override: dict):
           """Recursively merge configuration dictionaries."""
           for key, value in override.items():
               if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                   self._merge_config(base[key], value)
               else:
                   base[key] = value

Performance Optimization
-----------------------

Profiling and Monitoring
^^^^^^^^^^^^^^^^^^^^^^^

1. **Use cProfile for Performance Analysis**

   .. code-block:: python

      import cProfile
      import pstats
      from search_flow.main import SearchFlow
      
      def profile_search_flow():
          """Profile the search flow performance."""
          profiler = cProfile.Profile()
          profiler.enable()
          
          # Run the search flow
          flow = SearchFlow()
          flow.state.question = "What are diabetes symptoms?"
          result = flow.detect_field()
          
          profiler.disable()
          
          # Save stats to file
          stats = pstats.Stats(profiler)
          stats.sort_stats('cumulative')
          stats.print_stats()
          stats.dump_stats('search_flow_profile.prof')

2. **Memory Usage Monitoring**

   .. code-block:: python

      import psutil
      import os
      from search_flow.tools.rag import RAGTool
      
      def monitor_memory_usage():
          """Monitor memory usage during RAG operations."""
          process = psutil.Process(os.getpid())
          
          # Memory before operation
          memory_before = process.memory_info().rss / 1024 / 1024  # MB
          
          # Perform RAG operation
          rag_tool = RAGTool()
          result = rag_tool.run("diabetes symptoms")
          
          # Memory after operation
          memory_after = process.memory_info().rss / 1024 / 1024  # MB
          
          print(f"Memory used: {memory_after - memory_before:.2f} MB")
          return result

Caching Strategies
^^^^^^^^^^^^^^^^^

1. **Result Caching**

   .. code-block:: python

      """Caching decorator for search results."""
      
      import functools
      import hashlib
      from typing import Any, Callable
      
      
      def cache_results(max_size: int = 1000):
          """Cache decorator for search results."""
          cache = {}
          
          def decorator(func: Callable) -> Callable:
              @functools.wraps(func)
              def wrapper(*args, **kwargs):
                  # Create cache key
                  key_data = str(args) + str(sorted(kwargs.items()))
                  cache_key = hashlib.md5(key_data.encode()).hexdigest()
                  
                  # Check cache
                  if cache_key in cache:
                      return cache[cache_key]
                  
                  # Execute function and cache result
                  result = func(*args, **kwargs)
                  
                  # Manage cache size
                  if len(cache) >= max_size:
                      # Remove oldest entry
                      oldest_key = next(iter(cache))
                      del cache[oldest_key]
                  
                  cache[cache_key] = result
                  return result
              
              return wrapper
          return decorator
      
      # Usage
      @cache_results(max_size=500)
      def search_medical_documents(query: str) -> str:
          # Expensive search operation
          return "Search results"

2. **FAISS Index Caching**

   .. code-block:: python

      """FAISS index caching for improved performance."""
      
      import faiss
      import pickle
      from pathlib import Path
      from typing import Optional
      
      
      class CachedFAISSIndex:
          """Cached FAISS index for document search."""
          
          def __init__(self, index_path: str, cache_dir: str = "cache"):
              self.index_path = Path(index_path)
              self.cache_dir = Path(cache_dir)
              self.cache_dir.mkdir(exist_ok=True)
              self._index: Optional[faiss.Index] = None
          
          @property
          def index(self) -> faiss.Index:
              """Get cached FAISS index."""
              if self._index is None:
                  self._index = self._load_index()
              return self._index
          
          def _load_index(self) -> faiss.Index:
              """Load FAISS index with caching."""
              cache_file = self.cache_dir / f"{self.index_path.stem}_cache.pkl"
              
              # Check if cache exists and is newer than index
              if cache_file.exists() and cache_file.stat().st_mtime > self.index_path.stat().st_mtime:
                  try:
                      with open(cache_file, 'rb') as f:
                          return pickle.load(f)
                  except Exception:
                      pass
              
              # Load from original file
              index = faiss.read_index(str(self.index_path))
              
              # Cache the index
              try:
                  with open(cache_file, 'wb') as f:
                      pickle.dump(index, f)
              except Exception:
                  pass
              
              return index

Error Handling and Logging
--------------------------

Custom Exceptions
^^^^^^^^^^^^^^^^

.. code-block:: python

   """Custom exceptions for the RAG Search Flow."""
   
   class SearchFlowError(Exception):
       """Base exception for search flow errors."""
       pass
   
   
   class DocumentIndexError(SearchFlowError):
       """Raised when document index is not available."""
       pass
   
   
   class SearchError(SearchFlowError):
       """Raised when search operations fail."""
       pass
   
   
   class ConfigurationError(SearchFlowError):
       """Raised when configuration is invalid."""
       pass

Structured Logging
^^^^^^^^^^^^^^^^^

.. code-block:: python

   """Structured logging configuration."""
   
   import logging
   import json
   from datetime import datetime
   from typing import Any, Dict
   
   
   class StructuredFormatter(logging.Formatter):
       """JSON formatter for structured logging."""
       
       def format(self, record: logging.LogRecord) -> str:
           log_entry = {
               'timestamp': datetime.utcnow().isoformat(),
               'level': record.levelname,
               'logger': record.name,
               'message': record.getMessage(),
               'module': record.module,
               'function': record.funcName,
               'line': record.lineno
           }
           
           # Add extra fields if present
           if hasattr(record, 'extra_fields'):
               log_entry.update(record.extra_fields)
           
           return json.dumps(log_entry)
   
   
   def setup_logging(level: str = "INFO", log_file: str = None):
       """Setup structured logging."""
       # Configure root logger
       logging.basicConfig(level=getattr(logging, level.upper()))
       
       # Create formatter
       formatter = StructuredFormatter()
       
       # Create handlers
       handlers = [logging.StreamHandler()]
       
       if log_file:
           file_handler = logging.FileHandler(log_file)
           file_handler.setFormatter(formatter)
           handlers.append(file_handler)
       
       # Configure handlers
       for handler in handlers:
           handler.setFormatter(formatter)
           logging.getLogger().addHandler(handler)
       
       # Set specific logger levels
       logging.getLogger('search_flow').setLevel(logging.DEBUG)
       logging.getLogger('crewai').setLevel(logging.INFO)

Debugging Tools
---------------

Interactive Debugging
^^^^^^^^^^^^^^^^^^

1. **Use pdb for Interactive Debugging**

   .. code-block:: python

      import pdb
      from search_flow.main import SearchFlow
      
      def debug_search_flow():
          """Debug the search flow interactively."""
          flow = SearchFlow()
          
          # Set breakpoint
          pdb.set_trace()
          
          # Continue execution
          flow.state.question = "What are diabetes symptoms?"
          result = flow.detect_field()
          
          return result

2. **Remote Debugging with debugpy**

   .. code-block:: python

      """Remote debugging setup for the search flow."""
      
      import debugpy
      from search_flow.main import SearchFlow
      
      def setup_remote_debugging():
          """Setup remote debugging."""
          debugpy.listen(("0.0.0.0", 5678))
          print("Waiting for debugger to attach...")
          debugpy.wait_for_client()
          
          # Continue with normal execution
          flow = SearchFlow()
          return flow

Development Workflow
--------------------

Feature Development
^^^^^^^^^^^^^^^^^

1. **Create Feature Branch**

   .. code-block:: bash

      git checkout -b feature/new-rag-tool
      git push -u origin feature/new-rag-tool

2. **Implement Feature**

   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation
   - Update configuration files

3. **Test Changes**

   .. code-block:: bash

      # Run tests
      pytest
      
      # Check code style
      black --check src/ tests/
      isort --check-only src/ tests/
      
      # Type checking
      mypy src/

4. **Create Pull Request**

   - Provide clear description of changes
   - Include test results
   - Request code review

Code Review Process
^^^^^^^^^^^^^^^^^^

1. **Self-Review Checklist**

   - [ ] Code follows style guidelines
   - [ ] Tests pass and cover new functionality
   - [ ] Documentation is updated
   - [ ] No debugging code left in
   - [ ] Error handling is appropriate

2. **Review Request**

   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Performance impact assessment

3. **Review Feedback**

   - Address all review comments
   - Update code as needed
   - Re-run tests after changes

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^

The project uses GitHub Actions for CI/CD:

.. code-block:: yaml

   # .github/workflows/ci.yml
   name: CI
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: [3.10, 3.11, 3.12]
       
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python ${{ matrix.python-version }}
         uses: actions/setup-python@v4
         with:
           python-version: ${{ matrix.python-version }}
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -e ".[dev]"
       
       - name: Run tests
         run: |
           pytest --cov=src/search_flow --cov-report=xml
       
       - name: Upload coverage
         uses: codecov/codecov-action@v3
         with:
           file: ./coverage.xml

For contribution guidelines, see the :doc:`contributing` section.
