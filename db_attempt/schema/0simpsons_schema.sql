-- Characters table
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    normalized_name VARCHAR NOT NULL,
    gender VARCHAR
);

-- Episodes table
CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    number_in_season INTEGER,
    number_in_series INTEGER,
    original_air_date DATE,
    original_air_year INTEGER,
    season INTEGER,
    title VARCHAR NOT NULL
);

-- Locations table
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    normalized_name VARCHAR NOT NULL
);

-- Script lines table
CREATE TABLE script_lines (
    id INTEGER PRIMARY KEY,
    episode_id INTEGER NOT NULL,
    number INTEGER,
    raw_text TEXT,
    timestamp_in_ms INTEGER,
    speaking_line BOOLEAN,
    character_id INTEGER,
    location_id INTEGER,
    raw_character_text VARCHAR,
    raw_location_text VARCHAR,
    spoken_words TEXT,
    normalized_text TEXT,
    word_count INTEGER
);

-- Add foreign key constraints
ALTER TABLE script_lines
    ADD CONSTRAINT fk_script_lines_episode
    FOREIGN KEY (episode_id) REFERENCES episodes(id);

ALTER TABLE script_lines
    ADD CONSTRAINT fk_script_lines_character
    FOREIGN KEY (character_id) REFERENCES characters(id);

ALTER TABLE script_lines
    ADD CONSTRAINT fk_script_lines_location
    FOREIGN KEY (location_id) REFERENCES locations(id);