"""
Reset and reinitialize database with correct user structure
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from database.config import init_database, close_database
from auth.auth import create_demo_users

load_dotenv()

async def reset_database():
    """Reset and reinitialize the database"""
    try:
        # Get MongoDB URL from environment
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("MONGODB_DATABASE", "scenesplit_ai")
        
        print(f"🔗 Connecting to MongoDB: {mongodb_url}")
        
        # Create client
        client = AsyncIOMotorClient(mongodb_url)
        database = client[database_name]
        
        # Drop the users collection to clear any malformed data
        print("🗑️ Dropping users collection...")
        await database.users.drop()
        
        # Close the direct connection
        client.close()
        
        # Initialize database with Beanie
        print("🔄 Reinitializing database...")
        await init_database()
        
        # Create demo users
        print("👥 Creating demo users...")
        await create_demo_users()
        
        print("✅ Database reset and reinitialized successfully!")
        
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        raise
    finally:
        await close_database()

if __name__ == "__main__":
    asyncio.run(reset_database())
