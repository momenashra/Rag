[![Test Multiple Python Versions](https://github.com/momenashra/Rag/actions/workflows/my-workflow.yml/badge.svg)](https://github.com/momenashra/Rag/actions/workflows/my-workflow.yml)

# Multimodal RAG Application with Web Dev Environment

![ci-cd](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*QPH4dpcdC-BwA_eQykLu2Q.png)
---

## Overview

This project is a modular, scalable Retrieval-Augmented Generation (RAG) platform, designed for advanced document indexing, semantic search, and NLP workflows. Built with FastAPI, SQLAlchemy, and modern vector database integrations, it supports both local and cloud-based development environments, including Colab and GitHub Codespaces.

---

## Latest Features

### Summary Memory System
- Context-aware conversation history
- Intelligent summary storage and retrieval
- Project-specific conversation tracking
- Enhanced context management for better responses

### Enhanced RAG Capabilities
- Improved context retrieval with summary integration
- Better conversation continuity
- More comprehensive document processing
- Advanced template system for context management

### Security & Configuration
- Improved environment file handling
- Enhanced configuration management
- Better secret handling
- Streamlined deployment process

---

## Create a Project Scaffold

* Create a development environment that is cloud-based

### Colab Notebook

* **Project:** Machine Learning and Deep Learning Models for Predicting Sales in 3 Different Cities
* **Project Description:** This project uses machine learning algorithms to predict sales for retail products based on historical data. The model leverages various features such as product category, location, and time of year.
* **Technologies Used:**  
  [requirements.txt](https://github.com/momenashra/Rag/blob/main/requirements.txt)

### Github Codespaces

Build out python project scaffold:
* Makefile
* requirements.txt
* test_library.py
* Dockerfile
* Command-line tool
* Microservice (FastAPI + Uvicorn)
* Ngrok
* Qdrant
* MongoDB

---

## Setup Environment Variables

```bash
cp .env.example .env
```
- Update `.env` with your credentials and API keys.

---

## Run Docker Compose Services

```bash
cd docker
cp .env.example .env
```
- Update `.env` with your credentials.

---

## Local Development

1. **Create Virtual Environment**
   ```bash
   conda create -n mini-rag
   ```
2. **Activate Environment**
   ```bash
   conda activate mini-rag
   ```
3. **Clone the Repository**
   ```bash
   git clone https://github.com/momenashra/RAG.git
   ```
4. **go to docker**
   ```bash
   cd docker/
   ```
5. **Run the App**
   ```bash
   docker compose up -d
   ```
6. **Open in browser**
   ```
   http://localhost:8000/
   ```
7. **open postman**
   use api end points after setup request settings in postman by adding api variable
    initial value 'http://127.0.0.1:8000'
7. **Upload a Test File** (e.g., `test.pdf`)
8. **Execute and You're Done!**

---

## Features

- FastAPI-based API for high-performance, asynchronous request handling
- Modular OOP design: clear separation of models, controllers, routes, and helpers
- SQLAlchemy ORM for robust database interactions
- Vector database integration (e.g., Qdrant, MongoDB) for semantic search
- LLM support for text generation and embedding
- Extensible controllers for NLP and data processing
- Comprehensive Enum usage for maintainable code
- Environment-based configuration for easy deployment and scaling
- Docker & Codespaces ready for rapid development and deployment
- Advanced summary memory system for context-aware conversations
- Enhanced RAG capabilities with improved context management
- Secure configuration and environment management

---

## Architecture

- **Routers:** Organize API endpoints for base, data, and NLP operations.
- **Models:** Encapsulate business logic and database operations for Projects, Assets, and Data Chunks.
- **Controllers:** Orchestrate complex workflows, such as NLP tasks and vector database operations.
- **Stores:** Manage connections to LLM providers and vector databases.
- **Helpers:** Provide configuration and utility functions.
- **Memory System:** Manages conversation history and context through summaries.

---

## API Endpoints

- `GET /api/v1/` — Welcome endpoint
- `POST /api/v1/nlp/index/push/{project_id}` — Index project data into vector DB
- `GET /api/v1/nlp/index/info/{project_id}` — Get vector DB collection info
- `POST /api/v1/nlp/index/search/{project_id}` — Semantic search in indexed data
- `POST /api/v1/nlp/index/answer/{project_id}` — RAG-based question answering with context awareness

---

## Example Use Cases

- **Document Indexing:** Efficiently index and manage large collections of documents.
- **Semantic Search:** Retrieve relevant information using vector-based search.
- **Question Answering:** Leverage LLMs for advanced Q&A over your data.
- **Contextual Conversations:** Maintain conversation context through intelligent summary management.
- **Project-Specific Knowledge:** Track and utilize project-specific conversation history.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PlantUML](https://plantuml.com/)
- [TQDM](https://tqdm.github.io/)
