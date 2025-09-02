RAG Search Flow Documentation
=============================

Welcome to the RAG Search Flow documentation! This project implements an intelligent search system that combines Retrieval-Augmented Generation (RAG) for medical document search with web search capabilities for general queries.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Core Components:

   search_flow
   crews
   tools

.. toctree::
   :maxdepth: 2
   :caption: Configuration:

   configuration
   agents
   tasks

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/modules

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples

.. toctree::
   :maxdepth: 2
   :caption: Development:

   development
   contributing

.. toctree::
   :maxdepth: 2
   :caption: EU AI Act Compliance:

   application_compliance
   data_compliance
   ai_compliance


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Overview
--------

The RAG Search Flow is a sophisticated AI-powered search system built with `crewAI <https://crewai.com>`_ that intelligently routes user queries between:

- **Medical Document Search (RAG)**: Searches through local medical documents using vector similarity and AI-powered retrieval
- **Web Search**: Performs general web searches using DuckDuckGo for non-medical queries

The system automatically detects the intent of user queries and routes them to the appropriate search mechanism, providing intelligent and context-aware search results.

Key Features
-----------

- 🤖 **AI-Powered Intent Detection**: Automatically determines if queries are medical or general
- 📚 **RAG Document Search**: Efficient vector-based search through local medical documents
- 🌐 **Web Search Integration**: Seamless web search for general queries
- 🔄 **Intelligent Routing**: Smart flow management between different search types
- 🚀 **crewAI Framework**: Built on the powerful crewAI multi-agent framework

Architecture
-----------

The system is built around a flow-based architecture where:

1. **SearchFlow** orchestrates the entire search process
2. **RAGCrew** handles medical document searches using FAISS vector database
3. **SearchCrew** manages web searches and result summarization
4. **Tools** provide specialized functionality for different search types

For more details, see the :doc:`search_flow` section.

