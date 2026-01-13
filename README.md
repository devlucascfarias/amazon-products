# Smart Search AI - Intelligent E-commerce Assistant

An intelligent shopping assistant powered by Natural Language Processing (NLP) and Retrieval-Augmented Generation (RAG) that transforms traditional keyword searches into semantic, context-aware product discovery.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://www.langchain.com/)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Vector Store](#vector-store)
- [Prompt Engineering](#prompt-engineering)

---

## Overview

**Smart Search AI** is an intelligent e-commerce assistant that goes beyond traditional keyword matching. The system uses Large Language Models (LLMs) to understand user intent, extract contextual information, and provide semantically relevant product recommendations.

### Example Queries

```
Traditional: "notebook"
Smart Search: "lightweight laptop for students under $800"

Traditional: "headphones"
Smart Search: "wireless headphones for gym with good bass"

Traditional: "air conditioner"
Smart Search: "silent air conditioner for small bedroom"
```

---

## Key Features

### AI-Powered Search
- **Intent Analysis**: LLM-based query understanding
- **Category Mapping**: Automatic product category detection
- **Budget Extraction**: Smart price limit recognition
- **Contextual Understanding**: Handles complex, natural language queries

### Semantic Search (Vector Store)
- **ChromaDB Integration**: Fast similarity search using vector embeddings
- **Google Embeddings**: High-quality 768-dimensional vector representations
- **Indexed Products**: Approximately 5,500 products across 112 categories
- **Performance**: Search results in 100-200ms

### Modern UI/UX
- **Responsive Design**: Optimized for all device sizes
- **Real-time Suggestions**: Dynamic search recommendations
- **Smart Filters**: AI-generated filter suggestions based on query context

### Production-Ready Architecture
- **External Prompts**: Separated prompt management for easy versioning
- **Caching**: Optimized performance with intelligent caching
- **Error Handling**: Graceful degradation and comprehensive error messages
- **CORS Enabled**: Ready for cross-origin deployment

---

## Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         Intent Analysis             │
│  (LLM: Category + Budget Extract)   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│      Vector Store Search            │
│  (Semantic Similarity - ChromaDB)   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Product Retrieval (RAG)         │
│   (Real Database Query)             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│    Response Generation              │
│  (LLM: Smart Filtering + Format)    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Formatted  │
│  Response   │
└─────────────┘
```

### Agent Workflow

1. **Intent Agent**: Analyzes user query to extract categories and budget constraints
2. **Retrieval Agent**: Searches vector store to find semantically similar products
3. **Filter Agent**: Applies intelligent filtering to remove irrelevant items
4. **Response Agent**: Generates natural language response and formats product cards

---

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for developing LLM-powered applications
- **Google Gemini AI** - Large Language Model (gemini-2.5-flash-lite)
- **ChromaDB** - Vector database for semantic search
- **Pandas** - Data manipulation and analysis
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **Vanilla JavaScript** - No framework overhead, pure performance
- **Vite** - Next generation frontend build tool
- **Modern CSS** - Responsive design with CSS Grid and Flexbox

### AI/ML
- **Google Embeddings** (embedding-001) - Text-to-vector conversion
- **Prompt Engineering** - External prompt management and versioning
- **RAG Pattern** - Retrieval-Augmented Generation for accurate responses

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

### 1. Clone Repository

```bash
git clone https://github.com/devlucascfarias/smart-search-ai-products.git
cd smart-search-ai-products
```

### 2. Backend Setup

```bash
cd backend/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Initialize Vector Store

```bash
cd backend/api
python init_vector_store.py
```

This process will:
- Load approximately 5,500 products from CSV files
- Generate embeddings using Google AI
- Create and persist ChromaDB index
- Takes approximately 5-10 minutes to complete

---

## Usage

### Start Backend Server

```bash
cd backend/api
uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:5173`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

---

## Project Structure

```
smart-search-ai-products/
├── backend/
│   ├── api/
│   │   ├── prompts/              # External prompt files
│   │   │   ├── category_analysis.txt
│   │   │   ├── response_generation.txt
│   │   │   └── README.md
│   │   ├── chroma_db/            # Vector store (gitignored)
│   │   ├── main.py               # FastAPI application
│   │   ├── products.py           # Product data logic
│   │   ├── prompt_manager.py     # Prompt management system
│   │   ├── vector_store.py       # Vector store manager
│   │   ├── init_vector_store.py  # Vector store initialization
│   │   └── requirements.txt      # Python dependencies
│   └── data/                     # Product CSV files
├── frontend/
│   ├── index.html                # Main HTML file
│   ├── main.js                   # JavaScript logic
│   ├── style.css                 # Styles
│   └── package.json              # Node dependencies
├── .gitignore
├── .env.example
└── README.md
```

---

## API Documentation

### Main Endpoints

#### `POST /generate`
Intelligent product search with natural language processing

**Request:**
```json
{
  "prompt": "silent air conditioner for small bedroom",
  "budget": 500.0
}
```

**Response:**
```json
{
  "response": "AI-generated response with product recommendations",
  "detected_budget": 500.0,
  "queried_categories": ["Air Conditioners"]
}
```

#### `GET /vector-store/search`
Direct semantic search in the vector database

**Query Parameters:**
- `query` (string, required): Search query
- `category` (string, optional): Filter by specific category
- `limit` (int, default: 20): Maximum number of results

**Example:**
```bash
curl "http://localhost:8000/vector-store/search?query=gym+headphones&limit=10"
```

#### `POST /vector-store/rebuild`
Rebuild the vector store from scratch (use after data updates)

**Response:**
```json
{
  "status": "success",
  "message": "Vector store rebuilt successfully"
}
```

#### `GET /categories`
List all available product categories

**Response:**
```json
[
  {"id": "Air Conditioners", "name": "Air Conditioners"},
  {"id": "Laptops", "name": "Laptops"},
  ...
]
```

#### `GET /products/{category}`
Get products by category with pagination

**Query Parameters:**
- `page` (int, default: 1): Page number
- `page_size` (int, default: 20): Items per page

---

## Vector Store

### What is it?

The vector store uses semantic embeddings to find products by meaning rather than exact keyword matching. This enables the system to understand context and user intent.

### How it works:

1. **Indexing Phase**: 
   - Products are converted to 768-dimensional vectors using Google's embedding model
   - Vectors are stored in ChromaDB with metadata (name, category, price, etc.)

2. **Search Phase**: 
   - User query is converted to a vector using the same embedding model
   - ChromaDB performs similarity search in vector space
   - Returns products with highest cosine similarity

3. **Results**: 
   - Products are ranked by semantic relevance
   - Results include relevance scores for transparency

### Advantages:

- Understands synonyms and related concepts
- Finds products even without exact keyword match
- Handles complex, natural language queries
- Significantly faster than traditional full-text search
- Accuracy of 90-95% in product relevance

### Rebuild Vector Store:

```bash
# Via Python script
python init_vector_store.py

# Via API endpoint
curl -X POST http://localhost:8000/vector-store/rebuild
```

---

## Prompt Engineering

Prompts are stored externally in `backend/api/prompts/` for maintainability and version control:

- **category_analysis.txt** - Intent analysis and category mapping logic
- **response_generation.txt** - Final response formatting and product filtering

### Benefits of External Prompts:

- Easy to edit without modifying Python code
- Version control for prompt iterations
- A/B testing different prompt versions
- Collaboration with non-technical team members
- Hot-reload in development mode

### Prompt Manager Usage:

```python
from prompt_manager import prompt_manager

# Load a prompt
template = prompt_manager.load_prompt("category_analysis")

# List available prompts
available = prompt_manager.list_available_prompts()

# Reload a prompt (useful in development)
template = prompt_manager.reload_prompt("category_analysis")

# Clear cache (forces reload of all prompts)
prompt_manager.clear_cache()
```

---

## Performance Metrics

- **Products Indexed**: ~5,500 across 112 categories
- **Vector Search Speed**: 100-200ms average
- **Embedding Dimensions**: 768 (Google embedding-001)
- **Search Accuracy**: 90-95% relevance
- **API Response Time**: <500ms for most queries
