Examples and Use Cases
======================

This section provides practical examples and use cases for the RAG Search Flow system, demonstrating how to use different features and customize the system for various scenarios.

Basic Usage Examples
--------------------

Simple Medical Query
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.main import SearchFlow
   
   # Initialize the search flow
   flow = SearchFlow()
   
   # Ask a medical question
   flow.state.question = "What are the symptoms of diabetes?"
   
   # Run the flow
   result = flow.detect_field()
   
   # The system will automatically:
   # 1. Detect this as a medical query
   # 2. Route to RAG crew for document search
   # 3. Return relevant medical information
   
   print(f"Query type: {result.type}")
   print(f"Results: {result.result}")

Simple Web Query
^^^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.main import SearchFlow
   
   # Initialize the search flow
   flow = SearchFlow()
   
   # Ask a general question
   flow.state.question = "What's the latest news about AI technology?"
   
   # Run the flow
   result = flow.detect_field()
   
   # The system will automatically:
   # 1. Detect this as a general query
   # 2. Route to search crew for web search
   # 3. Return summarized web results
   
   print(f"Query type: {result.type}")
   print(f"Summary: {result.summary}")

Interactive Session
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.main import SearchFlow
   
   def interactive_search():
       flow = SearchFlow()
       
       print("Welcome to RAG Search Flow!")
       print("Ask me anything - medical questions or general queries.")
       print("Type 'quit' to exit.\n")
       
       while True:
           try:
               # Get user input
               question = input("> ")
               
               if question.lower() == 'quit':
                   break
               
               # Set the question and run the flow
               flow.state.question = question
               result = flow.detect_field()
               
               # Display results based on type
               if result.type.lower() == "medicina":
                   print(f"\n🔬 Medical Information:")
                   print(result.result)
               elif result.type.lower() == "altro":
                   print(f"\n🌐 Web Search Results:")
                   print(result.summary)
               else:
                   print("❓ I couldn't determine the type of query.")
               
               print("\n" + "="*50 + "\n")
               
           except KeyboardInterrupt:
               print("\nGoodbye!")
               break
           except Exception as e:
               print(f"Error: {e}")
   
   if __name__ == "__main__":
       interactive_search()

Advanced Usage Examples
-----------------------

Custom RAG Crew
^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.crews.rag_crew.rag_crew import RAGCrew
   from crewai import Agent, Task
   
   class CustomRAGCrew(RAGCrew):
       def __init__(self):
           super().__init__()
           # Add custom configuration
           self.custom_config = {
               "specialized_agent": {
                   "name": "Cardiology Specialist",
                   "role": "Expert cardiologist",
                   "goal": "Provide specialized cardiovascular information",
                   "backstory": "Board-certified cardiologist with 20+ years experience",
                   "verbose": True,
                   "tools": ["rag_search_tool"]
               }
           }
       
       def cardiology_specialist(self):
           """Create a specialized cardiology agent."""
           config = self.custom_config["specialized_agent"]
           return Agent(**config)
       
       def cardiology_search_task(self):
           """Create a specialized cardiology search task."""
           return Task(
               description="Search for specialized cardiovascular information",
               expected_output="Detailed cardiovascular medical information",
               agent=self.cardiology_specialist()
           )
   
   # Usage
   custom_crew = CustomRAGCrew()
   specialist = custom_crew.cardiology_specialist()
   task = custom_crew.cardiology_search_task()
   
   # Execute the task
   result = specialist.execute_task(task, context="heart disease symptoms")

Custom Search Crew
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.crews.search_crew.search_crew import SearchCrew
   from crewai import Agent, Task
   
   class CustomSearchCrew(SearchCrew):
       def __init__(self):
           super().__init__()
           # Add specialized news search agent
           self.news_config = {
               "news_specialist": {
                   "name": "News Research Specialist",
                   "role": "Expert news researcher and analyst",
                   "goal": "Find and analyze the most relevant news",
                   "backstory": "Experienced journalist and news analyst",
                   "verbose": True,
                   "tools": ["ddg_search_tool"]
               }
           }
       
       def news_specialist(self):
           """Create a specialized news research agent."""
           config = self.news_config["news_specialist"]
           return Agent(**config)
       
       def news_search_task(self):
           """Create a specialized news search task."""
           return Task(
               description="Search for and analyze relevant news articles",
               expected_output="Comprehensive news analysis with key insights",
               agent=self.news_specialist()
           )
   
   # Usage
   custom_crew = CustomSearchCrew()
   news_agent = custom_crew.news_specialist()
   news_task = custom_crew.news_search_task()
   
   # Execute news search
   result = news_agent.execute_task(news_task, context="latest technology developments")

Custom Tools
^^^^^^^^^^^

