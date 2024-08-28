#!/bin/bash

while true; do
    # Run the import script and capture its output
    output=$(./import_csv.sh 2>&1)
    echo "$output"

    # Use regex to find the line number
    if [[ $output =~ COPY\ script_lines,\ line\ ([0-9]+): ]]; then
        line_number="${BASH_REMATCH[1]}"
        echo "Found problematic line: $line_number"
        
        # Delete the problematic line
        python drow.py simpsons_script_lines.csv "$line_number"
    else
        echo "No more errors found or unexpected error format. Exiting."
        break
    fi
done

echo "Process completed."