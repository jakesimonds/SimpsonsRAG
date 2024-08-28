import csv
import psycopg2
from psycopg2 import sql


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


def create_table_from_csv(csv_file, table_name, db_params):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Hardcoded schema based on the provided information
        schema = [
            ('id', 'INTEGER'),
            ('episode_id', 'INTEGER'),
            ('number', 'INTEGER'),
            ('raw_text', 'TEXT'),
            ('timestamp_in_ms', 'INTEGER'),
            ('speaking_line', 'BOOLEAN'),
            ('character_id', 'INTEGER'),
            ('location_id', 'INTEGER'),
            ('raw_character_text', 'TEXT'),
            ('raw_location_text', 'TEXT'),
            ('spoken_words', 'TEXT'),
            ('normalized_text', 'TEXT'),
            ('word_count', 'INTEGER')
        ]

        # Create table
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(type_)) for name, type_ in schema)
        )
        cursor.execute(create_table_query)

        # Import data
        with open(csv_file, 'r') as file:
            # Skip the header row
            next(file)
            cursor.copy_expert(
                sql.SQL("COPY {} FROM STDIN WITH CSV").format(sql.Identifier(table_name)),
                file
            )

        conn.commit()
        print(f"Table '{table_name}' created and data imported successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":

    csv_file = 'script_lines_tiny.csv'  # Replace with your CSV file path
    table_name = 'script_lines_tiny'  # Replace with your desired table name

    create_table_from_csv(csv_file, table_name, db_params)
