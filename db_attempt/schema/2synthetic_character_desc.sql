CREATE TABLE characters_tiny (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255)
);

CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Add vector column to script_lines table
ALTER TABLE characters_tiny ADD COLUMN line_vector vector(768);
