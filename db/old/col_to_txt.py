import csv
import sys

def extract_column(input_file, output_file, column_name):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        reader = csv.DictReader(infile)
        
        if column_name not in reader.fieldnames:
            print(f"Error: Column '{column_name}' not found in the CSV file.")
            sys.exit(1)
        
        for row in reader:
            outfile.write(row[column_name] + '\n')

    print(f"Extracted column '{column_name}' from {input_file}. Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input_file.csv output_file.txt column_name")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    column_name = sys.argv[3]

    extract_column(input_file, output_file, column_name)