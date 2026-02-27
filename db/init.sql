CREATE TABLE IF NOT EXISTS works (
    id TEXT PRIMARY KEY,
    doi TEXT,
    title TEXT,
    publication_year INT,
    publication_date DATE,
    updated_date TIMESTAMP
);

CREATE TABLE ingestion_metadata (
    source TEXT PRIMARY KEY,
    last_updated_date TIMESTAMP NOT NULL,
    last_run_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO ingestion_metadata (source, last_updated_date)
VALUES ('openalex', '1900-01-01')
ON CONFLICT (source) DO NOTHING;