import psycopg2
import sys
from psycopg2 import sql

def update_db_from_file(db_name, table_name, new_column_name, txt_file_path):
    conn = psycopg2.connect(f"dbname={db_name}")
    cursor = conn.cursor()

    try:
        # Check if the column already exists
        cursor.execute(sql.SQL("SELECT * FROM {} LIMIT 0").format(sql.Identifier(table_name)))
        columns = [desc[0] for desc in cursor.description]
        if new_column_name not in columns:
            # Add the new column to the table
            cursor.execute(
                sql.SQL("ALTER TABLE {} ADD COLUMN {} TEXT").format(
                    sql.Identifier(table_name),
                    sql.Identifier(new_column_name)
                )
            )
            print(f"Added new column '{new_column_name}' to table '{table_name}'.")
        else:
            print(f"Column '{new_column_name}' already exists. Proceeding with update.")

        # Read the strings from the text file
        with open(txt_file_path, 'r') as file:
            strings = file.readlines()

        # Get all ids from the table
        cursor.execute(sql.SQL("SELECT id FROM {} ORDER BY id").format(sql.Identifier(table_name)))
        ids = [row[0] for row in cursor.fetchall()]

        # Update the table with the strings using a loop
        for i, string in enumerate(strings):
            if i < len(ids):
                cursor.execute(sql.SQL("""
                    UPDATE {}
                    SET {} = %s
                    WHERE id = %s
                """).format(
                    sql.Identifier(table_name),
                    sql.Identifier(new_column_name)
                ), (string.strip(), ids[i]))
            else:
                print(f"Warning: More lines in file than rows in table. Stopped at line {i+1}.")
                break

        # Commit the changes
        conn.commit()
        print(f"Successfully updated {min(len(strings), len(ids))} rows in {table_name}")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py database_name table_name new_column_name strings.txt")
        sys.exit(1)

    db_name = sys.argv[1]
    table_name = sys.argv[2]
    new_column_name = sys.argv[3]
    txt_file_path = sys.argv[4]

    update_db_from_file(db_name, table_name, new_column_name, txt_file_path)