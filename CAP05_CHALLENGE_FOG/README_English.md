# InternetWhisper Orchestrator

## Project Description

This directory contains the **Orchestrator** service for the InternetWhisper project. The Orchestrator is a FastAPI-based backend that coordinates search, retrieval, and context generation for user queries. It integrates with external APIs (Google Custom Search, OpenAI), a Redis vector cache, and a scraping service to provide relevant, context-rich responses to user questions.

## Technical Explanation

The Orchestrator service is responsible for:
- Accepting user queries via a REST API.
- Searching the web using Google Custom Search API.
- Scraping and parsing web pages for relevant content.
- Splitting and embedding text using OpenAI or remote embedding services.
- Caching and retrieving document embeddings in Redis for efficient similarity search.
- Streaming responses to the frontend using Server-Sent Events (SSE).
- Formatting context and generating prompts for LLMs (e.g., OpenAI GPT).

**Key Components:**
- `main.py`: FastAPI application entry point. Handles incoming requests, orchestrates retrieval, and streams responses.
- `retrieval/`: Contains modules for search, scraping, embeddings, caching, and text splitting.
- `models/`: Pydantic models for structured data (documents, search results).
- `util/`: Utility modules, including logging configuration.
- `prompt/`: Prompt templates for LLMs.
- `mocks/`: Mock data for development/testing.

## Environment Variables

The Orchestrator relies on several environment variables for API keys and configuration. Copy `.env.example` to `.env` and fill in the required values:

sh
cp [.env.example](http://_vscodecontentref_/0) .env

- Edit .env and set the following variables:

- HEADER_ACCEPT_ENCODING: HTTP header for encoding (default: "gzip").
- HEADER_USER_AGENT: HTTP header for user agent string.
- GOOGLE_API_HOST: Google Custom Search API endpoint.
- GOOGLE_FIELDS: Fields to retrieve from Google API.
- GOOGLE_API_KEY: Your Google Custom Search API key.
- GOOGLE_CX: Your Google Custom Search Engine ID.
- OPENAI_API_KEY: Your OpenAI API key.


**Running the Application Locally**
Prerequisites
- Docker and Docker Compose
- API keys for Google Custom Search and OpenAI

Steps
1. Clone the repository and navigate to the project directory.
2. Configure environment variables:
    Copy .env.example to .env and fill in your API keys and configuration.
3. Build and start the services:
    docker-compose up --build

This will start the following services:
-   orchestrator: The FastAPI backend (this directory).
-   frontend: The Streamlit frontend.
-   cache: Redis vector database.

4. Access the API and frontend:
Orchestrator API: http://localhost:8000
Frontend UI: http://localhost:8501

**OpenAPI Definition**
The Orchestrator exposes the following API endpoint:

GET /streamingSearch
**Description:**
Streams search and context results for a given query using Server-Sent Events (SSE).

Query Parameters:
query (string, required): The user query to search and retrieve context for.

**Response:**
A stream of events, including:

- search: JSON with search results.
- context: Aggregated context text.
- prompt: The prompt sent to the LLM.
- token: Incremental LLM response tokens.

**Example Request:**
- `GET /streamingSearch?query=What is LangChain?`
Accept: text/event-stream

Example Response (SSE):
event: search
data: {"items": [...]}

event: context
data: "Relevant context text..."

event: prompt
data: "Prompt sent to LLM..."

event: token
data: "First part of the answer..."

event: token
data: "Next part of the answer..."

`The full OpenAPI schema is available at http://localhost:8000/docs when the service is running.`

