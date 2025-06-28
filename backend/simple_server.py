"""
Simplified server for testing without MongoDB dependency
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
from datetime import datetime, timedelta
import uuid

app = FastAPI(title="SceneSplit AI - Simple Test Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# In-memory storage
users_db = {
    "admin@scenesplit.com": {
        "id": "1",
        "email": "admin@scenesplit.com",
        "username": "admin",
        "full_name": "Admin User",
        "password": "password123",  # In real app, this would be hashed
        "role": "ADMIN",
        "is_active": True,
        "is_verified": True,
        "created_at": datetime.now().isoformat()
    },
    "director@scenesplit.com": {
        "id": "2", 
        "email": "director@scenesplit.com",
        "username": "director",
        "full_name": "John Director",
        "password": "director123",
        "role": "USER",
        "is_active": True,
        "is_verified": True,
        "created_at": datetime.now().isoformat()
    }
}

projects_db = []
tokens_db = {}

# Models
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict

# Helper functions
def create_access_token(user_id: str, email: str) -> str:
    token = f"token_{uuid.uuid4().hex}"
    tokens_db[token] = {
        "user_id": user_id,
        "email": email,
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    return token

def verify_token(token: str) -> Optional[dict]:
    token_data = tokens_db.get(token)
    if not token_data:
        return None
    
    if datetime.now() > token_data["expires_at"]:
        del tokens_db[token]
        return None
    
    return token_data

# Routes
@app.get("/")
async def root():
    return {"message": "SceneSplit AI Simple Test Server", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = users_db.get(request.email)
    
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token = create_access_token(user["id"], user["email"])
    
    # Remove password from user data
    safe_user = {k: v for k, v in user.items() if k != "password"}
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=24 * 60 * 60,  # 24 hours
        user=safe_user
    )

@app.get("/projects/")
async def get_projects():
    return {"projects": projects_db}

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
