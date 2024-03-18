from flask import current_app
import uuid
from .embed import embed_message
from .vector_db import fetch_similar_vectors
from .search_tags import context_from_tags
from .generate_response import create_context, create_context_reg

def fetch_class_info_registration(data, thread_id, query_type, cached_thread):
    """
    Logic for handling questions regarding class information.
    Input: data, thread_id
    Output: response_thread_id, relevant_info, is_parent
    """
    conversation_history = data.get('conversation_history')
    user_message = data.get('user_message')
    tags = data.get('tags')

    relevant_info = []
    # if we are in a thread
    if cached_thread:
        # response inherits thread_id
        response_thread_id = thread_id
        # response is not parent
        is_parent = False
        # for message in cached thread
        for message in cached_thread:
            if message['fromUser'] == True:
                sender = 'User'
                msg_text = message['message']
                msg_str = f"{sender}: {msg_text}\n"
            else:
                sender = 'Duke Atlas Chatbot'
                context = message['context']
                msg_text = message['message']
                msg_str = f"Context: {context}\n{sender}: {msg_text}\n"

            relevant_info.append(msg_str)
        relevant_info.append('Duke Atlas Chatbot:')

        if tags:
            tag_context = context_from_tags(tags)
            relevant_info.extend(f"Context: {tag_context}")
    # else if we are not in a thread
    else:
        # generate new thread ID
        response_thread_id = str(uuid.uuid4())
        # response is a parent thread
        is_parent = True
        if tags:
            relevant_info = context_from_tags(tags)
        else:
            # create context using similar vectors
            if query_type == 'Class Info':
                embedded_message = embed_message(user_message) # embed message
                similar_vectors = fetch_similar_vectors(embedded_message, 'courses') # fetch similar vectors
                relevant_info = create_context(similar_vectors)
            elif query_type == 'Registration':
                embedded_message = embed_message(user_message) # embed message
                similar_vectors = fetch_similar_vectors(embedded_message, 'registration-vdb') # fetch similar vectors
                relevant_info = create_context_reg(similar_vectors)
            else:
                raise TypeError('Invalid db_name')

    return response_thread_id, relevant_info, is_parent

def fetch_other(data, thread_id, cached_thread):
    """
    Logic for handling other types of queries.
    Input: data, thread_id
    Output: response_thread_id, relevant_info, is_parent
    """
    conversation_history = data.get('conversation_history')

    relevant_info = []
    # if we are in a thread
    if cached_thread:
        # response inherits thread_id
        response_thread_id = thread_id
        # response is not parent
        is_parent = False
        # for message in cached thread
        for message in cached_thread:
            if message['fromUser'] == True:
                sender = 'User'
                msg_text = message['message']
                msg_str = f"{sender}: {msg_text}\n"
            else:
                sender = 'Duke Atlas Chatbot'
                context = message['context']
                msg_text = message['message']
                msg_str = f"Context: {context}\n{sender}: {msg_text}\n"

            relevant_info.append(msg_str)
        relevant_info.append('Duke Atlas Chatbot:')
     # else if we are not in a thread
    else:
        # generate new thread ID
        response_thread_id = str(uuid.uuid4())
        # response is a parent thread
        is_parent = True

    return response_thread_id, relevant_info, is_parent
