# #!/usr/bin/env python3

# import csv
# import psycopg2
# from psycopg2.extras import execute_values

# # Database connection parameters
# DB_NAME = "simpsons2"
# DB_USER = "jake.simonds"  # Replace with your actual username
# DB_HOST = "localhost"

# # Connect to the database
# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password='postgres', host=DB_HOST)
# cur = conn.cursor()

# # # Import characters
# # with open('simpsons_characters.csv', 'r') as f:
# #     cur.copy_expert("COPY characters FROM STDIN CSV HEADER", f)

# # # Import episodes
# # with open('simpsons_episodes_.csv', 'r') as f:
# #     cur.copy_expert("COPY episodes FROM STDIN CSV HEADER", f)

# # # Import locations
# # with open('simpsons_locations.csv', 'r') as f:
# #     cur.copy_expert("COPY locations FROM STDIN CSV HEADER", f)

# # Import script_lines
# error_count = 0
# successful_count = 0

# with open('simpsons_script_lines.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader)  # Skip header
#     batch_size = 1000
#     batch = []
    
#     for row in reader:
#         try:
#             # Convert empty strings to None for integer fields
#             row[0] = int(row[0]) if row[0] else None  # id
#             row[1] = int(row[1]) if row[1] else None  # episode_id
#             row[2] = int(row[2]) if row[2] else None  # number
#             row[4] = int(row[4]) if row[4] else None  # timestamp_in_ms
#             row[5] = row[5].lower() == 'true'  # speaking_line
#             row[6] = int(row[6]) if row[6] else None  # character_id
#             row[7] = int(row[7]) if row[7] else None  # location_id
#             row[12] = int(row[12]) if row[12] else None  # word_count
            
#             batch.append(tuple(row))
            
#             if len(batch) >= batch_size:
#                 execute_values(cur, "INSERT INTO script_lines VALUES %s", batch)
#                 conn.commit()
#                 successful_count += len(batch)
#                 batch = []
#         except (ValueError, psycopg2.Error) as e:
#             print(f"Error processing row: {row}")
#             print(f"Error details: {str(e)}")
#             error_count += 1
#             continue

#     # Insert any remaining rows
#     if batch:
#         execute_values(cur, "INSERT INTO script_lines VALUES %s", batch)
#         conn.commit()
#         successful_count += len(batch)

# print(f"Import completed. {successful_count} lines successfully imported. {error_count} lines failed to import.")

# # Close the database connection
# cur.close()
# conn.close()

#!/usr/bin/env python3

import csv
import psycopg2
from psycopg2.extras import execute_values

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


def parse_bool(value):
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)

def parse_int(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None

# Connect to the database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cur = conn.cursor()

# Clear existing data to make it idempotent
cur.execute("TRUNCATE TABLE script_lines RESTART IDENTITY CASCADE;")
conn.commit()
print("Cleared existing data from script_lines table")

# Import script_lines
error_count = 0
successful_count = 0

with open('simpsons_script_lines.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    batch_size = 1000
    batch = []

    for row in reader:
        try:
            processed_row = [
                parse_int(row[0]),     # id
                parse_int(row[1]),     # episode_id
                parse_int(row[2]),     # number
                row[3],                # raw_text
                parse_int(row[4]),     # timestamp_in_ms
                parse_bool(row[5]),    # speaking_line
                parse_int(row[6]),     # character_id
                parse_int(row[7]),     # location_id
                row[8],                # raw_character_text
                row[9],                # raw_location_text
                row[10],               # spoken_words
                row[11],               # normalized_text
                parse_int(row[12])     # word_count
            ]

            batch.append(tuple(processed_row))

            if len(batch) >= batch_size:
                try:
                    execute_values(cur, """
                        INSERT INTO script_lines 
                        (id, episode_id, number, raw_text, timestamp_in_ms, speaking_line, 
                         character_id, location_id, raw_character_text, raw_location_text, 
                         spoken_words, normalized_text, word_count)
                        VALUES %s
                        ON CONFLICT (id) DO NOTHING
                    """, batch)
                    conn.commit()
                    successful_count += len(batch)
                except psycopg2.Error as e:
                    print(f"Error inserting batch: {str(e)}")
                    conn.rollback()
                    error_count += len(batch)
                finally:
                    batch = []

        except Exception as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {str(e)}")
            error_count += 1
            continue

    # Insert any remaining rows
    if batch:
        try:
            execute_values(cur, """
                INSERT INTO script_lines 
                (id, episode_id, number, raw_text, timestamp_in_ms, speaking_line, 
                 character_id, location_id, raw_character_text, raw_location_text, 
                 spoken_words, normalized_text, word_count)
                VALUES %s
                ON CONFLICT (id) DO NOTHING
            """, batch)
            conn.commit()
            successful_count += len(batch)
        except psycopg2.Error as e:
            print(f"Error inserting final batch: {str(e)}")
            conn.rollback()
            error_count += len(batch)

print(f"Import completed. {successful_count} lines successfully imported. {error_count} lines failed to import.")

# Close the database connection
cur.close()
conn.close()