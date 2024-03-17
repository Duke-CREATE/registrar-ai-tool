from .embed import embed_message
from .vector_db import fetch_similar_vectors
from .search_tags import context_from_tags
from .generate_response import create_context
import uuid

def class_info(data, thread_id, CONVERSATION_CACHE):
    """
    Logic for handling questions regarding class information.
    Input: None
    Output: None
    """
    conversation_history = data.get('conversation_history')
    user_message = data.get('user_message')
    tags = data.get('tags')

    # append the user message to the conversation cache (by thread_id)
    if thread_id in CONVERSATION_CACHE:
        CONVERSATION_CACHE[thread_id].append({'message': user_message ,'fromUser': True})
    else:
        CONVERSATION_CACHE[thread_id] = [{'message': user_message ,'fromUser': True}]

    relevant_info = []
    # if we are in a thread
    if conversation_history:
        # response inherits parent thread thread_id
        response_thread_id = thread_id
        # response is not a parent
        is_parent = False
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
        # generate new threadid
        response_thread_id = str(uuid.uuid4())
        # response is a parent
        is_parent = True
        # if tags are provided, fetch context from tags
        if tags:
            relevant_info = context_from_tags(tags)
        # if no tags are provided, use the user message to fetch similar vectors
        else:
            # Embed the user message and fetch similar vectors
            embedded_message = embed_message(user_message)
            similar_vectors = fetch_similar_vectors(embedded_message, 'courses')
            # Generate context based on similar vectors
            relevant_info = create_context(similar_vectors)
            print('relevant info:')
            print(relevant_info)

    # if not user_message and not relevant_info:
    #     return jsonify({'error': 'No message provided'}), 400
    
    return response_thread_id, relevant_info, is_parent