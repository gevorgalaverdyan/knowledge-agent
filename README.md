# Knowledge Assistant

This project is a Knowledge Assistant application designed to help users understand their Tax-Free Savings Account (TFSA) contribution room and general guidelines. It leverages a RAG (Retrieval-Augmented Generation) system and an LLM Agent to provide accurate answers and calculations based on CRA (Canada Revenue Agency) guidelines.

## Project Structure

The codebase is organized as a monorepo with the following structure:

- **apps/backend**: The Python-based backend API and LLM logic.
- **apps/frontend**: The Angular-based frontend user interface.
- **scripts**: Utility scripts for database setup and seeding.

## Backend

The backend is built with **FastAPI** and serves as the core intelligence of the application. It handles chat sessions, message history, and interacts with the LLM.

### API Endpoints

The following API endpoints are available:

- **General**
  - `GET /`: Health check endpoint. Returns `{"message": "Server is running"}`.

- **Chat Operations**
  - `GET /chat/chats`: Fetch all existing chat sessions.
  - `POST /chat/create`: Create a new chat session. Requires a `title`.
  - `GET /chat/{chat_id}/messages`: Retrieve the message history for a specific chat session.
  - `POST /chat/{chat_id}/message`: Send a user message to the chat. This triggers the LLM agent flow and returns the AI's response.

### LLM Agent & Flow

The application uses a specialized agent, `TFSAAagent`, to determine the best way to answer a user's question. The flow is as follows:

1.  **Receive Question**: The backend receives a user question via the `/chat/{chat_id}/message` endpoint.
2.  **Agent Evaluation**: The `TFSAAagent` analyzes the question to decide if a specific tool is needed.
    - **Tool Usage (TFSA Calculator)**: If the question is about "contribution" room, the agent attempts to extract the year the user turned 18.
        - It calls the `calculate_tfsa_contribution_room` tool to compute the total contribution limit based on yearly limits since 2009.
        - It simultaneously retrieves relevant CRA sections using the vector store.
        - The calculation result and context are passed to the LLM to generate a detailed response.
    - **Standard RAG**: If no specific tool is triggered, the system falls back to a standard Retrieval-Augmented Generation (RAG) flow.
        - It searches the vector database (`tfsa.faiss`) for relevant chunks of the CRA guide.
        - It constructs a prompt with these chunks and the user's question.
3.  **LLM Generation**: The constructed prompt (with either tool results or RAG context) is sent to the **Gemini** LLM to generate the final natural language response.
4.  **Response**: The answer is saved to the database and returned to the user.

### Key Components

- **Agents**: Located in `apps/backend/agents/`, specifically `tfsa_agent.py`.
- **Tools**: Custom tools like `calculations.py` for TFSA math and `retrieval.py` for context fetching.
- **RAG**: Implements ingestion and retrieval logic using FAISS and embeddings.

## Frontend

The frontend is a modern web application built with **Angular 21**.

- **Tech Stack**: Angular, Tailwind CSS, `ngx-markdown`.
- **Features**:
    - Clean chat interface.
    - Markdown rendering for rich text responses.
    - Component-based architecture (Chat, Message, Input components).

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local backend dev)
- Node.js & npm (for local frontend dev)

### Running with Docker

The easiest way to run the entire stack is using Docker Compose:

```bash
docker-compose up --build
```

### Local Development

**Backend:**

```bash
cd apps/backend
pip install -r requirements.txt
./runme.sh
```

**Frontend:**

```bash
cd apps/frontend
npm install
npm start
```
