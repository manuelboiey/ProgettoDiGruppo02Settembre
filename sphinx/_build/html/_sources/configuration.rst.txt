Configuration Guide
==================

The RAG Search Flow is highly configurable through YAML configuration files. This section explains how to customize the system behavior, agent properties, and task definitions.

Overview
--------

Configuration is managed through several YAML files:

- **Agents Configuration**: Defines agent roles, goals, and capabilities
- **Tasks Configuration**: Specifies task descriptions and expected outputs
- **System Configuration**: Global settings and parameters
- **Tool Configuration**: Tool-specific settings and options

Configuration Files Structure
----------------------------

.. code-block:: text

   src/search_flow/crews/
   ├── rag_crew/
   │   └── config/
   │       ├── agents.yaml      # RAG crew agent definitions
   │       └── tasks.yaml       # RAG crew task definitions
   └── search_crew/
       └── config/
           ├── agents.yaml      # Search crew agent definitions
           └── tasks.yaml       # Search crew task definitions

Agents Configuration
-------------------

The `agents.yaml` file defines the properties and behavior of each agent in the crew.

Basic Agent Structure
^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   agent_name:
     name: "Human-readable name"
     role: "Agent's role description"
     goal: "What the agent aims to accomplish"
     backstory: "Agent's background and expertise"
     verbose: true/false
     allow_delegation: true/false
     tools: ["tool1", "tool2"]
     memory: true/false

Agent Properties
^^^^^^^^^^^^^^^^

**Core Properties:**

- **name**: Human-readable identifier for the agent
- **role**: Description of the agent's function and responsibilities
- **goal**: Specific objective the agent should achieve
- **backstory**: Background information that shapes agent behavior

**Behavior Properties:**

- **verbose**: Whether the agent provides detailed output
- **allow_delegation**: Whether the agent can delegate tasks to others
- **memory**: Whether the agent maintains conversation memory
- **max_iter**: Maximum number of reasoning iterations

**Tool Properties:**

- **tools**: List of tool names the agent can use
- **tool_choice**: How the agent selects tools ("auto", "required", "none")

Example RAG Crew Agents
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   document_searcher:
     name: "Medical Document Searcher"
     role: "Expert medical document researcher and information specialist"
     goal: "Find the most relevant medical information from local documents using vector similarity search"
     backstory: "Specialized in medical literature, clinical guidelines, and research papers. Expert at understanding medical terminology and extracting relevant information from complex documents."
     verbose: true
     allow_delegation: false
     tools: ["rag_search_tool"]
     memory: false

   medical_expert:
     name: "Medical Expert"
     role: "Board-certified medical professional and information validator"
     goal: "Validate medical information accuracy and provide professional medical context"
     backstory: "Experienced physician with expertise in multiple medical specialties. Skilled at interpreting medical research and providing evidence-based information."
     verbose: true
     allow_delegation: true
     tools: ["rag_search_tool", "medical_validator_tool"]
     memory: true

Example Search Crew Agents
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   web_researcher:
     name: "Web Research Specialist"
     role: "Expert web researcher and information gatherer"
     goal: "Find the most relevant and up-to-date information from the web using advanced search techniques"
     backstory: "Experienced in gathering and analyzing information from multiple sources. Skilled at filtering relevant content and identifying credible sources."
     verbose: true
     allow_delegation: false
     tools: ["ddg_search_tool"]
     memory: false

   information_analyst:
     name: "Information Analyst"
     role: "Data analyst and information synthesizer"
     goal: "Analyze search results and identify the most relevant information"
     backstory: "Expert at analyzing large amounts of information, identifying patterns, and extracting key insights. Skilled at data validation and quality assessment."
     verbose: true
     allow_delegation: true
     tools: ["ddg_search_tool", "content_analyzer_tool"]
     memory: true

Tasks Configuration
------------------

The `tasks.yaml` file defines the tasks that agents can perform and their expected outputs.

Basic Task Structure
^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   task_name:
     description: "What the task accomplishes"
     expected_output: "Format and content of expected results"
     agent: "agent_name"
     tools: ["tool1", "tool2"]
     context: "Additional context or requirements"
     async_execution: true/false

Task Properties
^^^^^^^^^^^^^^

**Core Properties:**

- **description**: Clear explanation of what the task does
- **expected_output**: Specification of the expected result format
- **agent**: Name of the agent assigned to this task

**Execution Properties:**

- **tools**: List of tools required for the task
- **context**: Additional information or requirements
- **async_execution**: Whether the task can run asynchronously
- **max_iter**: Maximum reasoning iterations for complex tasks

**Dependency Properties:**

- **required_tasks**: Tasks that must complete before this one
- **optional_tasks**: Tasks that can run in parallel
- **output_tasks**: Tasks that depend on this task's output

