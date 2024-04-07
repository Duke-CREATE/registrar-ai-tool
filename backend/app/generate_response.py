# Manages the communication with OpenAI's GPT-3.5 Turbo model.
from .config import Config
import openai as OpenAI

def generate_openai_response(user_message, courses_info, query_type):
    """
    Given the courses_info, generates a response using OpenAI's GPT-3.5 Turbo model.

    :param courses_info: A string representing the context.
    :return: A string representing the response.
    """
    # connect to OpenAI
    client = OpenAI.Client(api_key=Config.OPENAI_API_KEY)

    if query_type == 'Class Info' or query_type == 'Registration':
        if not courses_info:
            return "Sorry, I'm not equipped to answer that question."
        # Create the prompt
        context = (
            "You are a helpful course registration assistant at Duke University. "
            "Your task is to answer questions about courses confidently and in a friendly manner. "
            "Keep your answers short, concise, readable, and conversational. Only give the user the information they're asking for. "
            "Adjust capitalization as needed (no need to use all caps). "
            "If the information provided does not allow you to answer a question, respond with 'Sorry, I'm not equipped to answer that question'. "
            "For questions about classes, include the course code when possible (i.e. Intro to Machine Learning (ECE 520)\n\n"
            "Courses Information:\n"
            f"{courses_info}\n\n"
            "User Query: "
        )
    else:
        context = (
            "You are a helpful course registration assistant at Duke University. "
            "Your task is to answer questions about courses confidently and in a friendly manner. "
            "Encourage the user to ask questions about classes available at Duke as well as general questions about registration."
            "If a user asks you a question about classes or registration, do not answer this question. Instead, ask them to select "
            "the 'Class Info' or 'Registration' button above the chat field before they submit their question."
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
