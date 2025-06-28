"""
Check current users in database
"""
import asyncio
import os
from dotenv import load_dotenv
from database.config import init_database
from database.models import User

# Load environment variables
load_dotenv()

async def check_users():
    await init_database()
    users = await User.find_all().to_list()
    print("Current users in database:")
    for user in users:
        print(f"- ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print()

if __name__ == "__main__":
    asyncio.run(check_users())
