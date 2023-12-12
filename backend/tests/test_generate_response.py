import pytest
import sqlite3
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.generate_response import generate_openai_response

def test_create_context():
    """
    Tests the generate_openai_response function.

    :return: None
    """
    course_id = 27041

    with sqlite3.connect('../data/coursesDB.db') as conn:
        cursor = conn.cursor()
        sql = """
                SELECT
                    Descr,
                    `Course Long Descr`,
                    `Mtg Start`,
                    `Mtg End`,
                    Pat,
                    `Term Descr`
                FROM
                    courses
                WHERE
                    `Course ID` = ?
              """
        cursor.execute(sql, (course_id,))

        result = cursor.fetchone()
        assert result is not None
        result_dict = {
            'name': result[0],
            'descr': result[1],
            'start': result[2],
            'end': result[3],
            'days': result[4],
            'term': result[5]
        }

        assert result_dict is not None


def test_generate_openai_response():
    # Define your test input
    user_message = "Courses that teach machine learning"
    courses_info = "Course name: Machine Learning, Description: introduction to the modeling process " \
                    "and best practices in model creation, interpretation, validation, and selection of models for different uses."

    # Call the function with the test input
    response = generate_openai_response(user_message, courses_info)

    # Assert that the response is as expected
    assert response is not None
