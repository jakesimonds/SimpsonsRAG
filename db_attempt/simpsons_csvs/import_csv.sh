#!/bin/bash

# Database name
DB_NAME="simpsons2"

# Import characters
psql -d $DB_NAME -c "\COPY characters(id, name, normalized_name, gender) FROM 'simpsons_characters.csv' CSV HEADER;"

# Import episodes
psql -d $DB_NAME -c "\COPY episodes(id, number_in_season, number_in_series, original_air_date, original_air_year, season, title) FROM 'simpsons_episodes_.csv' CSV HEADER;"

# Import locations
psql -d $DB_NAME -c "\COPY locations(id, name, normalized_name) FROM 'simpsons_locations.csv' CSV HEADER;"



echo "Data import completed."