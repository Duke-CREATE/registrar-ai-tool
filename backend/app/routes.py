# routes.py
from flask import Blueprint, request, jsonify, current_app
import redis
import json
from .config import Config
from .generate_response import generate_openai_response
from .handle_query_type import fetch_class_info_registration, fetch_other
import uuid
from flask_cors import cross_origin

main = Blueprint('main', __name__)

# Then later in your code, inside a function or factory where `current_app` is available:
def get_redis_client():
    redis_url = Config.CACHE_REDIS_URL  # Use the actual config key for your Redis URL
    return redis.Redis.from_url(redis_url, decode_responses=True)

@main.route('/process_message', methods=['POST'])
@cross_origin()
def process_message():
    # get data
    data = request.get_json()
    print(data)
    user_message = data.get('user_message')
    query_type = data.get('query_type')
    if data['threadId'] == '':
        thread_id = str(uuid.uuid4())
        data['threadId'] = thread_id
    else:
        thread_id = data['threadId']
    
    # Initialize Redis client and fetch the relevant thread
    redis_client = get_redis_client()
    print('thread id pre cache:', thread_id)
    cached_thread = json.loads(redis_client.get(thread_id) or '[]')
    print()
    print('CACHED THREAD:')
    print(cached_thread)
    print()

    response = ""  # Initialize response variable
    if query_type in ['Class Info', 'Registration']:
        response_thread_id, relevant_info, is_parent = fetch_class_info_registration(data, thread_id, query_type, cached_thread)
    elif query_type == 'Other':
        response_thread_id, relevant_info, is_parent = fetch_other(data, thread_id, cached_thread)
    else:
        return jsonify({'error': 'Invalid query type'}), 400

    if not user_message and not relevant_info:
        return jsonify({'error': 'No message provided'}), 400

    # generate openai response
    print()
    print('relevant info:')
    print(relevant_info)
    print()
    response = generate_openai_response(user_message, relevant_info)

    try:
        # Append the new user message to the conversation history
        if user_message:
            user_cached_thread = [{'message': user_message, 'context': '', 'fromUser': True}]
            redis_client.set(thread_id, json.dumps(user_cached_thread))  # Store the updated conversation
        # Append the new system response to the conversation history
        if response:  # Check if there is a system response to append
            cached_thread.append({'message': response, 'context': relevant_info, 'fromUser': False})
            redis_client.set(response_thread_id, json.dumps(cached_thread))  # Store the updated conversation
        print('response:', response)
        print('response thread_id:', response_thread_id)
        return jsonify({'response': response, 'threadId': response_thread_id, 'isParent': is_parent})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

