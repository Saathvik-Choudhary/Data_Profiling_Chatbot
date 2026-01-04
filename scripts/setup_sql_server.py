"""
Script to help set up SQL Server database for the profiling chatbot.
This script creates the necessary tables and views in SQL Server.
"""
import pyodbc
import sys
import os
# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings

def get_connection():
    """Get SQL Server connection."""
    connection_string = (
        f"DRIVER={{{settings.db_driver}}};"
        f"SERVER={settings.db_server};"
        f"DATABASE={settings.db_database};"
        f"UID={settings.db_username};"
        f"PWD={settings.db_password};"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)

def create_tables(conn):
    """Create base tables for profiling data."""
    cursor = conn.cursor()
    
    print("Creating profiling_tables...")
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[profiling_tables]') AND type in (N'U'))
        CREATE TABLE profiling_tables (
            table_id INT IDENTITY(1,1) PRIMARY KEY,
            table_name NVARCHAR(255) NOT NULL UNIQUE,
            row_count INT,
            column_count INT,
            last_profiled_date DATE,
            table_size_mb DECIMAL(10,2)
        );
    """)
    
    print("Creating profiling_columns...")
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[profiling_columns]') AND type in (N'U'))
        CREATE TABLE profiling_columns (
            column_id INT IDENTITY(1,1) PRIMARY KEY,
            table_id INT NOT NULL,
            column_name NVARCHAR(255) NOT NULL,
            data_type NVARCHAR(50),
            null_count INT,
            distinct_count INT,
            avg_length DECIMAL(10,2),
            min_value NVARCHAR(MAX),
            max_value NVARCHAR(MAX),
            duplicate_count INT,
            FOREIGN KEY (table_id) REFERENCES profiling_tables (table_id)
        );
    """)
    
    conn.commit()
    print("✅ Tables created successfully")

def create_views(conn):
    """Create views for profiling statistics."""
    cursor = conn.cursor()
    
    print("Creating views...")
    
    # Drop existing views if they exist
    for view_name in ['profiling_column_stats', 'profiling_table_stats', 'profiling_data_quality']:
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.views WHERE name = '{view_name}')
            DROP VIEW {view_name};
        """)
    
    # Create profiling_column_stats view
    cursor.execute("""
        CREATE VIEW profiling_column_stats AS
        SELECT 
            t.table_name,
            c.column_name,
            CAST(c.null_count * 100.0 / NULLIF(t.row_count, 0) AS DECIMAL(5,2)) AS null_percentage,
            c.distinct_count,
            c.data_type,
            t.row_count,
            c.avg_length,
            c.min_value,
            c.max_value
        FROM profiling_tables t
        INNER JOIN profiling_columns c ON t.table_id = c.table_id;
    """)
    
    # Create profiling_table_stats view
    cursor.execute("""
        CREATE VIEW profiling_table_stats AS
        SELECT 
            table_name,
            row_count,
            column_count,
            last_profiled_date AS last_updated,
            table_size_mb
        FROM profiling_tables;
    """)
    
    # Create profiling_data_quality view
    cursor.execute("""
        CREATE VIEW profiling_data_quality AS
        SELECT 
            t.table_name,
            c.column_name,
            CAST(c.null_count * 100.0 / NULLIF(t.row_count, 0) AS DECIMAL(5,2)) AS null_percentage,
            CAST(c.duplicate_count * 100.0 / NULLIF(t.row_count, 0) AS DECIMAL(5,2)) AS duplicate_percentage,
            CASE 
                WHEN c.null_count * 100.0 / NULLIF(t.row_count, 0) > 50 THEN 'Poor'
                WHEN c.null_count * 100.0 / NULLIF(t.row_count, 0) > 10 THEN 'Fair'
                ELSE 'Good'
            END AS quality_score
        FROM profiling_tables t
        INNER JOIN profiling_columns c ON t.table_id = c.table_id;
    """)
    
    conn.commit()
    print("✅ Views created successfully")

def test_connection():
    """Test database connection."""
    try:
        print(f"Testing connection to {settings.db_server}/{settings.db_database}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"✅ Connected successfully!")
        print(f"SQL Server version: {version[:50]}...")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("SQL Server Database Setup for Profiling Chatbot")
    print("=" * 60)
    print()
    
    # Test connection first
    if not test_connection():
        print("\n❌ Cannot proceed without a valid connection.")
        print("Please check your .env file settings:")
        print(f"  DB_SERVER={settings.db_server}")
        print(f"  DB_DATABASE={settings.db_database}")
        print(f"  DB_USERNAME={settings.db_username}")
        print(f"  DB_DRIVER={settings.db_driver}")
        sys.exit(1)
    
    print()
    response = input("Do you want to create tables and views? (y/n): ").strip().lower()
    if response != 'y':
        print("Setup cancelled.")
        return
    
    try:
        conn = get_connection()
        create_tables(conn)
        create_views(conn)
        conn.close()
        print()
        print("=" * 60)
        print("✅ Setup completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Populate profiling_tables and profiling_columns with your data")
        print("2. The views are ready to use:")
        print("   - profiling_column_stats")
        print("   - profiling_table_stats")
        print("   - profiling_data_quality")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

