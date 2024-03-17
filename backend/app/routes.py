# routes.py
from flask import Blueprint, request, jsonify
from .embed import embed_message
from .vector_db import fetch_similar_vectors
from .generate_response import generate_openai_response, create_context_reg
from .handle_query_type import class_info
import uuid
from flask_cors import cross_origin

# Initialize a global dictionary for storing conversation histories
CONVERSATION_CACHE = {}

main = Blueprint('main', __name__)

@main.route('/process_message', methods=['POST'])
@cross_origin()
def process_message():
    # get data
    data = request.get_json()
    print(data)
    user_message = data.get('user_message')
    query_type = data.get('query_type')
    if not data.get('threadId'):
        thread_id = str(uuid.uuid4())
        data['threadId'] = thread_id
    else:
        thread_id = data['threadId']

    # HANDLE QUERY TYPES
    if query_type == 'Class Info':
        response_thread_id, relevant_info, is_parent = class_info(data, thread_id, CONVERSATION_CACHE)
        print('relevant info:')
        print(relevant_info)
        response = generate_openai_response(user_message, relevant_info)
    elif query_type == 'Registration':
        # TODO: build threading for registration
        # TODO: generate thread id for registration
        # embed user message
        embedded_message = embed_message(user_message)
        # fetch similar vectors from registration vector DB
        similar_vectors = fetch_similar_vectors(embedded_message, 'registration-vdb', top_k=3, num_candidates=20)
        print('similar vectors reg')
        print(similar_vectors)
        # create context from similar vectors
        relevant_info = create_context_reg(similar_vectors)
        print('relevant info registration:')
        print(relevant_info)
        # generate openai response
        response = generate_openai_response(user_message, relevant_info)
    elif query_type == 'Other':
        response = generate_openai_response(user_message, "")
    else:
        print('Error: Invalid query type')

    if not user_message and not relevant_info:
        return jsonify({'error': 'No message provided'}), 400

    try:
        print(response)
        # append the response to the conversation cache
        if response_thread_id in CONVERSATION_CACHE:
            CONVERSATION_CACHE[response_thread_id].append({'message': response, 'context': relevant_info, 'fromUser': False})
        else:
            CONVERSATION_CACHE[response_thread_id] = [{'message': response, 'context': relevant_info, 'fromUser': False}]

        print()
        print('RESPONSE')
        print(response)
        print(response_thread_id)
        print('RESPONSE END')

        return jsonify({'response': response, 'threadId': response_thread_id, 'isParent': is_parent})
    except Exception as e:
        return jsonify({'error': str(e)}), 500