Example RAG Crew Tasks
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   document_search_task:
     description: "Search medical documents for information relevant to the user's query using vector similarity search"
     expected_output: "Comprehensive medical information extracted from relevant documents, including symptoms, treatments, and medical context"
     agent: "document_searcher"
     tools: ["rag_search_tool"]
     context: "Focus on medical accuracy and relevance to the user's specific question"
     async_execution: false

   medical_validation_task:
     description: "Validate the medical accuracy of search results and provide professional medical context"
     expected_output: "Validated medical information with professional context, highlighting any areas of uncertainty or requiring further verification"
     agent: "medical_expert"
     tools: ["rag_search_tool", "medical_validator_tool"]
     context: "Ensure medical information meets professional standards and is appropriate for the user's query"
     async_execution: true

Example Search Crew Tasks
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   web_search_task:
     description: "Perform web search to find current information relevant to the user's query"
     expected_output: "Comprehensive search results from multiple sources, including URLs, titles, and brief descriptions"
     agent: "web_researcher"
     tools: ["ddg_search_tool"]
     context: "Focus on finding the most recent and relevant information from credible sources"
     async_execution: false

   result_analysis_task:
     description: "Analyze web search results and identify the most relevant information for the user"
     expected_output: "Synthesized information summary highlighting key points, sources, and relevance to the user's query"
     agent: "information_analyst"
     tools: ["ddg_search_tool", "content_analyzer_tool"]
     context: "Provide clear, concise information that directly addresses the user's question"
     async_execution: true

System Configuration
-------------------

Global system settings can be configured through environment variables and configuration files.

Environment Variables
^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   # API Configuration
   OPENAI_API_KEY=your_openai_api_key
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   
   # System Configuration
   LOG_LEVEL=INFO
   MAX_CONCURRENT_TASKS=5
   REQUEST_TIMEOUT=30
   
   # Tool Configuration
   FAISS_INDEX_PATH=faiss/index.faiss
   DOCUMENTS_PATH=documents/
   MAX_SEARCH_RESULTS=10

Configuration File
^^^^^^^^^^^^^^^^^

Create a `config.yaml` file in the project root for system-wide settings:

.. code-block:: yaml

   system:
     log_level: "INFO"
     max_concurrent_tasks: 5
     request_timeout: 30
     cache_enabled: true
     cache_ttl: 3600
   
   tools:
     rag:
       faiss_index_path: "faiss/index.faiss"
       documents_path: "documents/"
       chunk_size: 1000
       similarity_threshold: 0.7
       max_results: 5
     
     ddg_search:
       max_results: 5
       search_region: "it-IT"
       result_type: "web"
       language: "it"
       safe_search: true
   
   agents:
     default_verbose: true
     default_memory: false
     max_iterations: 3

Customization Examples
----------------------

Adding a New Agent
^^^^^^^^^^^^^^^^^^

1. **Define the agent in agents.yaml:**

   .. code-block:: yaml

      specialized_agent:
        name: "Specialized Medical Agent"
        role: "Expert in specific medical field"
        goal: "Provide specialized medical information"
        backstory: "Specialized background and expertise"
        verbose: true
        allow_delegation: true
        tools: ["rag_search_tool", "specialized_tool"]

2. **Create corresponding task in tasks.yaml:**

   .. code-block:: yaml

      specialized_task:
        description: "Perform specialized medical analysis"
        expected_output: "Specialized medical information and analysis"
        agent: "specialized_agent"
        tools: ["rag_search_tool", "specialized_tool"]

3. **Integrate into crew workflow:**

   .. code-block:: python

      class CustomRAGCrew(RAGCrew):
          def specialized_agent(self):
              return Agent(**self.config["agents"]["specialized_agent"])
          
          def specialized_task(self):
              return Task(**self.config["tasks"]["specialized_task"])

Modifying Agent Behavior
^^^^^^^^^^^^^^^^^^^^^^^^

**Change verbosity:**

.. code-block:: yaml

   document_searcher:
     verbose: false  # Reduce output detail

**Add new tools:**

.. code-block:: yaml

   medical_expert:
     tools: ["rag_search_tool", "medical_validator_tool", "new_tool"]

**Modify goals:**

.. code-block:: yaml

   web_researcher:
     goal: "Find the most relevant information with emphasis on recent sources"

Advanced Configuration
---------------------

**Conditional Configuration:**

.. code-block:: yaml

   agents:
     document_searcher:
       verbose: ${VERBOSE_MODE:-true}
       max_iter: ${MAX_ITERATIONS:-3}

**Environment-Specific Settings:**

.. code-block:: yaml

   environments:
     development:
       log_level: "DEBUG"
       verbose: true
       cache_enabled: false
     
     production:
       log_level: "WARNING"
       verbose: false
       cache_enabled: true

**Dynamic Configuration:**

.. code-block:: python

   import yaml
   from pathlib import Path
   
   def load_config():
       config_path = Path("config.yaml")
       with open(config_path) as f:
           config = yaml.safe_load(f)
       
       # Override with environment variables
       config["system"]["log_level"] = os.getenv("LOG_LEVEL", "INFO")
       return config

Configuration Validation
-----------------------

The system validates configuration files to ensure:

- **Required fields**: All necessary properties are present
- **Type validation**: Values match expected data types
- **Dependency checking**: Referenced agents and tools exist
- **Syntax validation**: YAML format is correct

For detailed API documentation, see the :doc:`api/modules` section.
