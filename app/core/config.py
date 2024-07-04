import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


class Settings:
    # MongoDB
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DB_NAME}?retryWrites=true&w=majority"

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")

    # Supabase
    DATABASE_URL = os.getenv("DATABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET")

    # Prompts
    SYSTEM_PROMPT_VERSION = os.getenv("SYSTEM_PROMPT_VERSION")
    TOOL_VERSION = os.getenv("TOOL_VERSION")


settings = Settings()
