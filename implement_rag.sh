#!/bin/bash

# Automated Implementation Script for LangChain Multi-Model RAG
# This script helps integrate RAG capabilities into surrealdb-agentic-compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "compose.yaml" ] || [ ! -d "src" ]; then
        print_error "This doesn't appear to be the surrealdb-agentic-compose directory"
        print_error "Please run this script from the root of your repository"
        exit 1
    fi
    print_success "Confirmed in surrealdb-agentic-compose directory"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check git
    if ! command -v git &> /dev/null; then
        print_error "Git not found. Please install Git first."
        exit 1
    fi
    print_success "Git found"
    
    # Check if in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    print_success "Git repository detected"
}

# Create feature branch
create_branch() {
    print_step "Creating feature branch..."
    
    # Get current branch
    current_branch=$(git branch --show-current)
    
    if [ "$current_branch" = "feature/langchain-multimodel-rag" ]; then
        print_warning "Already on feature/langchain-multimodel-rag branch"
    else
        git checkout -b feature/langchain-multimodel-rag
        print_success "Created and switched to feature/langchain-multimodel-rag"
    fi
}

# Backup original files
backup_files() {
    print_step "Backing up original files..."
    
    mkdir -p .backups
    
    files_to_backup=(
        "requirements.txt"
        "compose.yaml"
        "init.surql"
        "src/agents.py"
        "src/app.py"
    )
    
    for file in "${files_to_backup[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" ".backups/$(basename $file).original"
            print_success "Backed up $file"
        fi
    done
}

# Update requirements.txt
update_requirements() {
    print_step "Updating requirements.txt..."
    
    cat >> requirements.txt << 'EOF'

# ============================================
# LangChain Multi-Model RAG Dependencies
# Added: $(date +%Y-%m-%d)
# ============================================
# LangChain Core
langchain==0.3.16
langchain-core==0.3.28
langchain-community==0.3.16
langchain-text-splitters==0.3.4

# LangChain Integrations
langchain-ollama==0.2.2
langchain-openai==0.2.14
langchain-surrealdb==0.1.0

# Vector & Embedding Support
sentence-transformers==3.3.1
tiktoken==0.8.0

# Additional utilities
python-dotenv==1.0.1
pydantic==2.10.5
numpy==2.2.1
EOF

    print_success "requirements.txt updated"
}

# Create langchain_rag module directory
create_rag_module() {
    print_step "Creating langchain_rag module..."
    
    mkdir -p src/langchain_rag
    
    print_warning "⚠️  Module directory created"
    print_warning "📁 You need to copy the following files from the enhanced version:"
    print_warning "   - src/langchain_rag/__init__.py"
    print_warning "   - src/langchain_rag/stores.py"
    print_warning "   - src/langchain_rag/keywords.py"
    print_warning "   - src/langchain_rag/ingestion.py"
    print_warning "   - src/langchain_rag/retrieval.py"
    print_warning "   - src/langchain_rag/prompts.py"
    print_warning ""
    print_warning "These files are available in:"
    print_warning "/mnt/user-data/outputs/surrealdb-agentic-compose-enhanced/src/langchain_rag/"
    
    read -p "Have you copied these files? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Please copy the files and run this script again"
        exit 1
    fi
    
    print_success "langchain_rag module ready"
}

# Update compose.yaml
update_compose() {
    print_step "Updating compose.yaml..."
    
    # Check if embeddings service already exists
    if grep -q "embeddings:" compose.yaml; then
        print_warning "Embeddings service already exists in compose.yaml"
    else
        cat >> compose.yaml << 'EOF'

  # ============================================
  # Embedding Service for RAG
  # ============================================
  embeddings:
    image: ollama/ollama:latest
    container_name: embeddings-service
    command: serve
    environment:
      - OLLAMA_MODELS=all-minilm:22m
    ports:
      - "11435:11434"
    networks:
      - ai-network
    volumes:
      - embedding-models:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF
        print_success "Added embeddings service"
    fi
    
    # Check if embedding-models volume exists
    if grep -q "embedding-models:" compose.yaml; then
        print_warning "embedding-models volume already exists"
    else
        echo "" >> compose.yaml
        echo "  embedding-models:" >> compose.yaml
        print_success "Added embedding-models volume"
    fi
    
    print_warning "⚠️  Remember to add these environment variables to agent-app service:"
    print_warning "   - EMBEDDING_MODEL=all-minilm:22m"
    print_warning "   - EMBEDDING_URL=http://embeddings:11434"
    print_warning "   - VECTOR_THRESHOLD=0.3"
    print_warning "   - VECTOR_K=5"
    print_warning "   - GRAPH_LIMIT=5"
    print_warning "   - USE_OPENAI=false"
    print_warning "   - KEYWORD_MODEL=llama3.2"
}

