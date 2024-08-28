-- Step 1: Install pgvector extension (run this as a superuser)
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Add vector column to script_lines table
ALTER TABLE simpsons_character_strings ADD COLUMN line_vector vector(768);

-- Step 3: Create an index on the vector column (optional, but recommended for performance)
-- CREATE INDEX ON script_lines USING ivfflat (line_vector vector_cosine_ops);
