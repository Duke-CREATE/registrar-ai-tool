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
        collection_name = Config.COURSES_EMB_COLLECTION
        index = Config.COURSES_EMB_INDEX
    elif db_name == 'registration-vdb':
        collection_name = Config.REGISTRATION_COLLECTION
        print('collection and index:')
        print(collection_name)
        index = Config.REGISTRATION_INDEX
        print(index)
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

def create_context_tags(tags):
    """
    Creates a context from the given tags. Searches for courses based on the tags in data/coursesDB.db.

    :param tags: A list of class tags.
    :return: A dictionary containing the class descriptions for each tag.
    """
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.COURSES_DB]  # Adjust database name as necessary
    collection = db[Config.COURSES_INFO_COLLECTION]    # Adjust collection name as necessary
    results = {}

    for tag in tags:
        print(tag)
        course = collection.find_one({'Code': tag})
        if course:
            # Map the MongoDB document fields to the desired format
            result_dict = {
                'Course Name': course.get('Course Name', ''),
                'Code Code': course.get('Code', ''),
                'Course Description': course.get('Course Description', ''),
                'Credits': course.get('Max Units'),
                'Instructor': course.get('PI Name'),
                'Mode of Instruction': course.get('Mode'),
                'Start Time': course.get('Mtg Start', ''),
                'End Time': course.get('Mtg End', ''),
                'Days Offered': course.get('Pat', ''),
                'Term Offered': course.get('Term Descr', '')    
            }
            # Add result to dictionary of results
            results[tag] = result_dict
    
    return results

def create_context_registration(matches):
    """
    Creates context from the similar vectors for questions about registration.
    Input: matches
    Output: relevant_info
    """
    relevant_info = ""
    for match in matches:
        relevant_info += match['text'] + '\n'
    
    return relevant_info


def create_context_classinfo(matches):
    """
    Creates a context from the similar vectors. Matches vector ids to course descriptions in the MongoDB collection 'courses'.

    :param matches: A list of dictionaries with keys 'id' and 'score'.
    :return: A dictionary where each key is the course id and the value is the course information.
    """
    results = {}
    
    # Connect to the MongoDB. Adjust the connection string as necessary.
    client = MongoClient(Config.MONGODB_URI)
    db = client['courses']
    courses_collection = db['fa23-sp24-info']
    
    for match in matches:
        course_uuid = match['_id']
        
        # Fetch the course from the MongoDB collection
        course = courses_collection.find_one({'_id': course_uuid})
        if course:
            # Map the MongoDB document fields to the desired format
            result_dict = {
                'Course Name': course.get('Course Name', ''),
                'Code Code': course.get('Code', ''),
                'Course Description': course.get('Course Description', ''),
                'Credits': course.get('Max Units'),
                'Instructor': course.get('PI Name'),
                'Mode of Instruction': course.get('Mode'),
                'Start Time': course.get('Mtg Start', ''),
                'End Time': course.get('Mtg End', ''),
                'Days Offered': course.get('Pat', ''),
                'Term Offered': course.get('Term Descr', '')    
            }
            # Add result to dictionary of results
            results[course_uuid] = result_dict

    return results