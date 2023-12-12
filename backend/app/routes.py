# routes.py
from flask import Blueprint, request, jsonify
from .embed import embed_message
from .vector_db import fetch_similar_vectors
from .generate_response import generate_openai_response, create_context
from flask_cors import cross_origin

main = Blueprint('main', __name__)

@main.route('/process_message', methods=['POST'])
@cross_origin()
def process_message():
    # Extract 'user_message' from the request
    data = request.get_json()
    user_message = data.get('user_message')

    # Ensure user_message is provided
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Embed the user message using BERT (from embed.py)
        embedded_message = embed_message(user_message)

        # Fetch similar vectors from Pinecone (from vector_db.py)
        similar_vectors = fetch_similar_vectors(embedded_message)

        # Get courses_info from the similar vectors (from generate_response.py)
        courses_info = create_context(similar_vectors)

        # Generate a response using OpenAI's GPT-3.5 Turbo (from generate_response.py)
        response = generate_openai_response(user_message, courses_info)

        # Send the response back to the frontend
        return jsonify({'response': response})

    except Exception as e:
        # Handle exceptions and errors
        return jsonify({'error': str(e)}), 500