.. code-block:: python

   from crewai.tools import BaseTool
   import requests
   
   class WeatherTool(BaseTool):
       name: str = "weather_tool"
       description: str = "Get current weather information for a location"
       
       def _run(self, location: str) -> str:
           """Get weather information for a specific location."""
           try:
               # This is a simplified example - you'd use a real weather API
               # For demonstration, we'll return mock data
               weather_data = {
                   "Rome": "22°C, Sunny",
                   "Milan": "18°C, Cloudy",
                   "Naples": "25°C, Partly Cloudy"
               }
               
               if location in weather_data:
                   return f"Weather in {location}: {weather_data[location]}"
               else:
                   return f"Weather information not available for {location}"
                   
           except Exception as e:
               return f"Error getting weather: {str(e)}"
       
       def _validate_input(self, location: str) -> bool:
           """Validate the location input."""
           return isinstance(location, str) and len(location.strip()) > 0
   
   # Usage
   weather_tool = WeatherTool()
   result = weather_tool.run("Rome")
   print(result)  # Output: Weather in Rome: 22°C, Sunny

Integration Examples
--------------------

Flask Web Application
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from flask import Flask, request, jsonify
   from search_flow.main import SearchFlow
   import threading
   
   app = Flask(__name__)
   
   # Global flow instance
   flow = SearchFlow()
   
   @app.route('/search', methods=['POST'])
   def search():
       """API endpoint for search queries."""
       try:
           data = request.get_json()
           question = data.get('question', '')
           
           if not question:
               return jsonify({'error': 'Question is required'}), 400
           
           # Set the question and run the flow
           flow.state.question = question
           result = flow.detect_field()
           
           # Prepare response
           response = {
               'question': question,
               'type': result.type,
               'result': result.result if result.type.lower() == "medicina" else result.summary,
               'raw_results': result.raw_results,
               'timestamp': result.timestamp if hasattr(result, 'timestamp') else None
           }
           
           return jsonify(response)
           
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   
   @app.route('/health', methods=['GET'])
   def health():
       """Health check endpoint."""
       return jsonify({'status': 'healthy'})
   
   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)

FastAPI Application
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from search_flow.main import SearchFlow
   import asyncio
   
   app = FastAPI(title="RAG Search Flow API")
   
   # Global flow instance
   flow = SearchFlow()
   
   class SearchRequest(BaseModel):
       question: str
   
   class SearchResponse(BaseModel):
       question: str
       type: str
       result: str
       raw_results: str = ""
       summary: str = ""
   
   @app.post("/search", response_model=SearchResponse)
   async def search(request: SearchRequest):
       """Search endpoint for queries."""
       try:
           # Set the question and run the flow
           flow.state.question = request.question
           result = flow.detect_field()
           
           # Prepare response
           response = SearchResponse(
               question=request.question,
               type=result.type,
               result=result.result if result.type.lower() == "medicina" else result.summary,
               raw_results=result.raw_results,
               summary=result.summary
           )
           
           return response
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   
   @app.get("/health")
   async def health():
       """Health check endpoint."""
       return {"status": "healthy"}
   
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)

Batch Processing
^^^^^^^^^^^^^^^^

.. code-block:: python

   from search_flow.main import SearchFlow
   import csv
   from typing import List, Dict
   
   class BatchProcessor:
       def __init__(self):
           self.flow = SearchFlow()
       
       def process_queries(self, queries: List[str]) -> List[Dict]:
           """Process multiple queries in batch."""
           results = []
           
           for i, query in enumerate(queries):
               print(f"Processing query {i+1}/{len(queries)}: {query}")
               
               try:
                   # Set the question and run the flow
                   self.flow.state.question = query
                   result = self.flow.detect_field()
                   
                   # Store results
                   query_result = {
                       'query': query,
                       'type': result.type,
                       'result': result.result if result.type.lower() == "medicina" else result.summary,
                       'raw_results': result.raw_results,
                       'summary': result.summary,
                       'status': 'success'
                   }
                   
               except Exception as e:
                   query_result = {
                       'query': query,
                       'type': 'error',
                       'result': '',
                       'raw_results': '',
                       'summary': '',
                       'status': f'error: {str(e)}'
                   }
               
               results.append(query_result)
           
           return results
       
       def save_to_csv(self, results: List[Dict], filename: str):
           """Save results to a CSV file."""
           with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
               fieldnames = ['query', 'type', 'result', 'raw_results', 'summary', 'status']
               writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
               
               writer.writeheader()
               for result in results:
                   writer.writerow(result)
   
   # Usage
   processor = BatchProcessor()
   
   # List of queries to process
   queries = [
       "What are diabetes symptoms?",
       "Latest news about AI",
       "How to treat hypertension?",
       "Weather forecast for Rome",
       "What is machine learning?"
   ]
   
   # Process all queries
   results = processor.process_queries(queries)
   
   # Save results to CSV
   processor.save_to_csv(results, 'search_results.csv')
   
   print(f"Processed {len(queries)} queries. Results saved to search_results.csv")

