# 🧠 SurrealDB Agentic Compose - Enhanced with LangChain Multi-Model RAG

A sophisticated multi-agent AI system built with Google's ADK (Agno) and enhanced with LangChain's multi-model RAG capabilities using SurrealDB. This system demonstrates how agents can build persistent, graph-based memory across sessions using vector search, knowledge graphs, and hybrid retrieval strategies.

## 🌟 What's New

This enhanced version adds **LangChain Multi-Model RAG** capabilities inspired by the [SurrealDB blog post](https://surrealdb.com/blog/multi-model-rag-with-langchain):

- **🔍 Vector Search**: Semantic similarity search for agent outputs and research findings
- **🕸️ Knowledge Graph**: Graph-based relationships between documents and extracted keywords
- **🔄 Hybrid Retrieval**: Combines vector search + graph traversal for superior context retrieval
- **🏷️ Automatic Keyword Extraction**: LLM-powered keyword inference from agent outputs
- **📊 Multi-Model Storage**: Leverages SurrealDB's document, graph, and vector capabilities

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

## 📁 Project Structure

```
surrealdb-agentic-compose-enhanced/
├── compose.yaml              # Main Docker Compose config
├── compose.openai.yaml       # OpenAI model override
├── Dockerfile                # Agent application container
├── requirements.txt          # Python dependencies (with LangChain)
├── init.surql               # Enhanced SurrealDB schema
├── README.md                # This file
├── .mcp.env                 # MCP Gateway configuration
├── src/
│   ├── app.py               # Flask web app with RAG integration
│   ├── agents.py            # Enhanced ADK agents with RAG
│   └── langchain_rag/       # LangChain RAG module
│       ├── __init__.py
│       ├── stores.py        # Vector & Graph store setup
│       ├── keywords.py      # Keyword extraction with LLM
│       ├── ingestion.py     # Document ingestion pipeline
│       ├── retrieval.py     # Hybrid retrieval logic
│       └── prompts.py       # LLM prompts for RAG operations
└── data/                    # Data directory (mounted)
```

## 🕸️ SurrealDB Schema

The enhanced schema includes:

**Document Storage**:
- `documents` table with vector embeddings
- Full-text and vector indexes

**Keyword Storage**:
- `keywords` table with embeddings
- Frequency tracking and deduplication

**Knowledge Graph**:
- `graph_document` nodes (agent outputs, research)
- `graph_keyword` nodes (extracted topics)
- `DESCRIBED_BY` edges (document→keyword relationships)

**Agent Tracking**:
- `agent` nodes
- `agent_activity` for logging
- `COLLABORATED_WITH` edges for agent interactions

### Querying the Graph

```sql
-- View the document-keyword graph
SELECT id, <-DESCRIBED_BY<-graph_keyword.name as keywords
FROM graph_document;

-- Find related documents by keyword
SELECT id, <-DESCRIBED_BY<-graph_document.content as docs
FROM graph_keyword 
WHERE name = "docker";

-- Agent collaboration history
SELECT ->COLLABORATED_WITH->agent.name as collaborators
FROM agent:researcher;
```

## 🎯 Key Features

### 1. Persistent Memory
Agents remember past research and conversations across sessions, building knowledge over time.

### 2. Semantic Search
Vector embeddings enable finding related content even without keyword matches.

### 3. Graph Relationships
Knowledge graph tracks which topics relate to which documents, enabling discovery of indirect connections.

### 4. Hybrid Retrieval
Combines best of both worlds:
- Vector search for semantic similarity
- Graph traversal for relationship discovery
- Documents found in both get prioritized

### 5. Automatic Keyword Extraction
LLM analyzes content and extracts relevant keywords automatically, no manual tagging needed.

### 6. Time-Series Analysis
All activities are timestamped, enabling temporal analysis of how knowledge evolves.

## 🧪 Testing RAG Quality

```bash
# Test vector search threshold
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"task": "test query", "retrieval_method": "vector"}'

# Test graph traversal
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"task": "test query", "retrieval_method": "graph"}'

# Test hybrid (recommended)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"task": "test query", "retrieval_method": "hybrid", "use_memory": true}'
```

## 🔬 Advanced Usage

### Custom Keyword Extraction

The keyword inference can be tuned by modifying prompts in `src/langchain_rag/prompts.py`.

### Custom Graph Schema

Extend the graph schema in `init.surql` to add:
- Time-based nodes (dates, events)
- Location nodes
- User/persona nodes
- Custom relationship types

### Evaluation Metrics

Implement retrieval quality metrics:
- Precision: % of retrieved docs that are relevant
- Recall: % of relevant docs that were retrieved
- F1 Score: Harmonic mean of precision and recall

## 🤝 Comparison with Original

| Feature | Original | Enhanced |
|---------|----------|----------|
| Memory Storage | Simple key-value | Multi-model (vector + graph + doc) |
| Retrieval | Basic lookup | Hybrid (vector + graph traversal) |
| Keyword Extraction | Manual | Automatic (LLM-powered) |
| Context Discovery | Direct queries | Semantic + relationship-based |
| Temporal Analysis | Limited | Full time-series support |
| Agent Collaboration Tracking | No | Yes (graph-based) |

## 🐛 Troubleshooting

**Issue**: Agent responses don't include past context

**Solution**: Check that ingestion is working:
```bash
docker compose logs agent-app | grep "ingestion"
```

**Issue**: Vector search returns no results

**Solution**: Lower the `VECTOR_THRESHOLD` value in environment variables.

**Issue**: GPU out of memory

**Solution**: Use OpenAI models or Docker Offload:
```bash
docker compose -f compose.yaml -f compose.openai.yaml up
```

## 📚 Learn More

- [SurrealDB Multi-Model RAG Blog Post](https://surrealdb.com/blog/multi-model-rag-with-langchain)
- [LangChain SurrealDB Integration](https://python.langchain.com/docs/integrations/vectorstores/surrealdb/)
- [Docker Compose for Agents](https://github.com/docker/compose-for-agents)
- [Google ADK (Agno)](https://github.com/agno/agno)

## 📄 License

Apache-2.0 OR MIT

## 🙏 Acknowledgments

- Inspired by [SurrealDB's Multi-Model RAG tutorial](https://surrealdb.com/blog/multi-model-rag-with-langchain)
- Built on [Docker Compose for Agents](https://github.com/docker/compose-for-agents)
- Uses [LangChain](https://langchain.com) for RAG orchestration
- Powered by [SurrealDB](https://surrealdb.com) multi-model database

---

**Ready to build?** 🚀

```bash
docker compose up --build
```

Then open http://localhost:8080 and start chatting!
