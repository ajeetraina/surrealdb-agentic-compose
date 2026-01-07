"""
ADK Multi-Agent Application with SurrealDB Memory
Main application entry point with FastAPI web interface
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents import create_agent_system
from surrealdb_client import SurrealDBClient

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="ADK SurrealDB Multi-Agent System")

# Global state
db_client: Optional[SurrealDBClient] = None
agent_system = None

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    session_id: str
    research_count: int
    memory_used: bool

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    global db_client, agent_system
    
    logger.info("🚀 Starting ADK SurrealDB Multi-Agent System...")
    
    # Initialize SurrealDB connection
    db_url = os.getenv("SURREALDB_URL", "ws://surrealdb:8000/rpc")
    db_ns = os.getenv("SURREALDB_NS", "agents")
    db_name = os.getenv("SURREALDB_DB", "memory")
    db_user = os.getenv("SURREALDB_USER", "root")
    db_pass = os.getenv("SURREALDB_PASS", "root")
    
    db_client = SurrealDBClient(
        url=db_url,
        namespace=db_ns,
        database=db_name,
        username=db_user,
        password=db_pass
    )
    
    await db_client.connect()
    logger.info("✅ Connected to SurrealDB")
    
    # Initialize agent system
    agent_system = await create_agent_system(db_client)
    logger.info("✅ Agent system initialized")
    
    logger.info("🎉 System ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global db_client
    
    if db_client:
        await db_client.close()
        logger.info("👋 Disconnected from SurrealDB")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ADK SurrealDB Multi-Agent System</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
            }
            .query-section {
                margin-bottom: 30px;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                min-height: 100px;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .response-section {
                margin-top: 30px;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 5px;
                display: none;
            }
            .response-content {
                white-space: pre-wrap;
                line-height: 1.6;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .stat-card {
                background: white;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            .stat-label {
                color: #666;
                font-size: 14px;
            }
            .stat-value {
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
                margin-top: 5px;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .example-queries {
                margin-top: 20px;
            }
            .example-query {
                background: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                cursor: pointer;
            }
            .example-query:hover {
                background: #e0e0e0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ADK Multi-Agent System with SurrealDB Memory</h1>
            <p class="subtitle">Ask questions and watch agents research, remember, and collaborate</p>
            
            <div class="query-section">
                <label for="query"><strong>Your Question:</strong></label>
                <textarea id="query" placeholder="Ask anything... The agents will search, learn, and remember!"></textarea>
                <button onclick="submitQuery()" id="submitBtn">Ask Agents</button>
            </div>
            
            <div class="example-queries">
                <strong>Try these examples:</strong>
                <div class="example-query" onclick="setQuery('What are the latest trends in containerization?')">
                    🔍 What are the latest trends in containerization?
                </div>
                <div class="example-query" onclick="setQuery('How does Docker Compose help with microservices?')">
                    🐳 How does Docker Compose help with microservices?
                </div>
                <div class="example-query" onclick="setQuery('What did we learn about containers earlier?')">
                    💭 What did we learn about containers earlier?
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Agents are working...</p>
            </div>
            
            <div class="response-section" id="responseSection">
                <h2>Response:</h2>
                <div class="response-content" id="responseContent"></div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-label">Research Items Found</div>
                        <div class="stat-value" id="researchCount">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Memory Used</div>
                        <div class="stat-value" id="memoryUsed">No</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Session ID</div>
                        <div class="stat-value" id="sessionId" style="font-size: 14px;">-</div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let currentSessionId = null;
            
            function setQuery(text) {
                document.getElementById('query').value = text;
            }
            
            async function submitQuery() {
                const query = document.getElementById('query').value.trim();
                if (!query) {
                    alert('Please enter a question');
                    return;
                }
                
                const submitBtn = document.getElementById('submitBtn');
                const loading = document.getElementById('loading');
                const responseSection = document.getElementById('responseSection');
                
                submitBtn.disabled = true;
                loading.style.display = 'block';
                responseSection.style.display = 'none';
                
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            query: query,
                            session_id: currentSessionId
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('responseContent').textContent = data.response;
                        document.getElementById('researchCount').textContent = data.research_count;
                        document.getElementById('memoryUsed').textContent = data.memory_used ? 'Yes' : 'No';
                        document.getElementById('sessionId').textContent = data.session_id.substring(0, 8) + '...';
                        currentSessionId = data.session_id;
                        responseSection.style.display = 'block';
                    } else {
                        alert('Error: ' + data.detail);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    submitBtn.disabled = false;
                    loading.style.display = 'none';
                }
            }
            
            // Allow Enter to submit (with Shift+Enter for new line)
            document.getElementById('query').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    submitQuery();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/query", response_model=QueryResponse)
async def query_agents(request: QueryRequest):
    """Process a query through the agent system"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Agent system not initialized")
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Store conversation in database
        await db_client.create("conversation", {
            "session_id": session_id,
            "role": "user",
            "content": request.query,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process query through agent system
        result = await agent_system.process_query(request.query, session_id)
        
        # Store agent response
        await db_client.create("conversation", {
            "session_id": session_id,
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            response=result["response"],
            session_id=session_id,
            research_count=result.get("research_count", 0),
            memory_used=result.get("memory_used", False)
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = await db_client.query("""
            SELECT 
                (SELECT count() FROM research GROUP ALL)[0].count AS total_research,
                (SELECT count() FROM agent_memory GROUP ALL)[0].count AS total_memories,
                (SELECT count() FROM conversation GROUP ALL)[0].count AS total_messages,
                (SELECT count() FROM agent_activity GROUP ALL)[0].count AS total_activities
        """)
        
        return JSONResponse(content=stats[0] if stats else {})
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
