CREATE TABLE pdf_vectors (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,  -- The name of the PDF file
    vector FLOAT8[] NOT NULL,         -- The vector representation (array of floats)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);