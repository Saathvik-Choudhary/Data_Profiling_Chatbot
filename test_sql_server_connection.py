"""
Test script to verify SQL Server connection.
"""
import sys
import platform
from config import settings

IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"

def test_connection():
    """Test SQL Server connection."""
    try:
        import pyodbc
    except ImportError:
        print("❌ pyodbc is not installed.")
        print("Install it with: pip install pyodbc")
        if IS_MACOS:
            print("On macOS, you may also need: brew install unixodbc")
        elif IS_WINDOWS:
            print("On Windows, ODBC drivers are usually pre-installed.")
            print("If needed, download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        return False
    
    print("=" * 60)
    print("Testing SQL Server Connection")
    print("=" * 60)
    print()
    print(f"Server: {settings.db_server}")
    print(f"Database: {settings.db_database}")
    print(f"Username: {settings.db_username}")
    print(f"Driver: {settings.db_driver}")
    print()
    
    try:
        connection_string = (
            f"DRIVER={{{settings.db_driver}}};"
            f"SERVER={settings.db_server};"
            f"DATABASE={settings.db_database};"
            f"UID={settings.db_username};"
            f"PWD={settings.db_password};"
            f"TrustServerCertificate=yes;"
        )
        
        print("Attempting connection...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        # Check if views exist
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_NAME IN ('profiling_column_stats', 'profiling_table_stats', 'profiling_data_quality')
        """)
        views = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        print("✅ Connection successful!")
        print()
        print(f"SQL Server Version: {version[:80]}...")
        print()
        print("Required views:")
        for view_name in ['profiling_column_stats', 'profiling_table_stats', 'profiling_data_quality']:
            status = "✅" if view_name in views else "❌"
            print(f"  {status} {view_name}")
        
        if len(views) < 3:
            print()
            python_cmd = "python" if IS_WINDOWS else "python3"
            print(f"⚠️  Some views are missing. Run: {python_cmd} setup_sql_server.py")
        
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("Common issues:")
        print("1. Check if SQL Server is running")
        print("2. Verify server name, database name, username, and password")
        print("3. Ensure the ODBC driver is installed")
        print("4. Check firewall settings")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

