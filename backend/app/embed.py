# embed.py
# Contains the logic for embedding the user_message using BERT.
from transformers import BertModel, BertTokenizer
import torch
from sentence_transformers import SentenceTransformer

def embed_message(user_message):
    """
    embeds the user_message using BERT.
    
    :param user_message: The user message to embed. Type string.
    :return: The embedded message. Type list.
    """
    model = SentenceTransformer("avsolatorio/GIST-large-Embedding-v0")
    query_embedding = model.encode([user_message], convert_to_tensor=True).tolist()[0]
    return query_embedding