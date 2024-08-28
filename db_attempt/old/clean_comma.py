import csv
import sys

def clean_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            # Ensure each row has the correct number of fields
            if len(row) >= 6:  # Assuming 6 is the correct number of columns
                id, episode_id, raw_text, character_id, location_id, word_count = row[:6]
                # Combine any extra fields into raw_text
                if len(row) > 6:
                    raw_text += " " + " ".join(row[6:])
                writer.writerow([id, episode_id, raw_text, character_id, location_id, word_count])
            else:
                print(f"Skipping malformed row: {row}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_csv.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    clean_csv(input_file, output_file)
    print(f"Cleaned CSV saved to {output_file}")