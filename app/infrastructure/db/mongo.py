from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = None
        self.uri = uri
        self.db_name = db_name
        self.database = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self.uri)
        self.database = self.client[self.db_name]

    async def close(self):
        self.client.close()


# Create a global MongoDB instance
mongo_db = MongoDB(settings.MONGO_URI, settings.MONGO_DB_NAME)


# Dependency to get the database instance
async def get_mongo_db():
    return mongo_db.database


# Ensure the client is closed on shutdown
async def close_mongo_db():
    await mongo_db.close()
