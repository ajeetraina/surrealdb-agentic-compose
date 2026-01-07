# ADK Multi-Agent System with SurrealDB Memory

A collaborative multi-agent system built with Google's Agent Development Kit (ADK) that demonstrates persistent, graph-based memory using SurrealDB. The system features three agents that work together to research, analyze, and remember facts across sessions.

## Architecture

This system showcases how agents can build long-term memory and context:

- **Auditor Agent**: Coordinates the workflow and delegates tasks
- **Researcher Agent**: Gathers information via web search and stores findings in SurrealDB with embeddings
- **Analyst Agent**: Retrieves relevant past research from SurrealDB using semantic search and makes informed conclusions

All agent interactions, research findings, and decisions are persisted in SurrealDB's multi-model database, enabling:
- Graph relationships between agents and their work
- Vector search for semantic memory retrieval
- Document storage for research findings
- Time-series tracking of agent activities

## Prerequisites

- **Docker Desktop 4.43.0+ or Docker Engine** installed
- **A laptop or workstation with a GPU** (e.g., a MacBook) for running open models locally
  - If you don't have a GPU, you can use **Docker Offload**
- **Docker Compose 2.38.1+** (if using Docker Engine on Linux)

## Quick Start

1. **Navigate to this directory**
   ```bash
   cd adk-surrealdb-memory
   ```

2. **Create MCP environment file**
   ```bash
   cp mcp.env.example .mcp.env
   # Edit .mcp.env and add your API keys if needed
   ```

3. **Start the system**
   ```bash
   docker compose up --build
   ```

4. **Access the web interface**
   Open http://localhost:8080 in your browser to interact with the agents

5. **View SurrealDB data**
   - Access Surrealist: http://localhost:8081
   - Or use CLI:
     ```bash
     docker compose exec surrealdb surreal sql --ns agents --db memory --user root --pass root
     ```

## Using OpenAI Models

To use OpenAI instead of local models:

1. **Create OpenAI API key file**
   ```bash
   echo "sk-your-api-key-here" > secret.openai-api-key
   ```

2. **Start with OpenAI configuration**
   ```bash
   docker compose -f compose.yaml -f compose.openai.yaml up --build
   ```

## Example Interactions

Try these queries to see the memory system in action:

1. **First query**: "What are the latest trends in containerization?"
   - Researcher will search and store findings in SurrealDB
   
2. **Related query**: "How does Docker Compose help with microservices?"
   - Analyst will find related past research via semantic search
   - Response will reference previous containerization research

3. **Follow-up**: "What did we learn about containers earlier?"
   - System retrieves conversation history from SurrealDB

## Project Structure

```
surrealdb-agentic-compose/
├── compose.yaml              # Main Docker Compose configuration
├── compose.openai.yaml       # OpenAI model override
├── compose.offload.yaml      # Docker Offload configuration
├── mcp.env.example           # MCP environment template
├── Dockerfile                # Agent application container
├── requirements.txt          # Python dependencies
├── init.surql               # SurrealDB schema initialization
├── README.md                 # This file
└── src/
    ├── app.py               # Main application with web UI
    ├── agents.py            # ADK agent definitions
    ├── surrealdb_client.py  # SurrealDB connection and operations
    └── embeddings.py        # Embedding generation utilities
```

## Key Features

### 1. Persistent Agent Memory
Agents remember past research across sessions, building knowledge over time.

### 2. Semantic Search
Uses vector embeddings to find related past research, even if keywords don't match.

### 3. Graph Relationships
Tracks which agents collaborated on which topics, enabling insight into agent teamwork.

### 4. Time-Series Analysis
All activities are timestamped, allowing analysis of how agent knowledge evolves.





## License

This example follows the dual-license of the compose-for-agents repository:
Apache-2.0 OR MIT
