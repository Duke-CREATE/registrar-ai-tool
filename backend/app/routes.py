# routes.py
from flask import Blueprint, request, jsonify
from .embed import embed_message
from .vector_db import fetch_similar_vectors
from .search_tags import context_from_tags
from .generate_response import generate_openai_response, create_context
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
    conversation_history = data.get('conversation_history')
    user_message = data.get('user_message')
    tags = data.get('tags')
    if data['threadId'] == '':
        thread_id = str(uuid.uuid4())
        data['threadId'] = thread_id
    else:
        thread_id = data.get('threadId')  # assign new threadID
    
    print('DATA BEGIN')
    print(data)
    print('DATA END')

    # append the user message to the conversation cache (by thread_id)
    if thread_id in CONVERSATION_CACHE:
        CONVERSATION_CACHE[thread_id].append({'message': user_message ,'fromUser': True})
    else:
        CONVERSATION_CACHE[thread_id] = [{'message': user_message ,'fromUser': True}]

    relevant_info = []
    # if we are in a thread
    if conversation_history:
        print()
        print('CONVERSATION CACHE START')
        print(CONVERSATION_CACHE[thread_id])
        print('CONVERSATION CACHE END')
        # fetch the conversation history from the cache
        CONVERSATION_CACHE.setdefault(thread_id, [])  
        CONVERSATION_CACHE[thread_id].append({'message': user_message, 'context': None ,'fromUser': True})
        # fetch previous relevant info from the conversation history
        for msg in CONVERSATION_CACHE[thread_id]:
            if not msg['fromUser']:
                relevant_info.append(msg['context'])
                relevant_info.append(msg['message'])
            else:
                relevant_info.append(msg['message'])
        # if tags are provided, fetch context from tags
        if tags:
            tag_context = context_from_tags(tags)
            relevant_info.extend(tag_context)
    # else we are not in a thread
    else:
        # if tags are provided, fetch context from tags
        if tags:
            relevant_info = context_from_tags(tags)
        # if no tags are provided, use the user message to fetch similar vectors
        else:
            # Embed the user message and fetch similar vectors
            embedded_message = embed_message(user_message)
            similar_vectors = fetch_similar_vectors(embedded_message)
            # Generate context based on similar vectors
            relevant_info = create_context(similar_vectors)

    if not user_message and not relevant_info:
        return jsonify({'error': 'No message provided'}), 400

    try:
        print()
        print('PREVIOUS RELEVANT INFO START')
        print(relevant_info)
        print('PREVIOUS RELEVANT INFO END')
        response = generate_openai_response(user_message, relevant_info)
        # append the response to the conversation cache
        # generate new threadid using current timestamp
        response_thread_id = str(uuid.uuid4())
        if response_thread_id in CONVERSATION_CACHE:
            CONVERSATION_CACHE[response_thread_id].append({'message': response, 'context': relevant_info, 'fromUser': False})
        else:
            CONVERSATION_CACHE[response_thread_id] = [{'message': response, 'context': relevant_info, 'fromUser': False}]

        print()
        print('RESPONSE')
        print(response)
        print(response_thread_id)
        print('RESPONSE END')

        return jsonify({'response': response, 'threadId': response_thread_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500