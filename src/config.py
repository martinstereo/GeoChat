import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Embedding Model configuration
SENTENCE_MODEL = "intfloat/multilingual-e5-large"  # Model for sentence embeddings

# Database configuration
DB_CONFIG = {
    'dbname': 'geo_chat',
    'user': 'martin',
    'password': 'martin',  # Make sure to set your actual password here
    'host': 'localhost',
    'port': '5432'
}
