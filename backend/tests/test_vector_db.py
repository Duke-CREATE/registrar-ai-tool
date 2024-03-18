import sys
import os
import pytest
import pinecone
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.fetch_db import fetch_similar_vectors
from app.config import Config

def test_fetch_similar_vectors_integration():
    """
    Tests the fetch_similar_vectors function.

    :return: None
    """
    # Ensure Pinecone API key and index name are set
    assert Config.PINECONE_API_KEY is not None
    assert Config.PINECONE_INDEX_NAME is not None

    # get environment variables from config
    pinecone_index_name = Config.PINECONE_INDEX_NAME
    pinecone_api_key = Config.PINECONE_API_KEY
    pinecone_environment = Config.PINECONE_ENVIRONMENT

    # Initialize Pinecone
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

    # Ensure the Pinecone index exists
    assert pinecone_index_name in pinecone.list_indexes()

    # Connect to index
    index = pinecone.Index(pinecone_index_name)

    # Ensure the index is not None
    assert index is not None

    # Fetch a vector from the index
    vector = index.fetch(ids=['175'])
    vector = vector['vectors']['175']['values']

    # Ensure the vector is not None
    assert vector is not None

    # Fetch similar vectors
    similar_vectors = fetch_similar_vectors(vector, top_k=5)
    # create a file with the similar vectors
    with open('similar_vectors.txt', 'w') as f:
        f.write(str(similar_vectors))

    # Ensure the similar vectors are not None
    assert similar_vectors is not None

    # print the similar vectors
    # print(similar_vectors)

