# embed.py
# Contains the logic for embedding the user_message using BERT.
from transformers import BertModel, BertTokenizer
import torch

def embed_message(user_message):
    """
    embeds the user_message using BERT.
    
    :param user_message: The user message to embed. Type string.
    :return: The embedded message. Type list.
    """
    # Load the pre-trained BERT model and tokenizer
    model = BertModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Tokenize the user_message
    tokenized_message = tokenizer(user_message, return_tensors='pt')

    # Feed the tokenized message to the model
    # Get the embeddings
    with torch.no_grad():
        outputs = model(**tokenized_message)

    # Extract the embeddings from the model output, use mean pooling to get a single vector
    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()

    # Convert the embeddings from a torch tensor to a list
    embeddings_list = embeddings.tolist()[0]

    # Return the embeddings list
    return embeddings_list