# Update init.surql
update_schema() {
    print_step "Updating SurrealDB schema..."
    
    cat >> init.surql << 'EOF'

-- ============================================
-- LangChain Multi-Model RAG Schema
-- ============================================

-- Keywords table with vector embeddings
DEFINE TABLE keywords SCHEMAFULL;
DEFINE FIELD keyword ON keywords TYPE string;
DEFINE FIELD type ON keywords TYPE string DEFAULT "keyword";
DEFINE FIELD embedding ON keywords TYPE array<float>;
DEFINE FIELD frequency ON keywords TYPE int DEFAULT 1;
DEFINE FIELD last_seen ON keywords TYPE datetime;

DEFINE INDEX keywords_vector_idx ON keywords 
  FIELDS embedding 
  MTREE DIMENSION 384 
  DIST COSINE;

DEFINE INDEX keywords_text_idx ON keywords 
  FIELDS keyword 
  UNIQUE;

-- Graph document nodes
DEFINE TABLE graph_document SCHEMAFULL;
DEFINE FIELD content ON graph_document TYPE string;
DEFINE FIELD timestamp ON graph_document TYPE option<datetime>;
DEFINE FIELD agent ON graph_document TYPE option<string>;
DEFINE FIELD source ON graph_document TYPE option<string>;
DEFINE FIELD type ON graph_document TYPE option<string>;

-- Graph keyword nodes
DEFINE TABLE graph_keyword SCHEMAFULL;
DEFINE FIELD name ON graph_keyword TYPE string;
DEFINE FIELD category ON graph_keyword TYPE option<string>;

DEFINE INDEX graph_keyword_name_idx ON graph_keyword 
  FIELDS name 
  UNIQUE;

-- Document-Keyword relationships
DEFINE TABLE DESCRIBED_BY SCHEMAFULL TYPE RELATION 
  FROM graph_document TO graph_keyword;

DEFINE FIELD confidence ON DESCRIBED_BY TYPE option<float>;
DEFINE FIELD inferred_by ON DESCRIBED_BY TYPE string DEFAULT "llm";

-- Agent collaboration graph
DEFINE TABLE agent SCHEMAFULL;
DEFINE FIELD name ON agent TYPE string;
DEFINE FIELD role ON agent TYPE string;
DEFINE FIELD description ON agent TYPE option<string>;

DEFINE TABLE COLLABORATED_WITH SCHEMAFULL TYPE RELATION 
  FROM agent TO agent;

DEFINE FIELD task ON COLLABORATED_WITH TYPE string;
DEFINE FIELD timestamp ON COLLABORATED_WITH TYPE datetime;

-- Utility functions
DEFINE FUNCTION fn::recent_docs_by_agent($agent_name: string, $limit: int) {
  SELECT * FROM graph_document 
  WHERE agent = $agent_name 
  ORDER BY timestamp DESC 
  LIMIT $limit;
};

DEFINE FUNCTION fn::find_related_docs($keywords: array<string>, $limit: int) {
  SELECT id, <-DESCRIBED_BY<-graph_document.content as docs
  FROM graph_keyword 
  WHERE name IN $keywords 
  GROUP BY id 
  LIMIT $limit;
};

COMMIT;

SELECT "✅ LangChain RAG schema initialized" as status;
EOF

    print_success "init.surql updated with RAG schema"
}

# Create OpenAI compose override
create_openai_compose() {
    print_step "Creating compose.openai.yaml..."
    
    cat > compose.openai.yaml << 'EOF'
version: '3.9'

# OpenAI override configuration
# Usage: docker compose -f compose.yaml -f compose.openai.yaml up

services:
  agent-app:
    environment:
      - USE_OPENAI=true
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MODEL_NAME=gpt-4o-mini
      - EMBEDDING_MODEL=text-embedding-3-small
    secrets:
      - openai_api_key

  model-runner:
    profiles:
      - disabled

  embeddings:
    profiles:
      - disabled

secrets:
  openai_api_key:
    file: ./secret.openai-api-key
EOF

    print_success "compose.openai.yaml created"
}

# Show next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Automated Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next Manual Steps:${NC}"
    echo ""
    echo "1. Update src/agents.py:"
    echo "   - Add RAG imports and initialization"
    echo "   - See IMPLEMENTATION_STEPS.md Step 7"
    echo ""
    echo "2. Update src/app.py:"
    echo "   - Add RAG initialization"
    echo "   - See IMPLEMENTATION_STEPS.md Step 8"
    echo ""
    echo "3. Add environment variables to agent-app in compose.yaml"
    echo "   - See output above for required variables"
    echo ""
    echo "4. Test locally:"
    echo "   docker compose down -v"
    echo "   docker compose up --build"
    echo ""
    echo "5. Verify RAG functionality:"
    echo "   curl http://localhost:8080/health"
    echo ""
    echo "6. Commit and push:"
    echo "   git add ."
    echo "   git commit -m 'feat: Add LangChain Multi-Model RAG support'"
    echo "   git push origin feature/langchain-multimodel-rag"
    echo ""
    echo "7. Create PR on GitHub"
    echo ""
    echo -e "${BLUE}📚 See IMPLEMENTATION_STEPS.md for detailed instructions${NC}"
}

# Main execution
main() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  LangChain Multi-Model RAG Integration Setup   ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_directory
    check_prerequisites
    create_branch
    backup_files
    update_requirements
    create_rag_module
    update_compose
    update_schema
    create_openai_compose
    show_next_steps
}

# Run main
main
