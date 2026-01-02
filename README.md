# Knowledge Assistant

This project is a Knowledge Assistant application designed to help users understand their Tax-Free Savings Account (TFSA) contribution room and general guidelines. It leverages a RAG (Retrieval-Augmented Generation) system and an LLM Agent to provide accurate answers and calculations based on CRA (Canada Revenue Agency) guidelines.

## Project Structure

The codebase is organized as a monorepo with the following structure:

- **apps/backend**: The Python-based backend API built with FastAPI and LLM logic powered by Google Gemini.
- **apps/frontend**: The Angular 21-based frontend user interface with server-side rendering (SSR) support.
- **scripts**: Utility scripts for database setup, seeding, and container management.
- **docker-compose.yml**: Docker orchestration for running the full stack (PostgreSQL, backend, frontend).

## Backend

The backend is built with **FastAPI** and serves as the core intelligence of the application. It handles chat sessions, message history, and interacts with the **Google Gemini** LLM via the `google-genai` library.

### Key Technologies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations  
- **PostgreSQL**: Primary database with UUID extension support
- **FAISS**: Vector database for efficient similarity search
- **Auth0**: Authentication and authorization via JWT tokens
- **Google Gemini**: LLM provider for generating responses and embeddings

### API Endpoints

The following API endpoints are available:

#### General
- `GET /`: Health check endpoint. Returns `{"message": "Server is running"}`.

#### User Operations
- `GET /user/profile`: Fetch authenticated user profile information. Requires Auth0 JWT token.

#### Chat Operations
- `GET /chat/chats`: Fetch all chat sessions for the authenticated user.
- `POST /chat/create`: Create a new chat session. Requires a `title` parameter.
- `DELETE /chat/{chat_id}/delete`: Delete a specific chat session and all its messages.
- `GET /chat/{chat_id}/messages`: Retrieve the complete message history for a specific chat session.
- `POST /chat/{chat_id}/message`: Send a user message to the chat. This triggers the LLM agent flow and returns the AI's response.

**Note:** All chat and user endpoints require Auth0 authentication tokens.

### LLM Agent & Flow

The application uses a specialized agent, `TFSAAgent`, to intelligently determine the best way to answer a user's question. The flow is as follows:

1. **Receive Question**: The backend receives a user question via the `POST /chat/{chat_id}/message` endpoint.

2. **Message Storage**: The user's question is saved to the database with `MessageSenderType.USER`.

3. **Initial Retrieval**: The system performs a vector similarity search in the FAISS index to find relevant CRA document chunks.

4. **Agent Evaluation**: The `TFSAAgent` analyzes the question to decide if specialized tool usage is needed:
   
   **Scenario A: TFSA Contribution Calculation Tool**
   - **Trigger**: Questions containing the keyword "contribution"
   - **Process**:
     1. Extracts the year the user turned 18 from the question using `extract_year()` utility
     2. If year cannot be extracted, returns an error requesting the user specify the year
     3. Calls `calculate_tfsa_contribution_room()` to compute total contribution room
     4. Calculation includes yearly breakdown from 2009 (or year turned 18) through current year
     5. Retrieves relevant CRA sections simultaneously using `find_relevant_sections()`
     6. Returns a `CalculationAnswer` containing both calculation results and supporting context
   
   **Scenario B: Standard RAG (Retrieval-Augmented Generation)**
   - **Trigger**: All other questions (no specific tool needed)
   - **Process**:
     1. Uses previously retrieved chunks from vector search
     2. If no relevant chunks found, returns a "No relevant CRA sections found" message
     3. Retrieves the last 5 messages for conversation context
     4. Constructs a context-aware prompt with retrieved chunks and chat history

5. **LLM Generation**: The constructed prompt (with either tool results or RAG context) is sent to **Google Gemini** to generate the final natural language response.

6. **Response Storage & Return**: The AI-generated answer is saved to the database with `MessageSenderType.SYSTEM` and returned to the user.

### TFSA Contribution Room Calculation

The calculator includes yearly contribution limits from 2009 through 2025:
- **2009-2012**: $5,000/year
- **2013-2014**: $5,500/year  
- **2015**: $10,000 (one-time increase)
- **2016-2018**: $5,500/year
- **2019-2022**: $6,000/year
- **2023**: $6,500
- **2024-2025**: $7,000/year

