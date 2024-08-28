import psycopg2
import csv
import ollama
import json

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


def get_scene_info(scene_text, location):
    query = f"""
    Location: {location}

    Scene:
    {scene_text}

    Summarize this scene and provide the following information in JSON format:
    - title: a brief, informative title for the scene (just a few words)
    - summary: a one to two sentence summary of what happens in the scene
    - characters: a list of the characters that appear in the scene
    - location: the location where the scene takes place

    Respond only with the JSON object.
    """

    print(f"Sending query to LLM for location: {location}")
    response = ollama.chat(model='summaryAgent', messages=[{'role': 'user', 'content': query}])
    print("Received response from LLM")
    return response['message']['content']

def process_llm_response(scene_info):
    try:
        # Parse the JSON string
        data = json.loads(scene_info)
        # Extract the required fields
        return [
            data.get('title', ''),
            data.get('summary', ''),
            ', '.join(data.get('characters', [])),  # Join the list of characters
            data.get('location', '')
        ]
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {scene_info}")
        return ['', '', '', '']  # Return empty strings if parsing fails

def process_script_lines(db_params, output_file):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT number, raw_text, character_id, location_id,
                   (SELECT name FROM locations WHERE id = script_lines_tiny.location_id) as location_name
            FROM script_lines_tiny
            ORDER BY number
        """)

        print("Successfully executed database query")

        current_location_id = None
        scene_text = ""
        scene_count = 0

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csvwriter.writerow(['title', 'summary', 'characters', 'location'])

            for row in cursor:
                number, raw_text, character_id, location_id, location_name = row
                print(f"Processing row {number}")

                if location_id != current_location_id and scene_text:
                    print(f"Location changed. Processing scene for location: {location_name}")
                    scene_info = get_scene_info(scene_text, location_name)
                    print("Scene info received:")
                    print(scene_info)

                    scene_data = process_llm_response(scene_info)
                    if any(scene_data):  # Only write if there's any non-empty data
                        csvwriter.writerow(scene_data)
                        scene_count += 1
                        print(f"Wrote scene {scene_count} to CSV")

                    scene_text = ""

                current_location_id = location_id
                scene_text += raw_text + " "

            # Process the last scene
            if scene_text:
                print(f"Processing final scene for location: {location_name}")
                scene_info = get_scene_info(scene_text, location_name)
                print("Final scene info received:")
                print(scene_info)

                scene_data = process_llm_response(scene_info)
                if any(scene_data):  # Only write if there's any non-empty data
                    csvwriter.writerow(scene_data)
                    scene_count += 1
                    print(f"Wrote final scene {scene_count} to CSV")

        print(f"Scene analysis completed. Processed {scene_count} scenes. Results saved to {output_file}")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    output_file = 'simpsons_scene_analysis_with_custom_agent.csv'

    process_script_lines(db_params, output_file)