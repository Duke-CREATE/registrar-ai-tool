# Manages the communication with OpenAI's GPT-3.5 Turbo model.
from .config import Config
import openai as OpenAI
import sqlite3

def create_context(matches):
    """
    Creates a context from the similar vectors. Matches vector ids to course descriptions in data/coursesDB.db.

    :param similar_vectors: A list of dictionaries with keys 'id' and 'score'.
    :return: A string representing the context.
    """
    courses_info = ""
    with sqlite3.connect('data/coursesDB.db') as conn:
        cursor = conn.cursor()
        for match in matches:
            course_id = match['id']
            # Use parameterized queries to prevent SQL injection
            sql = """
                    SELECT
                        Descr,
                        `Course Long Descr`,
                        `Mtg Start`,
                        `Mtg End`,
                        Pat,
                        `Term Descr`
                    FROM
                        courses
                    WHERE
                        `Course ID` = ?
                  """
            cursor.execute(sql, (course_id,))

            result = cursor.fetchone()
            result_dict = {
                'course name': result[0],
                'course description': result[1],
                'start time': result[2],
                'end time': result[3],
                'days offered': result[4],
                'term': result[5]
            }

            # Format the result dictionary into a string
            course_info_str = ', '.join([f"{key}: {value}" for key, value in result_dict.items()])
            courses_info += course_info_str + "\n"

    return courses_info


def generate_openai_response(user_message, courses_info):
    """
    Given the courses_info, generates a response using OpenAI's GPT-3.5 Turbo model.

    :param courses_info: A string representing the context.
    :return: A string representing the response.
    """
    # connect to OpenAI
    client = OpenAI.Client(api_key=Config.OPENAI_API_KEY)

    # Create the prompt
    context = (
        "You are a helpful course registration assistant at Duke University. "
        "Your task is to answer questions about courses confidently and in a friendly manner. "
        "Keep your answers short, concise, and conversational. "
        "If the information provided does not allow you to answer a question, respond with 'Sorry, I'm not equipped to answer that question'.'\n\n"
        "Courses Information:\n"
        f"{courses_info}\n\n"
        "User Query: "
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
