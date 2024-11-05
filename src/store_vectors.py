import fitz  # PyMuPDF
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext, load_index_from_storage
from config import DB_CONFIG, get_embeddings, VECTOR_STORE_COLLECTION_NAME, get_connection_string

def extract_text_with_structure(file_path):
    """Extract text from PDF while preserving structure."""
    if str(file_path).endswith('.pdf'):
        doc = fitz.open(str(file_path))
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()
        return text
    return None

def split_text_into_paragraphs(text):
    """Split text into paragraphs."""
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

def process_and_store_documents():
    try:
        # Initialize vector store
        vector_store = PGVectorStore.from_params(
            database=DB_CONFIG['dbname'],
            host=DB_CONFIG['host'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            table_name=VECTOR_STORE_COLLECTION_NAME,
            embed_dim=384  # for multilingual-e5-large
        )

        # Create storage context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Load documents with custom PDF handling
        reader = SimpleDirectoryReader(
            input_dir='data/pdfs',
            recursive=True,
            filename_as_id=True,
            required_exts=['.pdf'],
            file_extractor={
                ".pdf": extract_text_with_structure
            }
        )
        documents = reader.load_data()

        # Create and store index
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=get_embeddings()
        )

        print(f"Successfully processed and stored {len(documents)} documents")
        return index

    except Exception as e:
        print(f"Error processing documents: {e}")
        raise

def load_existing_index():
    try:
        # Initialize vector store
        vector_store = PGVectorStore.from_params(
            database=DB_CONFIG['dbname'],
            host=DB_CONFIG['host'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            table_name=VECTOR_STORE_COLLECTION_NAME,
            embed_dim=384
        )

        # Create storage context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Load index
        index = load_index_from_storage(storage_context)
        print("Successfully loaded existing index")
        return index

    except Exception as e:
        print(f"Error loading index: {e}")
        raise

if __name__ == "__main__":
    process_and_store_documents()