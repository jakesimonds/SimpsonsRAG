import psycopg2
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file in the parent directory
dotenv_path = os.path.join(current_dir, '..', '.env')

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'options': f"-c search_path={os.getenv('DB_SCHEMA')}"
}
try:
    # Establish a connection to the database
    conn = psycopg2.connect(**db_params)

    # Create a cursor object
    cursor = conn.cursor()

    # Query to get table names
    cursor.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;

        -- Step 2: Add vector column to script_lines table
        ALTER TABLE script_lines ADD COLUMN line_vector vector(768);
    """)


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Close database connection
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")
