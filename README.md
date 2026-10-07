# Data_Analysis_AI_Platform

An enterprise-oriented, full-stack AI analytics platform that enables non-technical users to query connected databases using natural language. The platform dynamically retrieves schema context, generates SQL, validates queries through a strict safety policy engine, executes them using restricted read-only credentials, and presents formatted results, interactive charts, and grounded explanations.   
## Key Features
* Natural-Language-to-SQL Interface: Ask plain-English questions about your operational or analytical databases.
* SQL Safety Engine & Guardrails: Automatically parses and validates generated SQL to prevent unsafe operations (e.g., rejecting DROP, UPDATE, INSERT, DELETE) and query chaining.
* Schema-Aware Context: Introspects database metadata, columns, descriptions, and foreign key relationships to ground query generation.
* Human Approval Workflows: Routes high-impact, confidential, or multi-table queries to approvers before execution.
* Read-Only Database Identities: Executes queries under restricted database users with enforced execution timeouts and row limits.
* Automatic Visualizations & Grounded Summaries: Recommends chart types and generates plain-language explanations strictly derived from query results.
* Governance & Enterprise Auditing: Comprehensive role-based access control (Admin, Analyst, Viewer, Approver), sensitive data labeling (Public, Internal, Confidential, Restricted), and immutable activity audit logs.
## Architecture Overview
The system architecture decouples the natural-language interface and LLM generation from database execution via a server-side control and policy layer:
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
  │                 │       │                 │       │                 │
  │  React / Web    ├──────►│  FastAPI Core   ├──────►│  LLM Adapter    │
  │  Client         │       │  Backend        │       │  (OpenAI/etc.)  │
  │                 │       │                 │       │                 │
  └─────────────────┘       └────────┬────────┘       └─────────────────┘
                                     │
                        ┌────────────┴────────────┐
                        │                         │
                        ▼                         ▼
             ┌────────────────────┐    ┌────────────────────┐
             │ SQL Policy Engine  │    │  Read-Only Target  │
             │ & Security Parser  │    │     Database       │
             └────────────────────┘    └────────────────────┘

## Project Structure
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app initialization & routing
│   │   ├── config.py            # Environment & app configurations
│   │   ├── database.py          # SQLAlchemy async session setup
│   │   ├── models.py            # DB Schema (Users, Queries, Schema, Audit)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── security.py          # Password hashing, JWT, & auth middleware
│   │   ├── agent.py             # LLM orchestration & generation adapter
│   │   ├── sql_policy.py        # SQL parser, validation, & safety rules
│   │   └── api/                 # API endpoint controllers
│   │       ├── datasources.py   # Connection management & schema refresh
│   │       ├── analyst.py       # Conversational NL-to-SQL interface
│   │       ├── queries.py       # Query validation, approval, & execution
│   │       ├── saved_queries.py # Saved query creation & retrieval
│   │       ├── dashboards.py    # Dashboard creation & widget linking
│   │       └── audit.py         # Audit logging endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── index.html                   # Interactive web client interface
└── README.md

## Tech StackFrontend: 
* Vanilla JavaScript / HTML5 / CSS3 (Embeddable client)
* Backend Framework: Python 3.11+, FastAPI   Database ORM: SQLAlchemy 2.0 (Async), AsyncPGPrimary Database: PostgreSQL   SQL Parser & Security: sqlglot
* Authentication: OAuth2 with JWT tokens, Passlib (bcrypt)LLM Engine: Provider-agnostic agent adapter

## Local Development Setup
Prerequisites
* Python 3.11 or higher
* PostgreSQL database instance
* Docker (optional)
## Backend Installation
1. Clone the repository:
  git clone https://github.com/your-username/ai-data-analyst.git
  cd ai-data-analyst/backend
2. Set up a virtual environment:
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Environment Configuration:
  Create a .env file in the backend/ directory:
  PROJECT_NAME="AI Data Analyst Platform"
  SECRET_KEY="your-super-secret-jwt-key"
  DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/aidataanalyst"
  LLM_PROVIDER="openai"
  LLM_API_KEY="your-llm-api-key"
  DEFAULT_ROW_LIMIT=1000
  DEFAULT_QUERY_TIMEOUT=30
