import csv
import sys

def remove_columns(input_file, output_file, columns_to_remove):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read the header
        header = next(reader)
        
        # Find the indices of columns to remove
        indices_to_remove = [header.index(col) for col in columns_to_remove if col in header]
        
        # Write the new header
        new_header = [col for i, col in enumerate(header) if i not in indices_to_remove]
        writer.writerow(new_header)

        # Write the data
        for row in reader:
            new_row = [col for i, col in enumerate(row) if i not in indices_to_remove]
            writer.writerow(new_row)

    print(f"Processed {input_file}. Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py input_file output_file column1 [column2 ...]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    columns_to_remove = sys.argv[3:]

    remove_columns(input_file, output_file, columns_to_remove)