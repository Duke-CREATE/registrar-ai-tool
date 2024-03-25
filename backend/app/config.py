import os
from dotenv import load_dotenv

class Config:
    DEBUG = False

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the path to the .env file
    env_path = os.path.join(current_directory, '..', '.env')
    # Load the environment variables from the .env file
    load_dotenv(dotenv_path=env_path)

    # Sensitive configs
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')
    
    # Non-sensitive default configs
    COURSES_DB = 'courses'
    COURSES_INFO_COLLECTION = 'fa23-sp24-info'
    COURSES_EMB_COLLECTION = 'fa23-sp24-embeddings'
    COURSES_EMB_INDEX = 'course_embeddings'
    REGISTRATION_DB = 'registration-vdb'
    REGISTRATION_COLLECTION = 'embeddings'
    REGISTRATION_INDEX = 'vector_index'
    USER_DATA_DB = 'user_data'
    USER_DATA_COLLECTION = 'messages'

    # Cache configuration
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = 300  # Default cache timeout (in seconds)

class DevelopmentConfig(Config):
    DEBUG = True
    # Other development-specific configs