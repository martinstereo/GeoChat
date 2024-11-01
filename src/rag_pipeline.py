from retriever import retrieve_vectors
from generator import generate_response
from langchain.embeddings import OpenAIEmbeddings

# Initialize OpenAI embeddings
from config import OPENAI_API_KEY
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def generate_vector(text):
    """Generate a vector representation of the text using OpenAI."""
    return embeddings.embed(text)

def rag_pipeline(query):
    """Run the RAG pipeline: retrieve and generate."""
    # Generate a vector for the query
    query_vector = generate_vector(query)

    # Retrieve relevant documents based on the query vector
    retrieved_docs = retrieve_vectors(query_vector)

    # Combine the retrieved document texts into a single context
    context = "\n".join([doc[1] for doc in retrieved_docs])  # Assuming doc[1] contains the text

    # Generate a response based on the context
    response = generate_response(context)
    return response
