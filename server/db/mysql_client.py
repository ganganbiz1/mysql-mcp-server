import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)


class MySQLClient:
    """MySQL Client for executing queries and managing connections"""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                logger.info(f"Connected to MySQL Server: {self.host}:{self.port}")
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            raise

    def close(self) -> None:
        """Close MySQL connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            logger.info("MySQL connection closed")

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries"""
        try:
            if not self.connection or not self.connection.is_connected():
                logger.warning("Connection lost. Reconnecting...")
                self.connect()
            
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchall()
            return result
        except Error as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """Execute an update/insert query and return affected rows"""
        try:
            if not self.connection or not self.connection.is_connected():
                logger.warning("Connection lost. Reconnecting...")
                self.connect()
            
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            logger.error(f"Error executing update: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            if self.connection:
                self.connection.rollback()
            raise

    def get_tables(self) -> List[str]:
        """Get list of tables in the database"""
        return [
            table["TABLE_NAME"]
            for table in self.execute_query(
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                f"WHERE TABLE_SCHEMA = '{self.database}'"
            )
        ]

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a table"""
        return self.execute_query(
            "SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, "
            "IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            f"WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = %s "
            "ORDER BY ORDINAL_POSITION",
            (table_name,),
        ) 