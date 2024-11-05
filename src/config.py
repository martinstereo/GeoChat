import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


# Load environment variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Embedding configurations
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"
EMBEDDING_TYPE = os.getenv('EMBEDDING_TYPE', 'huggingface')  # 'openai' or 'huggingface'

# Get embeddings function
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# LlamaIndex configurations
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
VECTOR_STORE_COLLECTION_NAME = "document_embeddings"


# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'geo_chat'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

# Create connection string for LlamaIndex
def get_connection_string():
    return f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"