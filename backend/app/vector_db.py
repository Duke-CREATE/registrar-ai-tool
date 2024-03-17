from pymongo import MongoClient
from .config import Config

def fetch_similar_vectors(embedded_message, db_name, top_k=6, num_candidates=50):
    """
    Fetches the top_k most similar vectors from the MongoDB 'embeddings' collection using vector similarity search.

    :param embedded_message: The query vector. Type list of floats.
    :param top_k: Number of similar vectors to retrieve.
    :param num_candidates: Number of candidate vectors to evaluate in the search. Higher values increase accuracy but reduce performance.
    :return: A list of documents with similar vectors.
    """
    if db_name == 'courses':
        collection_name = 'fa23-sp24-embeddings'
        index = 'course_embeddings'
    elif db_name == 'registration-vdb':
        collection_name = 'embeddings'
        index = 'vector_index'
    else:
        raise TypeError("Invalid DB name")
    # ensure that embedded_vector is a list of floats
    if not isinstance(embedded_message, list) or not all(isinstance(x, float) for x in embedded_message):
        raise TypeError("embedded_vector must be a list of floats")

    # Connect to MongoDB
    client = MongoClient(Config.MONGODB_URI)
    db = client[db_name]  # Adjust database name as necessary
    collection = db[collection_name]    # Adjust collection name as necessary

    # Create the vector search query
    query = [
        {
            "$vectorSearch": {
                "index": index,
                "path": "embedding",
                "queryVector": embedded_message,
                "numCandidates": num_candidates,
                "limit": top_k
            }
        }
    ]

    # Execute the vector search query
    try:
        results = list(collection.aggregate(query))
    except Exception as e:
        print(f"Error performing vector search in MongoDB: {e}")
        results = []  # Return an empty list in case of error

    # Close the MongoDB connection
    client.close()

    # Return the list of similar vector documents
    return results
