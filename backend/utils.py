from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    provider = GoogleGLAProvider(api_key=api_key)
    # Create GeminiModel with the provider - fix: add model_name
    model_name = "gemini-2.0-flash"  # or "gemini-1.5-pro"
    return GeminiModel(model_name, provider=provider)