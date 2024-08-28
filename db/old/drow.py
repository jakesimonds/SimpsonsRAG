import csv
import sys

def delete_row(csv_file, row_number):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Check if the row number is valid
    if row_number < 1 or row_number > len(data):
        print(f"Error: Row number {row_number} is out of range.")
        return

    # Remove the specified row
    del data[row_number - 1]

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Row {row_number} has been deleted from {csv_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python d_row.py <csv_filename> <row_number>")
        sys.exit(1)

    csv_file = sys.argv[1]
    try:
        row_number = int(sys.argv[2])
    except ValueError:
        print("Error: Row number must be an integer.")
        sys.exit(1)

    delete_row(csv_file, row_number)