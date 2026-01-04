"""Initialize sample database with profiling data for testing."""
import sqlite3
import os
from datetime import datetime, timedelta

# Store database in project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(project_root, "profiling_sample.db")


def create_database():
    """Create SQLite database with sample profiling data."""
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Creating database schema...")
    
    # Create base profiling tables
    cursor.execute("""
        CREATE TABLE profiling_tables (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            row_count INTEGER,
            column_count INTEGER,
            last_profiled_date TIMESTAMP,
            table_size_mb REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE profiling_columns (
            column_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            column_name TEXT NOT NULL,
            data_type TEXT,
            null_count INTEGER,
            distinct_count INTEGER,
            avg_length REAL,
            min_value TEXT,
            max_value TEXT,
            duplicate_count INTEGER,
            FOREIGN KEY (table_id) REFERENCES profiling_tables(table_id)
        )
    """)
    
    # Insert sample table data
    print("Inserting sample table data...")
    tables_data = [
        ("customers", 15000, 12, datetime.now() - timedelta(days=1), 2.5),
        ("orders", 45000, 8, datetime.now() - timedelta(days=2), 3.8),
        ("products", 2500, 15, datetime.now() - timedelta(days=1), 1.2),
        ("transactions", 125000, 10, datetime.now() - timedelta(hours=12), 8.5),
        ("employees", 500, 20, datetime.now() - timedelta(days=3), 0.8),
    ]
    
    for table_name, row_count, col_count, last_profiled, size_mb in tables_data:
        cursor.execute("""
            INSERT INTO profiling_tables (table_name, row_count, column_count, last_profiled_date, table_size_mb)
            VALUES (?, ?, ?, ?, ?)
        """, (table_name, row_count, col_count, last_profiled, size_mb))
    
    # Insert sample column data
    print("Inserting sample column profiling data...")
    
    # Customers table columns
    customers_columns = [
        (1, "customer_id", "INTEGER", 0, 15000, None, "1", "15000", 0),
        (1, "first_name", "VARCHAR", 0, 14200, 12.5, "Aaron", "Zoe", 800),
        (1, "last_name", "VARCHAR", 0, 14800, 15.2, "Anderson", "Zimmerman", 200),
        (1, "email", "VARCHAR", 1500, 13500, 24.8, "a@example.com", "z@example.com", 0),
        (1, "phone", "VARCHAR", 3200, 12000, 13.0, "100-000-0000", "999-999-9999", 3000),
        (1, "address", "VARCHAR", 800, 14500, 45.2, "100 Main St", "9999 Oak Ave", 500),
        (1, "city", "VARCHAR", 0, 850, 12.5, "Albany", "Zurich", 0),
        (1, "state", "VARCHAR", 0, 52, 2.0, "AK", "WY", 0),
        (1, "zip_code", "VARCHAR", 0, 1200, 5.0, "00001", "99999", 0),
        (1, "registration_date", "DATE", 0, 1825, None, "2019-01-01", "2024-12-31", 0),
        (1, "status", "VARCHAR", 0, 3, 6.0, "active", "inactive", 0),
        (1, "notes", "TEXT", 8500, 8500, 125.5, None, None, 0),
    ]
    
    # Orders table columns
    orders_columns = [
        (2, "order_id", "INTEGER", 0, 45000, None, "1", "45000", 0),
        (2, "customer_id", "INTEGER", 0, 12000, None, "1", "15000", 0),
        (2, "order_date", "DATE", 0, 1095, None, "2022-01-01", "2024-12-31", 0),
        (2, "total_amount", "DECIMAL", 0, 12500, None, "5.99", "9999.99", 0),
        (2, "status", "VARCHAR", 0, 5, 10.0, "pending", "shipped", 0),
        (2, "shipping_address", "VARCHAR", 500, 44000, 48.5, None, None, 1000),
        (2, "payment_method", "VARCHAR", 0, 8, 12.0, "cash", "wire_transfer", 0),
        (2, "notes", "TEXT", 35000, 10000, 85.2, None, None, 0),
    ]
    
    # Products table columns
    products_columns = [
        (3, "product_id", "INTEGER", 0, 2500, None, "1", "2500", 0),
        (3, "product_name", "VARCHAR", 0, 2500, 28.5, "Widget A", "Zebra Stripes", 0),
        (3, "category", "VARCHAR", 0, 25, 15.0, "Electronics", "Toys", 0),
        (3, "price", "DECIMAL", 0, 1250, None, "0.99", "999.99", 0),
        (3, "stock_quantity", "INTEGER", 0, 500, None, "0", "10000", 0),
        (3, "description", "TEXT", 200, 2300, 145.8, None, None, 0),
        (3, "supplier_id", "INTEGER", 500, 200, None, "1", "50", 0),
        (3, "created_date", "DATE", 0, 1825, None, "2019-01-01", "2024-12-31", 0),
        (3, "is_active", "BOOLEAN", 0, 2, None, "0", "1", 0),
        (3, "tags", "VARCHAR", 800, 1700, 25.5, None, None, 0),
        (3, "image_url", "VARCHAR", 1200, 1300, 45.2, None, None, 0),
        (3, "weight_kg", "DECIMAL", 300, 2200, None, "0.01", "50.00", 0),
        (3, "dimensions", "VARCHAR", 400, 2100, 18.5, None, None, 0),
        (3, "warranty_months", "INTEGER", 600, 25, None, "0", "60", 0),
        (3, "rating", "DECIMAL", 1500, 100, None, "1.0", "5.0", 0),
    ]
    
    # Transactions table columns
    transactions_columns = [
        (4, "transaction_id", "INTEGER", 0, 125000, None, "1", "125000", 0),
        (4, "order_id", "INTEGER", 0, 45000, None, "1", "45000", 0),
        (4, "transaction_date", "TIMESTAMP", 0, 87500, None, "2022-01-01 00:00:00", "2024-12-31 23:59:59", 0),
        (4, "amount", "DECIMAL", 0, 8750, None, "0.01", "5000.00", 0),
        (4, "currency", "VARCHAR", 0, 5, 3.0, "EUR", "USD", 0),
        (4, "payment_status", "VARCHAR", 0, 4, 10.0, "failed", "success", 0),
        (4, "processor_response", "TEXT", 25000, 100000, 125.5, None, None, 0),
        (4, "refund_amount", "DECIMAL", 110000, 1500, None, "0.00", "5000.00", 0),
        (4, "fraud_score", "DECIMAL", 50000, 75000, None, "0.0", "100.0", 0),
        (4, "metadata", "JSON", 30000, 95000, 85.2, None, None, 0),
    ]
    
    # Employees table columns
    employees_columns = [
        (5, "employee_id", "INTEGER", 0, 500, None, "1", "500", 0),
        (5, "first_name", "VARCHAR", 0, 485, 8.5, "Alice", "Zachary", 0),
        (5, "last_name", "VARCHAR", 0, 495, 10.2, "Adams", "Zimmer", 0),
        (5, "email", "VARCHAR", 0, 500, 22.5, "a.adams@company.com", "z.zimmer@company.com", 0),
        (5, "department", "VARCHAR", 0, 12, 15.0, "Engineering", "Sales", 0),
        (5, "position", "VARCHAR", 0, 45, 20.5, "Intern", "VP Engineering", 0),
        (5, "salary", "DECIMAL", 0, 450, None, "40000.00", "250000.00", 0),
        (5, "hire_date", "DATE", 0, 1825, None, "2019-01-01", "2024-12-31", 0),
        (5, "manager_id", "INTEGER", 50, 450, None, "1", "500", 0),
        (5, "phone_extension", "VARCHAR", 100, 400, 4.0, "1000", "9999", 0),
        (5, "office_location", "VARCHAR", 0, 8, 12.0, "Building A", "Remote", 0),
        (5, "emergency_contact", "VARCHAR", 200, 300, 35.5, None, None, 0),
        (5, "emergency_phone", "VARCHAR", 200, 300, 13.0, None, None, 0),
        (5, "start_date", "DATE", 0, 1825, None, "2019-01-01", "2024-12-31", 0),
        (5, "end_date", "DATE", 450, 50, None, None, None, 0),
        (5, "status", "VARCHAR", 0, 3, 8.0, "active", "terminated", 0),
        (5, "notes", "TEXT", 400, 100, 125.5, None, None, 0),
        (5, "performance_rating", "DECIMAL", 150, 350, None, "1.0", "5.0", 0),
        (5, "training_completed", "BOOLEAN", 0, 2, None, "0", "1", 0),
        (5, "certifications", "VARCHAR", 300, 200, 45.2, None, None, 0),
    ]
    
    all_columns = customers_columns + orders_columns + products_columns + transactions_columns + employees_columns
    
    cursor.executemany("""
        INSERT INTO profiling_columns 
        (table_id, column_name, data_type, null_count, distinct_count, avg_length, min_value, max_value, duplicate_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_columns)
    
    # Create views for the chatbot
    print("Creating profiling views...")
    
    cursor.execute("""
        CREATE VIEW profiling_column_stats AS
        SELECT 
            t.table_name,
            c.column_name,
            CAST(c.null_count * 100.0 / NULLIF(t.row_count, 0) AS REAL) AS null_percentage,
            c.distinct_count,
            c.data_type,
            t.row_count,
            c.avg_length,
            c.min_value,
            c.max_value
        FROM profiling_tables t
        INNER JOIN profiling_columns c ON t.table_id = c.table_id
    """)
    
    cursor.execute("""
        CREATE VIEW profiling_table_stats AS
        SELECT 
            table_name,
            row_count,
            column_count,
            last_profiled_date AS last_updated,
            table_size_mb
        FROM profiling_tables
    """)
    
    cursor.execute("""
        CREATE VIEW profiling_data_quality AS
        SELECT 
            t.table_name,
            c.column_name,
            CAST(c.null_count * 100.0 / NULLIF(t.row_count, 0) AS REAL) AS null_percentage,
            CAST(c.duplicate_count * 100.0 / NULLIF(t.row_count, 0) AS REAL) AS duplicate_percentage,
            CASE 
                WHEN c.null_count * 100.0 / NULLIF(t.row_count, 0) > 50 THEN 'Poor'
                WHEN c.null_count * 100.0 / NULLIF(t.row_count, 0) > 10 THEN 'Fair'
                ELSE 'Good'
            END AS quality_score
        FROM profiling_tables t
        INNER JOIN profiling_columns c ON t.table_id = c.table_id
    """)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database created successfully: {DB_PATH}")
    print(f"✅ Inserted {len(tables_data)} tables")
    print(f"✅ Inserted {len(all_columns)} columns")
    print(f"✅ Created 3 profiling views")
    print("\nDatabase is ready for use!")


if __name__ == "__main__":
    create_database()


