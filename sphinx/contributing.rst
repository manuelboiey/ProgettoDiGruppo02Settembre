Contributing Guidelines
======================

Thank you for your interest in contributing to the RAG Search Flow project! This document provides guidelines and information for contributors.

How to Contribute
-----------------

There are many ways to contribute to the project:

- **Code Contributions**: Bug fixes, new features, improvements
- **Documentation**: Improving docs, adding examples, fixing typos
- **Testing**: Writing tests, improving test coverage
- **Bug Reports**: Reporting issues and suggesting improvements
- **Feature Requests**: Proposing new functionality
- **Code Review**: Reviewing pull requests from other contributors

Getting Started
--------------

1. **Fork the Repository**

   Visit the project repository and click the "Fork" button to create your own copy.

2. **Clone Your Fork**

   .. code-block:: bash

      git clone https://github.com/your-username/rag_search.git
      cd rag_search

3. **Set Up Development Environment**

   Follow the setup instructions in the :doc:`development` section.

4. **Create a Branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name
      # or
      git checkout -b fix/your-bug-fix

Development Workflow
-------------------

1. **Make Your Changes**

   - Write clean, well-documented code
   - Follow the project's coding standards
   - Add tests for new functionality
   - Update documentation as needed

2. **Test Your Changes**

   .. code-block:: bash

      # Run the test suite
      pytest
      
      # Check code style
      black --check src/ tests/
      isort --check-only src/ tests/
      
      # Type checking
      mypy src/

3. **Commit Your Changes**

   Use conventional commit messages:

   .. code-block:: bash

      git add .
      git commit -m "feat: add new medical validation tool"
      git commit -m "fix: resolve FAISS index loading issue"
      git commit -m "docs: update installation guide"

4. **Push and Create Pull Request**

   .. code-block:: bash

      git push origin feature/your-feature-name

   Then create a pull request through the GitHub interface.

Coding Standards
----------------

Python Style Guide
^^^^^^^^^^^^^^^^^

- Follow **PEP 8** with project-specific modifications
- Maximum line length: **120 characters**
- Use **type hints** for all public functions
- Write **Google-style docstrings** for all public functions
- Use **f-strings** for string formatting (Python 3.6+)

Example:

.. code-block:: python

   """Medical document search tool using RAG.
   
   This module provides the RAGTool class for searching medical documents
   using vector similarity search with FAISS.
   """
   
   from typing import List, Optional
   import faiss
   from crewai.tools import BaseTool
   
   
   class RAGTool(BaseTool):
       """Tool for searching medical documents using RAG."""
       
       name: str = "rag_search_tool"
       description: str = "Search medical documents using vector similarity"
       
       def _run(self, query: str, max_results: Optional[int] = None) -> str:
           """Execute the RAG search.
           
           Args:
               query: The search query string.
               max_results: Maximum number of results to return.
               
           Returns:
               Search results as a formatted string.
               
           Raises:
               DocumentIndexError: If the document index is not available.
               SearchError: If the search operation fails.
           """
           if not self._validate_input(query):
               raise ValueError("Invalid query input")
           
           try:
               results = self._perform_search(query, max_results)
               return self._format_results(results)
           except Exception as e:
               raise SearchError(f"Search failed: {e}")

Import Organization
^^^^^^^^^^^^^^^^^^

Organize imports in this order:

1. **Standard library imports**
2. **Third-party imports**
3. **Local application imports**

Separate each group with a blank line:

.. code-block:: python

   """Example of proper import organization."""
   
   import os
   import sys
   from pathlib import Path
   from typing import Dict, List, Optional
   
   import faiss
   import numpy as np
   from crewai.tools import BaseTool
   from pydantic import BaseModel
   
   from search_flow.crews.utils import load_config
   from search_flow.tools.base import BaseSearchTool

Naming Conventions
^^^^^^^^^^^^^^^^^

