# embed.py
import requests
from .config import Config
def embed_message(user_message):
    """
    Sends a request to the specified Hugging Face model API and returns the response.
    :param payload: The data to send in the request.
    :return: The JSON response from the API.
    """
    api_key = Config.EMBEDDINGS_API_KEY
    api_url = Config.EMBEDDINGS_API_URL
    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")
    payload = {
        "inputs": user_message,
        "parameters": {}
    }
    emb_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + Config.EMBEDDINGS_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(Config.EMBEDDINGS_API_URL, headers=emb_headers, json=payload)
    return response.json()['embeddings']