Custom Configuration Examples
-----------------------------

Environment-Specific Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
   
   tools:
     rag:
       similarity_threshold: 0.5
       max_results: 10

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
   
   tools:
     rag:
       similarity_threshold: 0.7
       max_results: 5

Dynamic Configuration Loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import yaml
   import os
   from pathlib import Path
   
   class ConfigManager:
       def __init__(self, config_dir: str = "config"):
           self.config_dir = Path(config_dir)
           self.config = {}
       
       def load_config(self, environment: str = None):
           """Load configuration for a specific environment."""
           if environment is None:
               environment = os.getenv("ENVIRONMENT", "development")
           
           # Load base configuration
           base_config = self.config_dir / "base.yaml"
           if base_config.exists():
               with open(base_config) as f:
                   self.config = yaml.safe_load(f)
           
           # Load environment-specific configuration
           env_config = self.config_dir / f"{environment}.yaml"
           if env_config.exists():
               with open(env_config) as f:
                   env_settings = yaml.safe_load(f)
                   self._merge_config(self.config, env_settings)
           
           # Override with environment variables
           self._override_from_env()
           
           return self.config
       
       def _merge_config(self, base: dict, override: dict):
           """Recursively merge configuration dictionaries."""
           for key, value in override.items():
               if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                   self._merge_config(base[key], value)
               else:
                   base[key] = value
       
       def _override_from_env(self):
           """Override configuration with environment variables."""
           env_mappings = {
               "LOG_LEVEL": "system.log_level",
               "VERBOSE": "system.verbose",
               "CACHE_ENABLED": "system.cache_enabled",
               "SIMILARITY_THRESHOLD": "tools.rag.similarity_threshold",
               "MAX_RESULTS": "tools.rag.max_results"
           }
           
           for env_var, config_path in env_mappings.items():
               env_value = os.getenv(env_var)
               if env_value is not None:
                   self._set_nested_value(config_path, env_value)
       
       def _set_nested_value(self, path: str, value):
           """Set a nested configuration value."""
           keys = path.split('.')
           current = self.config
           
           for key in keys[:-1]:
               if key not in current:
                   current[key] = {}
               current = current[key]
           
           # Convert string values to appropriate types
           if isinstance(value, str):
               if value.lower() in ('true', 'false'):
                   value = value.lower() == 'true'
               elif value.isdigit():
                   value = int(value)
               elif value.replace('.', '').isdigit():
                   value = float(value)
           
           current[keys[-1]] = value
   
   # Usage
   config_manager = ConfigManager()
   config = config_manager.load_config("production")
   
   print(f"Log level: {config['system']['log_level']}")
   print(f"Similarity threshold: {config['tools']['rag']['similarity_threshold']}")

Testing Examples
----------------

Unit Tests
^^^^^^^^^^

.. code-block:: python

   import unittest
   from unittest.mock import Mock, patch
   from search_flow.tools.rag import RAGTool
   from search_flow.main import SearchFlow, SearchState
   
   class TestRAGTool(unittest.TestCase):
       def setUp(self):
           self.rag_tool = RAGTool()
       
       def test_rag_tool_initialization(self):
           """Test RAG tool initialization."""
           self.assertEqual(self.rag_tool.name, "rag_search_tool")
           self.assertIn("medical document", self.rag_tool.description.lower())
       
       def test_rag_tool_input_validation(self):
           """Test input validation."""
           # Valid input
           self.assertTrue(self.rag_tool._validate_input("diabetes symptoms"))
           
           # Invalid inputs
           self.assertFalse(self.rag_tool._validate_input(""))
           self.assertFalse(self.rag_tool._validate_input(None))
           self.assertFalse(self.rag_tool._validate_input(123))
   
   class TestSearchFlow(unittest.TestCase):
       def setUp(self):
           self.flow = SearchFlow()
       
       def test_search_state_initialization(self):
           """Test SearchState initialization."""
           self.assertEqual(self.flow.state.question, "")
           self.assertEqual(self.flow.state.type, "")
           self.assertEqual(self.flow.state.result, "")
       
       @patch('search_flow.main.LLM')
       def test_intent_detection_medical(self, mock_llm):
           """Test medical intent detection."""
           # Mock LLM response
           mock_llm_instance = Mock()
           mock_llm_instance.call.return_value = "medicina"
           mock_llm.return_value = mock_llm_instance
           
           # Test medical query
           self.flow.state.question = "What are diabetes symptoms?"
           result = self.flow.detect_field()
           
           self.assertEqual(result.type, "medicina")
       
       @patch('search_flow.main.LLM')
       def test_intent_detection_general(self, mock_llm):
           """Test general intent detection."""
           # Mock LLM response
           mock_llm_instance = Mock()
           mock_llm_instance.call.return_value = "altro"
           mock_llm.return_value = mock_llm_instance
           
           # Test general query
           self.flow.state.question = "What's the weather like?"
           result = self.flow.detect_field()
           
           self.assertEqual(result.type, "altro")
   
   if __name__ == '__main__':
       unittest.main()

