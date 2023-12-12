# vector_db.py
# Handles interactions with the vector database (Pinecone), like fetching similar vectors.
import pinecone
import os
from .config import Config

# Initialize Pinecone
pinecone.init(api_key=Config.PINECONE_API_KEY, environment='gcp-starter')

# Connect to your Pinecone index
index_name = Config.PINECONE_INDEX_NAME
index = pinecone.Index(index_name)

def fetch_similar_vectors(embedded_vector, top_k=6):
    """
    Fetches the top_k most similar vectors from the Pinecone index.

    :param embedded_vector: The query vector. Type list.
    :param top_k: Number of similar vectors to retrieve.
    :return: A dictionary of similar vectors.
    """
    # ensure that embedded_vector is a list
    if not isinstance(embedded_vector, list):
        raise TypeError("embedded_vector must be a list")
    
    try:
        query_result = index.query(vector=embedded_vector, top_k=top_k)
        # Process the query_result as per your application's need
        return query_result['matches']
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        # Handle the exception as appropriate for your application
        return None


