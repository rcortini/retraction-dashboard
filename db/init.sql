CREATE TABLE IF NOT EXISTS works (
    id TEXT PRIMARY KEY,
    title TEXT,
    publication_year INT,
    publication_date DATE,
    updated_date TIMESTAMP,
    is_retracted BOOLEAN,
    doi TEXT,
    -- journal TEXT,
    -- country TEXT,
    raw JSONB
);

CREATE TABLE IF NOT EXISTS ingestion_metadata (
    id SERIAL PRIMARY KEY,
    last_updated_date TIMESTAMP
);

INSERT INTO ingestion_metadata (last_updated_date)
SELECT '1900-01-01'
WHERE NOT EXISTS (SELECT 1 FROM ingestion_metadata);