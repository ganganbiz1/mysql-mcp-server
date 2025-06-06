# MySQL MCP Server

A MySQL Model Context Protocol (MCP) server implemented with FastMCP 2.0 and Python.

## Features

- Execute SQL queries via MCP functions
- Get database schema information
- Fully containerized with Docker and docker-compose
- Packaged with Poetry for dependency management

## MCP Tools

The server provides the following MCP tools:

- `execute_query`: Execute a SQL query and return results
- `execute_update`: Execute an update/insert SQL query
- `get_tables`: Get a list of tables in the database
- `get_table_schema`: Get schema information for a specific table
- `describe_database`: Get comprehensive database structure information

## Setup

### Prerequisites

- Docker and docker-compose
- Poetry (for local development)
- Python 3.13+

## Cursor Integration

To integrate with Cursor, add the following to your `~/.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "mysqlMcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "MYSQL_HOST",
        "-e",
        "MYSQL_PORT",
        "-e",
        "MYSQL_USER",
        "-e",
        "MYSQL_PASSWORD",
        "-e",
        "MYSQL_DATABASE",
        "mysql-mcp-server"
      ],
      "env": {
        "MYSQL_HOST": "host.docker.internal",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "mcpdb"
      }
    }
  }
}
```

## Docker Build

To build the Docker image separately:

```bash
docker build -t mysql-mcp-server .
```
