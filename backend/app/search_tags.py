from pymongo import MongoClient
from .config import Config

def context_from_tags(tags):
    """
    Creates a context from the given tags. Searches for courses based on the tags in data/coursesDB.db.

    :param tags: A list of class tags.
    :return: A dictionary containing the class descriptions for each tag.
    """
    client = MongoClient(Config.MONGODB_URI)
    db = client['courses']  # Adjust database name as necessary
    collection = db['fa23-sp24-info']    # Adjust collection name as necessary
    results = {}

    for tag in tags:
        print(tag)
        course = collection.find_one({'Code': tag})
        if course:
            # Map the MongoDB document fields to the desired format
            result_dict = {
                'Course Name': course.get('Course Name', ''),
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
