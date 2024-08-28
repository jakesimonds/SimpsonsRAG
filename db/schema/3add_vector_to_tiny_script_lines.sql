CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Add vector column to script_lines table
ALTER TABLE script_lines_tiny ADD COLUMN line_vector vector(768);
