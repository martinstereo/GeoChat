# src/store_vectors.py
import os
import psycopg2
from unstructured.partition.pdf import partition_pdf
from sentence_transformers import SentenceTransformer
from config import DB_CONFIG, SENTENCE_MODEL

def extract_text_from_pdfs(pdf_folder):
    """Extract text from all PDF files in a given folder using unstructured."""


def store_vectors_in_db(pdf_folder):
    """Store vectors of PDFs in the PostgreSQL database."""
    # Connect to the database
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Extract text from PDFs
    pdf_texts = extract_text_from_pdfs(pdf_folder)

    # Initialize SentenceTransformer model
    model = SentenceTransformer(SENTENCE_MODEL)

    for filename, text in pdf_texts.items():
        # Split the text into sentences for embedding
        sentences = text.split('. ')  # Simple split by period. Adjust as needed.

        # Generate embeddings for the sentences
        embeddings = model.encode(sentences, convert_to_tensor=True)

        # Store each embedding in the database
        for i, embedding in enumerate(embeddings):
            cursor.execute("""
                INSERT INTO pdf_vectors (filename, vector) VALUES (%s, %s);
            """, (filename, embedding.numpy().tolist()))  # Convert tensor to list for storage

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Specify the folder where your PDFs are stored
    pdf_folder = 'data/pdfs'
    store_vectors_in_db(pdf_folder)
    print("Vectors stored in database successfully.")