**Assumptions:**
- Canadian resident for all eligible years
- No prior TFSA contributions made
- No withdrawals made
- Calculations start from the year turned 18 or 2009 (whichever is later)

### Key Components

- **Agents**: `apps/backend/app/agents/tfsa_agent.py` - Contains the `TFSAAgent` class for intelligent routing
- **Tools**: 
  - `apps/backend/app/tools/calculations.py` - TFSA contribution room calculator with yearly limits
  - `apps/backend/app/tools/retrieval.py` - Vector database search for relevant CRA sections
- **RAG System**:
  - `apps/backend/app/rag/ingest.py` - Document ingestion and embedding generation
  - `apps/backend/app/rag/retriever.py` - FAISS-based similarity search
  - `apps/backend/app/rag/ask.py` - Orchestrates agent and LLM interaction
  - `apps/backend/app/rag/prompt.py` - Prompt engineering and context building
- **Database Models**:
  - `apps/backend/app/models/user.py` - User account management
  - `apps/backend/app/models/chat.py` - Chat session tracking  
  - `apps/backend/app/models/message.py` - Message history with sender type
- **Authentication**: `apps/backend/app/core/auth.py` - Auth0 integration with automatic user provisioning

## Frontend

The frontend is a modern web application built with **Angular 21** and optimized for both client-side and server-side rendering.

### Tech Stack

- **Angular 21**: Latest Angular framework with standalone components
- **Angular SSR**: Server-side rendering for improved performance and SEO
- **Tailwind CSS 4**: Utility-first CSS framework for styling
- **ngx-markdown**: Markdown rendering with support for code highlighting
- **Auth0 Angular SDK**: Seamless authentication integration with JWT interceptors
- **Lucide Angular**: Modern icon library
- **RxJS**: Reactive programming for state management
- **Express**: Node.js server for SSR

### Key Features

- **Modern UI/UX**: Clean, responsive chat interface built with custom component library
- **Markdown Support**: Rich text rendering for formatted AI responses including code blocks
- **Authentication**: Auth0-powered authentication with automatic token management
- **Dark Mode**: Theme switching capability (configured via `dark-mode.ts` service)
- **Component Architecture**: Reusable UI components including:
  - Button, Card, Dialog components
  - Input and InputGroup for form controls
  - Message component with sender-specific styling
  - Navbar with authentication status
  - Loader and Skeleton states for better UX
- **HTTP Interceptors**: Automatic Auth0 token injection for API requests
- **Services**:
  - `chat.service.ts`: Chat session and message management
  - `user.service.ts`: User profile operations
  - `message.service.ts`: Message handling utilities

### Port Configuration

- **Development**: `http://localhost:4200`
- **Docker (Production)**: `http://localhost:4200` (mapped from internal port 8080 via nginx)

## Database

The application uses **PostgreSQL** as its primary database with the following setup:

- **UUID Extension**: Automatically installed via `uuid-ossp` for UUID primary keys
- **Tables**: Automatically created via SQLAlchemy on application startup
  - **users**: Stores Auth0 user information
  - **chats**: Chat session metadata with foreign key to users
  - **messages**: Message history with sender type (USER/SYSTEM) and foreign key to chats
- **Docker Volume**: Persistent storage mounted at `/var/lib/postgresql`
- **Health Checks**: Configured health check using `pg_isready`
- **Port**: Exposed on `5432` for local development

## Authentication & Authorization

The application implements **Auth0** for secure authentication:

### Backend
- JWT token validation on protected endpoints
- Automatic user provisioning on first login
- User identity tracked via Auth0 `sub` (subject) claim
- Dependency injection pattern for auth validation

### Frontend
- Auth0 Angular SDK integration
- HTTP interceptor for automatic token injection
- Redirect handling after authentication
- Audience-based token requests for API access

### Required Environment Variables
- `AUTH0_DOMAIN`: Your Auth0 tenant domain
- `AUTH0_AUDIENCE`: API identifier in Auth0 dashboard
- `AUTH0_CLIENT_ID`: Frontend application client ID (frontend only)

## Getting Started

### Prerequisites

