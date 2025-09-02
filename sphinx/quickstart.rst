Quick Start Guide
================

This guide will get you up and running with the RAG Search Flow in just a few minutes.

Prerequisites
------------

- ✅ Python 3.10+ installed
- ✅ Project dependencies installed (see :doc:`installation`)
- ✅ API keys configured in `.env` file
- ✅ Medical documents in the `documents/` folder

Basic Usage
-----------

1. **Start the Search Flow**

   From the project root directory:

   .. code-block:: bash

      crewai run

   Or alternatively:

   .. code-block:: bash

      python -m search_flow.main

2. **Ask a Question**

   The system will prompt you to ask a question. Try these examples:

   **Medical Query:**
   - "What are the symptoms of diabetes?"
   - "How to treat hypertension?"
   - "What is the recommended dosage for aspirin?"

   **General Query:**
   - "What's the weather like today?"
   - "Latest news about AI technology"
   - "How to cook pasta carbonara"

3. **Get Results**

   The system will automatically:
   - Detect the type of query (medical vs. general)
   - Route to the appropriate search mechanism
   - Return relevant results

Example Session
--------------

Here's what a typical session looks like:

.. code-block:: text

   > crewai run
   
   Chiedimi quello che vuoi!
   > What are the symptoms of diabetes?
   
   [System detects: medicina]
   [Searching medical documents...]
   
   Based on the medical documents, diabetes symptoms include:
   - Increased thirst and frequent urination
   - Increased hunger
   - Weight loss
   - Fatigue
   - Blurred vision
   - Slow-healing sores
   
   > What's the latest news about space exploration?
   
   [System detects: altro]
   [Searching web...]
   [Summarizing results...]
   
   Recent space exploration news includes:
   - NASA's Artemis program developments
   - SpaceX Starship updates
   - International Space Station activities
   - Mars rover discoveries

Configuration
------------

The system uses two main configuration files:

- **Agents**: `src/search_flow/crews/rag_crew/config/agents.yaml`
- **Tasks**: `src/search_flow/crews/rag_crew/config/tasks.yaml`

You can customize:
- AI models used
- Search parameters
- Response formatting
- Agent behaviors

For detailed configuration options, see :doc:`configuration`.

Advanced Features
----------------

**Custom Medical Documents**

Add your own medical documents to the `documents/` folder:

.. code-block:: text

   documents/
   ├── cardiology.txt
   ├── pediatrics.txt
   ├── pharmacology.txt
   └── your_document.txt

**Flow Visualization**

Generate a visual representation of the search flow:

.. code-block:: bash

   python -m search_flow.main plot

This creates `search_flow_diagram.html` showing the flow structure.

**Custom Crews**

Extend the system with your own crews and agents:

.. code-block:: python

   from search_flow.crews.base_crew import BaseCrew
   
   class CustomCrew(BaseCrew):
       def __init__(self):
           super().__init__()
           # Add your custom logic here

Troubleshooting
--------------

**Common Issues:**

1. **"No module named 'search_flow'"**
   - Ensure you're in the project root directory
   - Check that dependencies are installed

2. **API Key Errors**
   - Verify your `.env` file exists and contains valid keys
   - Check API key permissions and credits

3. **Document Search Not Working**
   - Ensure documents are in the `documents/` folder
   - Check that the FAISS index is properly built

4. **Web Search Fails**
   - Check internet connection
   - Verify DuckDuckGo search tool configuration

**Getting Help:**

- Check the :doc:`troubleshooting` section
- Review the :doc:`api/modules` reference
- Look at the :doc:`examples` for working code samples

Next Steps
----------

Now that you're up and running:

1. **Explore the API**: See :doc:`api/modules` for detailed function documentation
2. **Customize**: Modify :doc:`configuration` to suit your needs
3. **Extend**: Learn how to :doc:`development` add new features
4. **Contribute**: Check out :doc:`contributing` guidelines

The system is designed to be extensible, so feel free to experiment and build upon it!
