"""
MongoDB Database Configuration for SceneSplit AI
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from database.models import User, Project, Scene, Character, Location, Props, Budget, ProjectCollaborator, Comment, FileUpload

# Database connection
client = None
database = None

async def init_database():
    """Initialize MongoDB connection and Beanie ODM"""
    global client, database
    
    try:
        # Get MongoDB URL from environment
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("MONGODB_DATABASE", "scenesplit_ai")
        
        print(f"🔗 Connecting to MongoDB: {mongodb_url}")
        
        # Create client
        client = AsyncIOMotorClient(mongodb_url)
        database = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Initialize Beanie with models
        await init_beanie(
            database=database,
            document_models=[
                User, Project, Scene, Character, Location, 
                Props, Budget, ProjectCollaborator, Comment, FileUpload
            ]
        )
        
        print("✅ Beanie ODM initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        raise

async def close_database():
    """Close database connection"""
    global client
    
    if client:
        client.close()
        print("👋 Database connection closed")

async def get_database():
    """Get database instance"""
    global database
    return database