- **Docker & Docker Compose**: For containerized deployment
- **Python 3.11+**: For local backend development
- **Node.js 20+ & npm**: For local frontend development
- **Auth0 Account**: For authentication setup
- **Google Gemini API Key**: For LLM access

### Environment Setup

#### Backend Environment (`.env` in `apps/backend/`)
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_GENAI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=text-embedding-004
DB_URL=postgresql://user:password@db:5432/dbname
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=your-api-identifier
```

#### Frontend Environment (`.env` in `apps/frontend/src/environments/`)
```typescript
export const environment = {
  production: false,
  API_URL: 'http://localhost:8000',
  AUTH0_DOMAIN: 'your-tenant.auth0.com',
  AUTH0_CLIENT_ID: 'your_client_id',
  AUTH0_AUDIENCE: 'your-api-identifier'
};
```

#### Database Environment (`db.env` in root)
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
```

### Running with Docker (Recommended)

The easiest way to run the entire stack is using Docker Compose:

```bash
# Build and start all services (PostgreSQL, Backend, Frontend)
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Access Points:**
- Frontend: `http://localhost:4200`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

### Local Development

#### Backend Development

```bash
cd apps/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
./runme.sh
# Or manually with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### Frontend Development

```bash
cd apps/frontend

# Install dependencies
npm install

# Start development server
npm start
# Or: ng serve

# Build for production
npm run build

# Run SSR server
npm run serve:ssr:frontend
```

The frontend will be available at `http://localhost:4200`

### Database Management

#### Initialize Database Tables

Tables are automatically created on backend startup via SQLAlchemy. To manually seed data:

```bash
# Run the seed script
psql -h localhost -U your_user -d your_database -f scripts/db/seed.sql

# Or use Python script
python scripts/db/create_tables.py
```

### Container Management Scripts

Utility scripts are provided in the `scripts/` directory:

```bash
# Backend container management
./scripts/backend/start-container.sh
./scripts/backend/prune-container.sh

# Frontend container management
./scripts/frontend/start-container.sh
./scripts/frontend/prune-container.sh
```

### Deployment

```bash
# Build and push containers (custom script)
./pushme.sh "commit message"
```

## Project Dependencies

### Backend (Python)
- `fastapi[standard]` - Web framework with auto-generated OpenAPI docs
- `sqlalchemy` - ORM for database operations
- `psycopg2-binary` - PostgreSQL adapter
- `google-genai` - Google Gemini LLM client
- `faiss-cpu` - Vector similarity search
- `auth0-fastapi-api` - Auth0 JWT validation
- `pydantic-settings` - Environment variable management

### Frontend (Node.js)
- `@angular/core` v21 - Core framework
- `@angular/ssr` - Server-side rendering
- `@auth0/auth0-angular` - Authentication SDK
- `ngx-markdown` - Markdown rendering
- `tailwindcss` v4 - Styling framework
- `lucide-angular` - Icon library
- `marked` - Markdown parser

## API Documentation

Once the backend is running, you can access the auto-generated API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Check database credentials in environment files match
- Verify `DB_URL` format: `postgresql://user:password@host:port/database`

#### Authentication Errors
- Verify Auth0 domain and audience are correctly configured
- Ensure API is registered in Auth0 dashboard with correct identifier
- Check that frontend client ID matches Auth0 application
- Verify JWT tokens are being sent with requests (check browser dev tools)

#### FAISS Index Missing
- Ensure `apps/backend/app/embedding/tfsa.faiss` exists
- Run the ingestion script to create embeddings: `python -m app.rag.ingest`
- Check that `cra_tfsa_guide.txt` exists in `apps/backend/app/knowledge/`

#### Docker Build Failures
- Clear Docker cache: `docker-compose down -v && docker system prune -af`
- Ensure sufficient disk space
- Check Dockerfile syntax in `apps/backend/` and `apps/frontend/`

## License

This project is provided as-is for educational and development purposes.

## Contributing

When contributing to this project:

1. Follow the existing code structure and patterns
2. Ensure all endpoints require authentication where appropriate
3. Update this README when adding new features or endpoints
4. Test both Docker and local development setups
5. Maintain type safety in both Python (type hints) and TypeScript
