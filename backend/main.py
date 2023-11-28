from langchain.llms import OpenAI
import os

# Fetch api key from .env file
from dotenv import load_dotenv
load_dotenv()

def generate_dog_names():
    # Initialize the LangChain OpenAI model
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7)

    # Your prompt
    prompt = "Suggest five unique and cool dog names."

    # Generating response
    response = llm(prompt)

    return response

if __name__ == "__main__":
    dog_names = generate_dog_names()
    print("Suggested Dog Names:")
    print(dog_names)