Integration Tests
^^^^^^^^^^^^^^^^

.. code-block:: python

   import pytest
   from search_flow.main import SearchFlow
   from search_flow.tools.rag import RAGTool
   from search_flow.tools.ddg_search import DuckDuckGoSearchTool
   
   class TestIntegration:
       @pytest.fixture
       def search_flow(self):
           """Create a SearchFlow instance for testing."""
           return SearchFlow()
       
       @pytest.fixture
       def rag_tool(self):
           """Create a RAGTool instance for testing."""
           return RAGTool()
       
       @pytest.fixture
       def ddg_tool(self):
           """Create a DuckDuckGoSearchTool instance for testing."""
           return DuckDuckGoSearchTool()
       
       def test_complete_medical_flow(self, search_flow):
           """Test complete medical query flow."""
           # Set medical question
           search_flow.state.question = "What are the symptoms of diabetes?"
           
           # Run intent detection
           result = search_flow.detect_field()
           assert result.type == "medicina"
           
           # Test routing
           route = search_flow.route_field()
           assert route == "medicina"
       
       def test_complete_general_flow(self, search_flow):
           """Test complete general query flow."""
           # Set general question
           search_flow.state.question = "What's the latest news?"
           
           # Run intent detection
           result = search_flow.detect_field()
           assert result.type == "altro"
           
           # Test routing
           route = search_flow.route_field()
           assert route == "altro"
       
       def test_tool_integration(self, rag_tool, ddg_tool):
           """Test tool integration and basic functionality."""
           # Test RAG tool
           rag_result = rag_tool.run("test medical query")
           assert isinstance(rag_result, str)
           
           # Test DuckDuckGo tool
           ddg_result = ddg_tool.run("test web query")
           assert isinstance(ddg_result, str)

Performance Testing
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import time
   import statistics
   from search_flow.main import SearchFlow
   
   class PerformanceTester:
       def __init__(self):
           self.flow = SearchFlow()
           self.results = []
       
       def test_query_performance(self, query: str, iterations: int = 10):
           """Test performance of a specific query."""
           times = []
           
           for i in range(iterations):
               start_time = time.time()
               
               try:
                   self.flow.state.question = query
                   result = self.flow.detect_field()
                   
                   end_time = time.time()
                   execution_time = end_time - start_time
                   times.append(execution_time)
                   
                   print(f"Iteration {i+1}: {execution_time:.3f}s")
                   
               except Exception as e:
                   print(f"Error in iteration {i+1}: {e}")
           
           if times:
               stats = {
                   'min': min(times),
                   'max': max(times),
                   'mean': statistics.mean(times),
                   'median': statistics.median(times),
                   'std': statistics.stdev(times) if len(times) > 1 else 0
               }
               
               print(f"\nPerformance Statistics:")
               for key, value in stats.items():
                   print(f"{key.capitalize()}: {value:.3f}s")
               
               return stats
           
           return None
       
       def benchmark_different_queries(self, queries: list, iterations: int = 5):
           """Benchmark different types of queries."""
           benchmark_results = {}
           
           for query in queries:
               print(f"\nBenchmarking: {query}")
               print("=" * 50)
               
               stats = self.test_query_performance(query, iterations)
               if stats:
                   benchmark_results[query] = stats
           
           return benchmark_results
   
   # Usage
   tester = PerformanceTester()
   
   # Test queries
   test_queries = [
       "What are diabetes symptoms?",
       "Latest news about AI",
       "How to treat hypertension?",
       "Weather forecast for Rome"
   ]
   
   # Run benchmarks
   results = tester.benchmark_different_queries(test_queries, iterations=5)
   
   # Print summary
   print("\n" + "="*60)
   print("BENCHMARK SUMMARY")
   print("="*60)
   
   for query, stats in results.items():
       print(f"\nQuery: {query}")
       print(f"Average time: {stats['mean']:.3f}s")
       print(f"Best time: {stats['min']:.3f}s")
       print(f"Worst time: {stats['max']:.3f}s")

For more advanced examples and use cases, see the :doc:`development` section.
