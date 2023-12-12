import pytest
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.embed import embed_message

def load_test_vector():
    # Get the directory of the current file
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the test vector file
    file_path = os.path.join(dir_path, 'test_vector.json')

    # Load and return the vector
    with open(file_path, 'r') as file:
        return json.load(file)

def test_embed_message():
    # Test input
    user_message = "classes that teach about machine learning"

    # Call the function
    embedded_message = embed_message(user_message)

    # Ensure the embedded_message is a list
    assert isinstance(embedded_message, list)

    # Ensure the length of the embedded_message is 768
    assert len(embedded_message) == 768

    # Load the test vector
    test_vector = load_test_vector()

    # Check if the embedded message matches the expected output
    assert embedded_message == pytest.approx(test_vector)
