# SurrealDB Agentic Compose with LangChain Multi-Model RAG

A sophisticated multi-agent AI system built with Google's ADK (Agno) and enhanced with LangChain's multi-model RAG capabilities using SurrealDB. This system demonstrates how agents can build persistent, graph-based memory across sessions using vector search, knowledge graphs, and hybrid retrieval strategies.

## 🌟 What's New

This version adds **LangChain Multi-Model RAG** capabilities inspired by the [SurrealDB blog post](https://surrealdb.com/blog/multi-model-rag-with-langchain):

- **🔍 Vector Search**: Semantic similarity search for agent outputs and research findings
- **🕸️ Knowledge Graph**: Graph-based relationships between documents and extracted keywords
- **🔄 Hybrid Retrieval**: Combines vector search + graph traversal for superior context retrieval
- **🏷️ Automatic Keyword Extraction**: LLM-powered keyword inference from agent outputs
- **📊 Multi-Model Storage**: Leverages SurrealDB's document, graph, and vector capabilities

## Why SurrealDB for AI Agents

- Agents need to remember conversations, context, and state
- Graph Relationships for Multi-Agent Systems
- Agents can subscribe to changes (WebSocket support)
- When one agent updates data, others are notified instantly.


## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Flask Web App - :8080)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Agent Layer (ADK)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Coordinator  │──│ Researcher   │──│  Analyst     │      │
│  │    Agent     │  │    Agent     │  │   Agent      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
┌────────────┴────────────────────────────────┴───────────────┐
│              LangChain RAG Pipeline                          │
│                                                              │
│  ┌──────────────────┐  ┌─────────────────────────────┐     │
│  │   Ingestion      │  │      Retrieval              │     │
│  │   - Documents    │  │   - Vector Search           │     │
│  │   - Keywords     │  │   - Graph Traversal         │     │
│  │   - Graph Build  │  │   - Hybrid Combination      │     │
│  └──────────────────┘  └─────────────────────────────┘     │
└─────────────┬──────────────────────────────────────────────┘
              │
┌─────────────┴──────────────────────────────────────────────┐
│                 SurrealDB (Multi-Model)                     │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Vector    │  │    Graph    │  │  Document   │        │
│  │    Store    │  │    Store    │  │    Store    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop 4.43.0+** or **Docker Engine**
- **GPU-enabled system** (for local models) OR **OpenAI API key**
- **Docker Compose 2.38.1+** (if using Docker Engine on Linux)

### 1. Clone & Setup

```bash
cd surrealdb-agentic-compose-enhanced
cp mcp.env.example .mcp.env
# Edit .mcp.env if you want to configure MCP servers
```

### 2. Choose Your Model Provider

#### Option A: Local Models (Requires GPU)

```bash
docker compose up --build
```

#### Option B: OpenAI Models

```bash
# Create API key file
echo "sk-your-api-key-here" > secret.openai-api-key

# Start with OpenAI configuration
docker compose -f compose.yaml -f compose.openai.yaml up --build
```

### 3. Access the Application

- **Web Interface**: http://localhost:8080
- **Surrealist UI**: http://localhost:8081
- **MCP Gateway**: http://localhost:8811

## 💡 How It Works

### Multi-Model RAG Flow

1. **Ingestion Pipeline**
   ```
   Agent Output/Research Finding
   ↓
   Extract Keywords (LLM)
   ↓
   Generate Embeddings
   ↓
   Store in:
   - Vector Store (conversations)
   - Vector Store (keywords)  
   - Graph Store (document→keyword relationships)
   ```

2. **Hybrid Retrieval**
   ```
   User Query
   ↓
   ┌─────────────────┬─────────────────┐
   │  Vector Search  │ Graph Traversal │
   │  (Semantic)     │ (Relationships) │
   └────────┬────────┴────────┬────────┘
            │                 │
            └────── Merge ────┘
                     ↓
            Re-rank & Combine
                     ↓
            Context for LLM
   ```

3. **Agent Coordination**
   ```
   User Request
   ↓
   Coordinator Agent
   ↓
   Check Past Context (Hybrid Retrieval)
   ↓
   ┌────────────────────┬────────────────┐
   │ Researcher Agent   │ Analyst Agent  │
   │ (Gather Info)      │ (Analyze)      │
   └────────────────────┴────────────────┘
   ↓
   Store Results (Ingestion)
   ↓
   Return to User
   ```

## 📊 Example Interactions

### First Query: Research
```
Query: "What are the latest trends in containerization?"

Process:
1. Coordinator routes to Researcher
2. Researcher searches web via MCP Gateway
3. Findings stored in SurrealDB with embeddings
4. Keywords extracted: ["containerization", "docker", "kubernetes", "trends"]
5. Graph relationships created
```

### Follow-up Query: Analysis with Context
```
Query: "How does Docker Compose help with the containerization we discussed?"

Process:
1. Hybrid retrieval finds previous containerization research
2. Vector search: matches "docker compose" and "containerization"
3. Graph traversal: finds documents linked to "containerization" keyword
4. Analyst receives enriched context from past research
5. Response references previous findings naturally
```

### Memory Query
```
Query: "What did we learn about Docker earlier?"

Process:
1. Vector search on "docker" finds semantically related docs
2. Graph traversal finds all docs connected to "docker" keyword
3. Returns timestamped findings in chronological order
```

## 🔧 Configuration

### Environment Variables

```bash
# SurrealDB
SURREAL_URL=ws://surrealdb:8000/rpc
SURREAL_NS=agents
SURREAL_DB=memory
SURREAL_USER=root
SURREAL_PASS=root

# Embedding Model
EMBEDDING_MODEL=all-minilm:22m
USE_OPENAI=false

# RAG Parameters
VECTOR_THRESHOLD=0.3  # Similarity threshold (0-1)
VECTOR_K=5           # Number of vector results
GRAPH_LIMIT=5        # Number of graph results

# Keyword Extraction
KEYWORD_MODEL=llama3.2
```

### Tuning RAG Performance

**Vector Search Threshold** (`VECTOR_THRESHOLD`):
- Lower (0.2-0.3): More results, may include less relevant docs
- Higher (0.4-0.6): Fewer results, more precise matches
- Default: 0.3 works well for most cases

**K Value** (`VECTOR_K`):
- How many top results to retrieve
- Typically 3-10 depending on context window size
- Default: 5 balances context richness and token usage