- **Classes**: Use `PascalCase` (e.g., `RAGTool`, `SearchFlow`)
- **Functions and Methods**: Use `snake_case` (e.g., `perform_search`, `validate_input`)
- **Variables**: Use `snake_case` (e.g., `search_results`, `max_items`)
- **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_RESULTS`, `DEFAULT_TIMEOUT`)
- **Private Methods**: Prefix with underscore (e.g., `_validate_input`, `_format_results`)

Testing Guidelines
------------------

Test Structure
^^^^^^^^^^^^^

Organize tests to mirror the source code structure:

.. code-block:: text

   tests/
   ├── unit/                    # Unit tests
   │   ├── test_main.py        # Tests for main.py
   │   ├── test_rag_crew.py    # Tests for RAG crew
   │   ├── test_search_crew.py # Tests for search crew
   │   └── test_tools.py       # Tests for tools
   ├── integration/             # Integration tests
   │   ├── test_flow.py        # End-to-end flow tests
   │   └── test_crews.py       # Crew integration tests
   └── fixtures/                # Test data and fixtures
       ├── sample_documents/    # Sample medical documents
       └── test_configs/        # Test configuration files

Writing Tests
^^^^^^^^^^^^

Follow these principles:

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
   from search_flow.tools.rag import RAGTool, DocumentIndexError, SearchError
   
   
   class TestRAGTool:
       """Test suite for RAGTool."""
       
       @pytest.fixture
       def rag_tool(self):
           """Create a RAGTool instance for testing."""
           return RAGTool()
       
       @pytest.fixture
       def mock_faiss_index(self):
           """Create a mock FAISS index."""
           mock_index = Mock()
           mock_index.search.return_value = ([0.8, 0.7], [0, 1])
           return mock_index
       
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
       def test_run_success(self, mock_faiss, rag_tool, mock_faiss_index):
           """Test successful RAG search execution."""
           # Arrange
           mock_faiss.read_index.return_value = mock_faiss_index
           
           # Act
           result = rag_tool._run("diabetes symptoms")
           
           # Assert
           assert isinstance(result, str)
           assert len(result) > 0
           mock_faiss.read_index.assert_called_once()
       
       def test_run_invalid_input(self, rag_tool):
           """Test RAG search with invalid input."""
           with pytest.raises(ValueError, match="Invalid query input"):
               rag_tool._run("")
       
       @patch('search_flow.tools.rag.faiss')
       def test_run_document_index_error(self, mock_faiss, rag_tool):
           """Test RAG search when document index is not available."""
           # Arrange
           mock_faiss.read_index.side_effect = FileNotFoundError("Index not found")
           
           # Act & Assert
           with pytest.raises(DocumentIndexError, match="Document index not available"):
               rag_tool._run("diabetes symptoms")

Test Fixtures
^^^^^^^^^^^^

Create reusable test fixtures:

.. code-block:: python

   """Test fixtures for the RAG Search Flow."""
   
   import pytest
   from pathlib import Path
   from search_flow.main import SearchFlow
   from search_flow.tools.rag import RAGTool
   from search_flow.tools.ddg_search import DuckDuckGoSearchTool
   
   
   @pytest.fixture
   def sample_documents():
       """Provide sample medical documents for testing."""
       return [
           "Diabetes is a chronic disease that affects how your body turns food into energy.",
           "Hypertension, or high blood pressure, is a common condition affecting blood vessels.",
           "Asthma is a condition that affects the airways in the lungs."
       ]
   
   
   @pytest.fixture
   def test_config():
       """Provide test configuration."""
       return {
           "agents": {
               "document_searcher": {
                   "name": "Test Document Searcher",
                   "role": "Test medical document researcher",
                   "goal": "Find test medical information",
                   "verbose": False
               }
           },
           "tools": {
               "rag": {
                   "similarity_threshold": 0.5,
                   "max_results": 3
               }
           }
       }
   
   
   @pytest.fixture
   def mock_llm_response():
       """Provide mock LLM responses for testing."""
       return {
           "diabetes symptoms": "medicina",
           "latest news": "altro",
           "weather forecast": "altro",
           "hypertension treatment": "medicina"
       }

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
   
   # Run tests with verbose output
   pytest -v
   
   # Run tests and stop on first failure
   pytest -x

Documentation Standards
-----------------------

Documentation Structure
^^^^^^^^^^^^^^^^^^^^^^

- **Docstrings**: Use Google-style docstrings for all public functions
- **README**: Keep the main README focused and link to detailed docs
- **API Documentation**: Use Sphinx autodoc for automatic generation
- **Examples**: Provide practical examples for all major features
- **Tutorials**: Step-by-step guides for common use cases

Docstring Format
^^^^^^^^^^^^^^^^

.. code-block:: python

   def search_medical_documents(
       query: str,
       max_results: int = 5,
       similarity_threshold: float = 0.7
   ) -> List[Dict[str, Any]]:
       """Search medical documents using vector similarity.
       
       This function performs a semantic search through medical documents
       using FAISS vector similarity. It returns the most relevant documents
       based on the query and similarity threshold.
       
       Args:
           query: The search query string.
           max_results: Maximum number of results to return. Defaults to 5.
           similarity_threshold: Minimum similarity score for results.
               Defaults to 0.7.
       
       Returns:
           List of dictionaries containing search results. Each dictionary
           includes 'document_id', 'content', 'similarity_score', and
           'metadata' fields.
       
       Raises:
           DocumentIndexError: If the document index is not available.
           SearchError: If the search operation fails.
           ValueError: If input parameters are invalid.
       
       Example:
           >>> results = search_medical_documents("diabetes symptoms", max_results=3)
           >>> for result in results:
           ...     print(f"Score: {result['similarity_score']}")
           ...     print(f"Content: {result['content'][:100]}...")
       
       Note:
           The similarity threshold should be between 0.0 and 1.0. Higher
           values result in more precise but fewer results.
       """

Pull Request Guidelines
-----------------------

Before Submitting
^^^^^^^^^^^^^^^^

1. **Ensure Tests Pass**: All tests must pass before submitting
2. **Check Code Style**: Run formatting tools and style checks
3. **Update Documentation**: Update relevant documentation
4. **Add Tests**: Include tests for new functionality
5. **Self-Review**: Review your own code before submitting

Pull Request Template
^^^^^^^^^^^^^^^^^^^^

Use this template for pull requests:

.. code-block:: markdown

   ## Description
   
   Brief description of the changes made.
   
   ## Type of Change
   
   - [ ] Bug fix (non-breaking change which fixes an issue)
   - [ ] New feature (non-breaking change which adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update
   - [ ] Test addition or update
   
   ## Testing
   
   - [ ] All tests pass
   - [ ] New tests added for new functionality
   - [ ] Test coverage maintained or improved
   
   ## Checklist
   
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No debugging code left in
   - [ ] Error handling is appropriate
   - [ ] Performance impact considered
   
   ## Related Issues
   
   Fixes #(issue number)
   Related to #(issue number)

Code Review Process
-------------------

Review Checklist
^^^^^^^^^^^^^^^

When reviewing code, check for:

- **Functionality**: Does the code do what it's supposed to do?
- **Code Quality**: Is the code clean, readable, and maintainable?
- **Testing**: Are there adequate tests for the changes?
- **Documentation**: Is the documentation updated and clear?
- **Performance**: Are there any performance implications?
- **Security**: Are there any security concerns?
- **Error Handling**: Is error handling appropriate and comprehensive?

Review Comments
^^^^^^^^^^^^^^

Provide constructive feedback:

- **Be Specific**: Point out specific issues with line numbers
- **Suggest Solutions**: Offer concrete suggestions for improvement
- **Be Respectful**: Maintain a professional and helpful tone
- **Focus on Code**: Keep feedback focused on the code, not the person

Example Review Comment:

.. code-block:: markdown

   ```python
   # Line 45: Consider adding input validation here
   def process_query(query: str) -> str:
       # Missing validation for empty or None query
       return self._search(query)
   ```
   
   **Suggestion**: Add input validation to handle edge cases:
   
   ```python
   def process_query(query: str) -> str:
       if not query or not query.strip():
           raise ValueError("Query cannot be empty")
       return self._search(query)
   ```

Issue Reporting
---------------

Bug Reports
^^^^^^^^^^

When reporting bugs, include:

1. **Clear Description**: What happened vs. what was expected
2. **Reproduction Steps**: Step-by-step instructions to reproduce
3. **Environment**: OS, Python version, package versions
4. **Error Messages**: Full error messages and stack traces
5. **Minimal Example**: Minimal code example that reproduces the issue

Bug Report Template:

.. code-block:: markdown

   ## Bug Description
   
   Brief description of the bug.
   
   ## Steps to Reproduce
   
   1. Step 1
   2. Step 2
   3. Step 3
   
   ## Expected Behavior
   
   What you expected to happen.
   
   ## Actual Behavior
   
   What actually happened.
   
   ## Environment
   
   - OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
   - Python Version: [e.g., 3.10.0]
   - Package Versions: [e.g., crewai 0.165.1, faiss-cpu 1.12.0]
   
   ## Error Messages
   
   ```
   Paste error messages here
   ```
   
   ## Additional Information
   
   Any other context about the problem.

Feature Requests
^^^^^^^^^^^^^^^

When requesting features, include:

1. **Problem Statement**: What problem does this feature solve?
2. **Proposed Solution**: How should the feature work?
3. **Use Cases**: What are the main use cases?
4. **Alternatives**: What alternatives have you considered?
5. **Impact**: What is the expected impact on the project?

Feature Request Template:

.. code-block:: markdown

   ## Problem Statement
   
   Clear description of the problem this feature would solve.
   
   ## Proposed Solution
   
   Description of how the feature should work.
   
   ## Use Cases
   
   - Use case 1
   - Use case 2
   - Use case 3
   
   ## Alternatives Considered
   
   Description of alternatives you've considered.
   
   ## Impact
   
   Expected impact on the project and users.

Community Guidelines
--------------------

Code of Conduct
^^^^^^^^^^^^^^

- **Be Respectful**: Treat all contributors with respect
- **Be Inclusive**: Welcome contributors from diverse backgrounds
- **Be Constructive**: Provide helpful and constructive feedback
- **Be Patient**: Understand that contributors have different skill levels
- **Be Collaborative**: Work together to improve the project

Communication Channels
^^^^^^^^^^^^^^^^^^^^^

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions and reviews
- **Documentation**: For improving project documentation

Getting Help
^^^^^^^^^^^

If you need help:

1. **Check Documentation**: Review the project documentation first
2. **Search Issues**: Look for similar issues in the GitHub repository
3. **Ask Questions**: Use GitHub Discussions for questions
4. **Join Community**: Participate in community discussions

Recognition
-----------

Contributor Recognition
^^^^^^^^^^^^^^^^^^^^^^

Contributors are recognized through:

- **Contributors List**: Added to the project's contributors list
- **Commit History**: Git commit history preserves contributions
- **Release Notes**: Contributors acknowledged in release notes
- **Documentation**: Contributors credited in relevant documentation

Types of Contributions
^^^^^^^^^^^^^^^^^^^^^

- **Code Contributors**: Those who contribute code changes
- **Documentation Contributors**: Those who improve documentation
- **Test Contributors**: Those who add or improve tests
- **Review Contributors**: Those who provide code reviews
- **Community Contributors**: Those who help with community support

For more information about development, see the :doc:`development` section.
