# routes.py
from flask import Blueprint, request, jsonify
import redis
import json
from .config import Config
from .generate_response import generate_openai_response
from .handle_query_type import fetch_class_info_registration, fetch_other
from .fetch_db import store_data
import uuid
from flask_cors import cross_origin

main = Blueprint('main', __name__)

def get_redis_client():
    """
    Initializes and returns redis client
    Input: None
    Output: redis client
    """
    redis_url = Config.CACHE_REDIS_URL  # Use the actual config key for your Redis URL
    return redis.Redis.from_url(redis_url, decode_responses=True)

@main.route('/process_message', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_message():
    if request.method == 'OPTIONS':
        # Handles CORS preflight requests; these require no further processing
        return ('', 204)
    # get data
    data = request.get_json()
    user_message = data.get('user_message')
    query_type = data.get('query_type')
    if data['threadId'] == '':
        thread_id = str(uuid.uuid4())
        data['threadId'] = thread_id
    else:
        thread_id = data['threadId']
    
    # Store data in user data
    store_data(data)
    
    # Initialize Redis client and fetch the relevant thread
    redis_client = get_redis_client()
    cached_thread = json.loads(redis_client.get(thread_id) or '[]')

    response = []  # Initialize response variable
    if query_type in ['Class Info', 'Registration']:
        response_thread_id, relevant_info, is_parent = fetch_class_info_registration(data, thread_id, query_type, cached_thread)
    elif query_type == 'Other':
        response_thread_id, relevant_info, is_parent = fetch_other(thread_id, cached_thread)
    else:
        return jsonify({'error': 'Invalid query type'}), 400

    if not user_message and not relevant_info:
        return jsonify({'error': 'No message provided'}), 400

    # generate openai response
    response = generate_openai_response(user_message, relevant_info, query_type)

    try:
        # Append the new user message to the conversation history
        if user_message:
            user_cached_thread = [{'message': user_message, 'context': '', 'fromUser': True}]
            redis_client.set(thread_id, json.dumps(user_cached_thread))  # Store the updated conversation
        # Append the new system response to the conversation history
        if response:  # Check if there is a system response to append
            cached_thread.append({'message': response, 'context': relevant_info, 'fromUser': False})
            redis_client.set(response_thread_id, json.dumps(cached_thread))  # Store the updated conversation
        return jsonify({'response': response, 'threadId': response_thread_id, 'isParent': is_parent})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

