import ollama
import psycopg2
from psycopg2 import sql
import sys

import os
import psycopg2
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

TABLE = 'script_lines'
COL_TO_VEC = 'raw_text'

def generate_embedding_local(string, model):
    try:
        response = ollama.embeddings(model=model, prompt=string)
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def update_vectors(db_params=db_params):
    counter = 0
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Set search path
        cursor.execute("SET search_path TO simpsons, public")

        # Fetch all script lines without vectors
        cursor.execute(f"SELECT id, {COL_TO_VEC} FROM {TABLE} WHERE line_vector IS NULL")
        rows = cursor.fetchall()

        for row in rows:
            id, line_text = row
            if line_text:
                vector = generate_embedding_local(line_text, 'nomic-embed-text')
                if vector:
                    try:
                        # Update the database with the new vector
                        cursor.execute(sql.SQL(f"""
                            UPDATE {TABLE}
                            SET line_vector = %s::vector
                            WHERE id = %s
                        """), (vector, id))
                        conn.commit()
                        if counter % 100 == 0:
                            print(f"Successfully updated vector for id {id}. Counter: {counter}")
                    except Exception as e:
                        print(f"Error updating vector for id {id}: {e}")
                        conn.rollback()
            counter += 1

        print(f"Attempted to update vectors for {len(rows)} rows")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or updating vectors:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    update_vectors()