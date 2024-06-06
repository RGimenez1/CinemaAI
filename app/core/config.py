
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_CLUSTER_URL = os.getenv('MONGO_CLUSTER_URL')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
    MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DB_NAME}?retryWrites=true&w=majority"

settings = Settings()
