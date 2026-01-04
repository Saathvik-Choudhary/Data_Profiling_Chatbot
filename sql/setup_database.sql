-- Example SQL script for setting up profiling database views
-- Adjust according to your actual profiling table structure

-- View: Column-level statistics
CREATE OR ALTER VIEW profiling_column_stats AS
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

-- View: Table-level statistics
CREATE OR ALTER VIEW profiling_table_stats AS
SELECT 
    table_name,
    row_count,
    column_count,
    last_profiled_date AS last_updated,
    table_size_mb
FROM profiling_tables;

-- View: Data quality metrics
CREATE OR ALTER VIEW profiling_data_quality AS
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

-- Grant read-only access to application user
-- GRANT SELECT ON profiling_column_stats TO [your_app_user];
-- GRANT SELECT ON profiling_table_stats TO [your_app_user];
-- GRANT SELECT ON profiling_data_quality TO [your_app_user];


