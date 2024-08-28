import sys
import psycopg2
from psycopg2 import sql
import ollama

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

def execute_query(query, db_params):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute(query)

        # Fetch column names
        col_names = [desc[0] for desc in cursor.description]
        # Print column names
        # Check if 'raw_text' is in the result
        if 'raw_text' not in col_names:
            print("Error: 'raw_text' column not found in the query results.", file=sys.stderr)
            return

        raw_text_index = col_names.index('raw_text')

        # Print only the 'raw_text' values
        for row in cursor.fetchall():
            print(row[raw_text_index])


        # print("\t".join(col_names))
        # print("-" * (sum(len(name) for name in col_names) + (len(col_names) - 1) * 2))

        # # Fetch and print rows
        # for row in cursor.fetchall():
        #     print("\t".join(str(value) for value in row))

        print(f"\n{cursor.rowcount} rows returned.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Input to SQL-izer: ")
        #query = ollama.chat(model='SimpsonsSQL', messages=[{'role': 'user', 'content': query}])
        query = ollama.chat(model='SimpsonsSQL', messages=[{'role': 'user', 'content': query}])
        print(query['message']['content'])
        query = query['message']['content']

    execute_query(query, db_params)
