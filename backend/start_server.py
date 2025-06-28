#!/usr/bin/env python3
"""
Simple server startup script for the SceneSplit API.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[".", "agents", "auth", "database", "graph", "models", "routes", "services"]
    )
