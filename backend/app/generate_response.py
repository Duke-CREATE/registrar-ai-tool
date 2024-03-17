# Manages the communication with OpenAI's GPT-3.5 Turbo model.
from .config import Config
import openai as OpenAI
from pymongo import MongoClient

def create_context_reg(matches):
    """
    Creates context from the similar vectors
    """
    relevant_info = ""
    for match in matches:
        relevant_info += match['text'] + '\n'
    
    return relevant_info


def create_context(matches):
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

def generate_openai_response(user_message, courses_info):
    """
    Given the courses_info, generates a response using OpenAI's GPT-3.5 Turbo model.

    :param courses_info: A string representing the context.
    :return: A string representing the response.
    """
    # connect to OpenAI
    client = OpenAI.Client(api_key=Config.OPENAI_API_KEY)

    if courses_info:
        # Create the prompt
        context = (
            "You are a helpful course registration assistant at Duke University. "
            "Your task is to answer questions about courses confidently and in a friendly manner. "
            "Keep your answers short, concise, and conversational. Only give the user the information they're asking for. "
            "Adjust capitalization and punctuation as needed. "
            "If the information provided does not allow you to answer a question, respond with 'Sorry, I'm not equipped to answer that question'.'\n\n"
            "Courses Information:\n"
            f"{courses_info}\n\n"
            "User Query: "
        )
    else:
        context = (
            "You are a helpful course registration assistant at Duke University. "
            "Your task is to answer questions about courses confidently and in a friendly manner. "
            "Encourage the user to ask questions about classes available at Duke as well as general questions about registration."
        )

    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_message}
            ]
        )

        # Get the response from the completion
        response = completion.choices[0].message.content

        # Check if the reply is empty, indicating the question may be out of context
        if not response:
            response = "I am sorry, but I am not equipped to answer that question."
    except Exception as e:
        print("Failed to generate response.")
        print(e)
    
    return response
