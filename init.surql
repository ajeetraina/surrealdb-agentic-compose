-- ADK Multi-Agent Memory System - SurrealDB Schema
-- This file initializes the database schema for agent memory

-- Use namespace and database
USE NS agents;
USE DB memory;

-- Research findings table with vector embeddings
DEFINE TABLE research SCHEMALESS;
DEFINE FIELD agent_id ON research TYPE string;
DEFINE FIELD query ON research TYPE string;
DEFINE FIELD findings ON research TYPE string;
DEFINE FIELD embedding ON research TYPE array;
DEFINE FIELD source ON research TYPE string DEFAULT "web_search";
DEFINE FIELD confidence ON research TYPE float DEFAULT 0.8;
DEFINE FIELD timestamp ON research TYPE datetime DEFAULT time::now();

-- Vector index for semantic search (384 dimensions for MiniLM)
DEFINE INDEX research_vector ON research FIELDS embedding MTREE DIMENSION 384;

-- Agent activities table
DEFINE TABLE agent_activity SCHEMALESS;
DEFINE FIELD agent_id ON agent_activity TYPE string;
DEFINE FIELD action ON agent_activity TYPE string;
DEFINE FIELD details ON agent_activity TYPE object;
DEFINE FIELD timestamp ON agent_activity TYPE datetime DEFAULT time::now();

-- Agent collaboration relationships
DEFINE TABLE collaborated SCHEMALESS;

-- Agent memory (conclusions and analyses)
DEFINE TABLE agent_memory SCHEMALESS;
DEFINE FIELD agent_id ON agent_memory TYPE string;
DEFINE FIELD topic ON agent_memory TYPE string;
DEFINE FIELD content ON agent_memory TYPE string;
DEFINE FIELD confidence ON agent_memory TYPE float;
DEFINE FIELD related_research ON agent_memory TYPE array;
DEFINE FIELD timestamp ON agent_memory TYPE datetime DEFAULT time::now();

-- Conversation history
DEFINE TABLE conversation SCHEMALESS;
DEFINE FIELD session_id ON conversation TYPE string;
DEFINE FIELD role ON conversation TYPE string;
DEFINE FIELD content ON conversation TYPE string;
DEFINE FIELD timestamp ON conversation TYPE datetime DEFAULT time::now();

-- Agent definitions
DEFINE TABLE agent SCHEMALESS;
DEFINE FIELD name ON agent TYPE string;
DEFINE FIELD role ON agent TYPE string;
DEFINE FIELD description ON agent TYPE string;
DEFINE FIELD capabilities ON agent TYPE array;
DEFINE FIELD created_at ON agent TYPE datetime DEFAULT time::now();

-- Insert default agents
INSERT INTO agent (name, role, description, capabilities) VALUES
    ('auditor', 'Coordinator', 'Coordinates multi-agent workflows and delegates tasks', ['coordination', 'task_delegation']),
    ('researcher', 'Information Gatherer', 'Searches the web and stores findings with embeddings', ['web_search', 'data_storage', 'embedding_generation']),
    ('analyst', 'Analyzer', 'Retrieves past research and makes informed conclusions', ['semantic_search', 'analysis', 'synthesis']);
