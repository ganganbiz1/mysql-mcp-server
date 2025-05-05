#!/usr/bin/env python
import logging
import os
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from dotenv import load_dotenv
from fastmcp import FastMCP

from server.db.mysql_client import MySQLClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize MySQL client
mysql_client = MySQLClient(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DATABASE", "mcpsw"),
)

# Define lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[None]:
    """Handle startup and shutdown events"""
    # Startup
    logger.info("MySQL MCP Server starting up...")
    mysql_client.connect()
    logger.info("Connected to MySQL database")
    
    yield  # App is running
    
    # Shutdown
    logger.info("MySQL MCP Server shutting down...")
    mysql_client.close()
    logger.info("MySQL connection closed")

# Initialize FastMCP app with lifespan
mcp = FastMCP("MySQL MCP Server")


@mcp.tool()
def execute_query(query: str, params: Optional[List] = None) -> Dict[str, Any]:
    """Execute a SQL query and return results"""
    logger.info(f"Executing query: {query}")
    
    try:
        results = mysql_client.execute_query(query, tuple(params) if params else None)
        return {"results": results, "affected_rows": len(results)}
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def execute_update(query: str, params: Optional[List] = None) -> Dict[str, Any]:
    """Execute an update/insert SQL query and return affected rows"""
    logger.info(f"Executing update: {query}")
    
    try:
        affected_rows = mysql_client.execute_update(query, tuple(params) if params else None)
        return {"affected_rows": affected_rows}
    except Exception as e:
        logger.error(f"Error executing update: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_tables() -> Dict[str, Any]:
    """Get a list of tables in the database"""
    try:
        tables = mysql_client.get_tables()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Error getting tables: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_table_schema(table_name: str) -> Dict[str, Any]:
    """Get schema information for a specific table"""
    if not table_name:
        return {"error": "Table name is required"}
    
    try:
        schema = mysql_client.get_table_schema(table_name)
        return {"schema": schema}
    except Exception as e:
        logger.error(f"Error getting schema for table {table_name}: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def describe_database() -> Dict[str, Any]:
    """Get comprehensive information about the database structure"""
    try:
        tables = mysql_client.get_tables()
        database_info = {
            "database": mysql_client.database,
            "tables": {}
        }
        
        for table in tables:
            schema = mysql_client.get_table_schema(table)
            # Get sample data (first 5 rows)
            sample_data = mysql_client.execute_query(f"SELECT * FROM {table} LIMIT 5")
            
            database_info["tables"][table] = {
                "schema": schema,
                "sample_data": sample_data
            }
        
        return database_info
    except Exception as e:
        logger.error(f"Error describing database: {str(e)}")
        return {"error": str(e)}


def main():
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting MySQL MCP Server on {host}:{port}")
    mcp.run()


if __name__ == "__main__":
    main() 