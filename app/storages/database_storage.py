from typing import Optional
import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession, AsyncIOMotorDatabase
from app.core.config import settings


Client = AsyncIOMotorClient
Session = AsyncIOMotorClientSession
Database = AsyncIOMotorDatabase


db_client: AsyncIOMotorClient = None
ca = certifi.where()


async def get_db_client() -> Client:
    """Return database client instance."""
    return db_client


async def get_db_session() -> Optional[Session]:
    """Return database session instance."""
    if db_client is None:
        await connect_db()
    return db_client.start_session()


async def connect_db():
    """Create database connection."""
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGO_URL, tlsCAFile=ca)


async def close_db():
    """Close database connection."""
    if db_client:
        await db_client.close()


async def get_db() -> Database:
    """Return database instance."""
    if db_client is None:
        await connect_db()
    return db_client[settings.DEFAULT_DATABASE]
