"""SurrealDB Client for Agent Memory Operations"""
import logging
from typing import Any, Dict, List, Optional
from surrealdb import Surreal

logger = logging.getLogger(__name__)

class SurrealDBClient:
    def __init__(self, url: str, namespace: str, database: str, username: str, password: str):
        self.url = url
        self.namespace = namespace
        self.database = database
        self.username = username
        self.password = password
        self.client: Optional[Surreal] = None
    
    async def connect(self):
        try:
            self.client = Surreal(self.url)
            await self.client.connect()  # ← CRITICAL: Added this line!
            await self.client.signin({"username": self.username, "password": self.password})
            await self.client.use(self.namespace, self.database)
            logger.info(f"✅ Connected to SurrealDB at {self.url}")
        except Exception as e:
            logger.error(f"Failed to connect to SurrealDB: {e}")
            raise
    
    async def close(self):
        if self.client:
            await self.client.close()
    
    async def create(self, table: str, data: Dict[str, Any]):
        return await self.client.create(table, data)
    
    async def query(self, sql: str, params: Optional[Dict[str, Any]] = None):
        result = await self.client.query(sql, params) if params else await self.client.query(sql)
        return result[0] if result else []
    
    async def select(self, target: str):
        return await self.client.select(target)
    
    async def update(self, target: str, data: Dict[str, Any]):
        return await self.client.update(target, data)
    
    async def delete(self, target: str):
        return await self.client.delete(target)
