# HomeMatch Real Estate Listings App

## Overview

HomeMatch is an AI-powered real estate platform that provides personalized property recommendations by leveraging advanced natural language processing and vector search capabilities. The system intelligently matches user preferences with property listings using semantic search and generates customized property descriptions.

This IPython Notebook provides a streamlined, end-to-end pipeline for generating, processing, and presenting personalized real estate listings using cutting-edge tools like LangChain and OpenAI. It covers data generation, embedding listings into a vector database, enabling efficient semantic search, and delivering personalized recommendations via an interactive widget.

---

## Key Features

### 🏠 Intelligent Property Generation

* Automatically creates realistic and diverse real estate listings using OpenAI's language models.
* Generates comprehensive property details including neighborhood descriptions, pricing, specifications, and detailed descriptions.
* Produces varied property types to simulate a realistic real estate market.

### 🔍 Semantic Search & Matching

* Converts property listings into high-dimensional vector embeddings using OpenAI's embedding models.
* Stores embeddings in ChromaDB vector database for fast, semantic-based property retrieval.
* Enables natural language queries that understand user intent beyond exact keyword matching.

### 🎯 Personalized Recommendations

* Processes user preferences written in natural language.
* Transforms casual requests into structured, searchable queries.
* Generates personalized property descriptions that highlight features most relevant to user preferences.
* Handles budget constraints intelligently, acknowledging limitations while presenting alternatives.

### 🛠 Modular Architecture

* Core functionality encapsulated in a reusable `services.py` module.
* Clean separation of concerns for maintainability and extensibility.
* Easy integration with web interfaces or other applications.

### Interactive Widget
The widget provides a **complete testing and demonstration environment** for validating search quality, personalization effectiveness, and showcasing the platform's AI capabilities to stakeholders.

---

## Technical Architecture

```
User Input → Preference Processing → Vector Search → Result Personalization → Output
     ↓              ↓                    ↓                ↓
Natural Language → Structured Query → ChromaDB → Customized Descriptions
```

**Components:**

* **OpenAI API:** Powers listing generation, preference processing, and description personalization.
* **ChromaDB:** Vector database for embedding storage and semantic search.
* **LangChain:** Framework for chaining AI operations and managing embeddings.
* **Python Services:** Core business logic and data management.

---

## Setup & Installation

### Environment Configuration

An OpenAI API Key is required to access the AI models. Place your API key in the `key.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1  
```

### Required Dependencies

Ensure the following packages are installed (see `requirements.txt`):

* langchain==0.0.305
* openai==0.28.1
* pydantic>=1.10.12
* pytest>=7.4.0
* sentence-transformers>=2.2.0
* transformers>=4.31.0
* chromadb==0.4.12
* jupyter==1.0.0
* tiktoken==0.4.0
* ipywidgets>=8.0.0

---

## Project Structure

```
/
├── HomeMatch.ipynb        # Main Jupyter notebook demonstrating the end-to-end pipeline
├── app.py                 # Entrypoint script to launch the application or run scripts
├── key.env                # Environment variables file containing API keys
├── listings.json          # Sample or generated real estate listings dataset
├── requirements.txt       # Python dependencies for the project
├── services.py            # Core business logic (listing generation, search, personalization)
└── tester.py              # Test scripts to validate functionalities and workflows
```

* **`HomeMatch.ipynb`**: Interactive notebook that guides you through generating, searching, and personalizing listings.
* **`app.py`**: Script to run the application, potentially a CLI or server startup.
* **`key.env`**: Store sensitive API keys securely, loaded at runtime.
* **`listings.json`**: Data file with property listings used for embeddings and search.
* **`requirements.txt`**: Lists Python package dependencies with pinned versions.
* **`services.py`**: Implements main logic such as LLM calls, JSON parsing, embedding management, and personalized descriptions.
* **`tester.py`**: Contains automated or manual tests for verifying different parts of the system.

---

## 📱 Interactive Testing Widget

* **Real-time Query Interface**: Test search functionality with natural language queries and immediate visual feedback
* **Pre-built Test Scenarios**: One-click example queries covering family homes, luxury properties, budget constraints, and investment opportunities
* **Dual-mode Results**: View both original property listings and AI-generated personalized descriptions side-by-side
* **Configurable Testing**: Adjustable result limits and scrollable output area for comprehensive result analysis
* **Development Tools**: Built-in error handling, clear functionality, and step-by-step workflow visualization for debugging and refinement

### Simple Setup
**Import your HomeMatch app and the tester**
<br>
```
    from services import HomeMatchApp
   
    from tester import create_simple_tester
```
<br>

**Initialize your app**
<br>
```
    app = HomeMatchApp(api_key="your-openai-key")
    
    app.load_listings("listings.json")  # or generate new one
```
<br>

**Create and display the tester interface**
<br>
```
    tester = create_simple_tester(app)
```

### Quick Setup

**This handles app creation, data loading, and tester display**
<br>
```
    from tester import quick_test_setup

    app, tester = quick_test_setup(
        api_key="your-openai-key",
        generate_new=False  # Set to True to generate fresh listings
    )
```
---


## 📄 License
[License](./LICENSE.txt)
