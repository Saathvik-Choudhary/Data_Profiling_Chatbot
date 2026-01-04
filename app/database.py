"""Database connection and query execution."""
import logging
import sqlite3
import os
import sys
import platform
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from app.config import settings

logger = logging.getLogger(__name__)

# Detect platform
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# Lazy import of pyodbc to allow server to start without ODBC driver
try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError as e:
    PYODBC_AVAILABLE = False
    logger.warning(f"pyodbc not available: {e}. Will use SQLite for local development.")


class DatabaseConnection:
    """Manages database connections and query execution."""
    
    def __init__(self):
        # Check if using SQLite (local development) or SQL Server
        self.use_sqlite = self._should_use_sqlite()
        
        if self.use_sqlite:
            # Store database in project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(project_root, "profiling_sample.db")
            if not os.path.exists(self.db_path):
                python_cmd = "python" if IS_WINDOWS else "python3"
                logger.warning(f"SQLite database not found: {self.db_path}")
                logger.warning(f"Run: {python_cmd} scripts/init_sample_database.py to create it")
        else:
            if not PYODBC_AVAILABLE:
                error_msg = "pyodbc is not available.\n"
                if IS_WINDOWS:
                    error_msg += (
                        "On Windows:\n"
                        "  1. Install pyodbc: pip install pyodbc\n"
                        "  2. ODBC drivers are usually pre-installed with Windows\n"
                        "  3. If needed, download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
                    )
                elif IS_MACOS:
                    error_msg += (
                        "On macOS:\n"
                        "  1. Install unixODBC: brew install unixodbc\n"
                        "  2. Install Microsoft ODBC Driver: brew install msodbcsql17\n"
                        "  3. Install pyodbc: pip install pyodbc"
                    )
                else:
                    error_msg += (
                        "On Linux:\n"
                        "  1. Install unixODBC and Microsoft ODBC Driver\n"
                        "  2. See: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-linux\n"
                        "  3. Install pyodbc: pip install pyodbc"
                    )
                raise ImportError(error_msg)
            self.connection_string = self._build_connection_string()
    
    def _should_use_sqlite(self) -> bool:
        """Determine if we should use SQLite based on database name."""
        # Use SQLite ONLY if database name explicitly ends with .db
        # Otherwise, use SQL Server
        return settings.db_database.endswith('.db')
    
    def _build_connection_string(self) -> str:
        """Build SQL Server connection string."""
        return (
            f"DRIVER={{{settings.db_driver}}};"
            f"SERVER={settings.db_server};"
            f"DATABASE={settings.db_database};"
            f"UID={settings.db_username};"
            f"PWD={settings.db_password};"
            f"TrustServerCertificate=yes;"
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        if self.use_sqlite:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            try:
                logger.info(f"SQLite connection established: {self.db_path}")
                yield conn
            except sqlite3.Error as e:
                logger.error(f"SQLite connection error: {e}")
                raise
            finally:
                conn.close()
                logger.info("SQLite connection closed")
        else:
            if not PYODBC_AVAILABLE:
                raise ImportError("pyodbc is not available")
            conn = None
            try:
                conn = pyodbc.connect(self.connection_string)
                logger.info("SQL Server connection established")
                yield conn
            except pyodbc.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
            finally:
                if conn:
                    conn.close()
                    logger.info("Database connection closed")
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as a list of dictionaries.
        
        Args:
            query: SQL SELECT query string
            
        Returns:
            List of dictionaries representing rows
            
        Raises:
            Database error if query execution fails
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                
                # Get column names
                if self.use_sqlite:
                    columns = [description[0] for description in cursor.description]
                    rows = cursor.fetchall()
                    # Convert Row objects to dictionaries
                    results = [dict(row) for row in rows]
                else:
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]
                
                logger.info(f"Query executed successfully. Returned {len(results)} rows")
                return results
                
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                raise
            finally:
                cursor.close()


# Global database instance (lazy initialization)
db = None

def get_db():
    """Get or create database connection instance."""
    global db
    if db is None:
        db = DatabaseConnection()
    return db

