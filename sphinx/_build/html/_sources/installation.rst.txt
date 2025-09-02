Installation Guide
==================

This guide will help you install and set up the RAG Search Flow project on your system.

Prerequisites
------------

- **Python**: Version 3.10 or higher (but less than 3.14)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM recommended for FAISS operations

System Requirements
------------------

- **Python**: 3.10.x, 3.11.x, or 3.12.x
- **pip**: Latest version
- **Git**: For cloning the repository

Installation Steps
------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone <your-repository-url>
      cd rag_search

2. **Install UV (Recommended Package Manager)**

   The project uses `UV <https://docs.astral.sh/uv/>`_ for dependency management, which provides faster and more reliable package handling.

   .. code-block:: bash

      pip install uv

3. **Install Dependencies**

   Using UV (recommended):

   .. code-block:: bash

      uv sync

   Or using pip:

   .. code-block:: bash

      pip install -e .

4. **Install Sphinx Documentation Dependencies**

   .. code-block:: bash

      pip install sphinx sphinx-rtd-theme

5. **Set Up Environment Variables**

   Create a `.env` file in the project root:

   .. code-block:: text

      OPENAI_API_KEY=your_openai_api_key_here
      AZURE_OPENAI_API_KEY=your_azure_api_key_here
      AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here

   **Note**: You need at least one of these API keys configured.

6. **Verify Installation**

   Test that everything is working:

   .. code-block:: bash

      python -c "import search_flow; print('Installation successful!')"

Troubleshooting
--------------

Common Issues and Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Python Version Issues**
   - Ensure you're using Python 3.10-3.12
   - Use `python --version` to check your version

**FAISS Installation Problems**
   - On Windows, you might need to install Visual C++ build tools
   - Try: `pip install faiss-cpu --no-cache-dir`

**Memory Issues**
   - FAISS operations can be memory-intensive
   - Close other applications if you encounter memory errors

**API Key Issues**
   - Ensure your `.env` file is in the project root
   - Check that the API keys are valid and have sufficient credits

**Permission Errors**
   - On Linux/macOS, you might need to use `sudo` for global installations
   - Consider using virtual environments to avoid permission issues

Virtual Environment Setup
------------------------

It's recommended to use a virtual environment:

.. code-block:: bash

   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -e .

Development Installation
-----------------------

For development and contribution:

.. code-block:: bash

   # Install in development mode
   pip install -e ".[dev]"

   # Install pre-commit hooks
   pre-commit install

   # Run tests
   pytest

Next Steps
----------

After successful installation:

1. Read the :doc:`quickstart` guide to get started
2. Explore the :doc:`configuration` section to customize the system
3. Check out :doc:`examples` for usage examples

For more help, see the :doc:`development` section or check the project's GitHub repository.
