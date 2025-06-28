from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
import uuid
import json
import traceback
import tempfile
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database imports
from database.config import init_database, close_database
from database.models import User, Project
from database.services import ProjectService, UserService
from auth.auth import create_demo_users

# Route imports
from routes.auth import router as auth_router, get_current_user
from routes.projects import router as projects_router

# Langchain imports for AI chat
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage
    GEMINI_AVAILABLE = True
except ImportError:
    print("Warning: Langchain dependencies not found. AI chat will use fallback responses.")
    GEMINI_AVAILABLE = False

from graph.workflow import run_analyze_script_workflow, resume_workflow, get_workflow_state
from graph.workflow import run_analyze_script_workflow_from_file
from services.data_transformer import DataTransformer
from models.models import EnhancedScriptAnalysisResponse

# Constants
ALLOWED_FILE_TYPES = ['.pdf', '.txt', '.fountain']
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]
API_VERSION = "2.0.0"
MIN_CONTENT_LENGTH = 10

# Initialize Gemini AI if available
gemini_llm = None
chat_chain = None
chat_store = {}

if GEMINI_AVAILABLE:
    api_key = os.getenv("GEMINI_API_KEY")  
    # Check for valid API key (not placeholder or test keys)  
    if api_key and not api_key.startswith('your_actual'):
        try:
            print(f"🔑 Initializing Gemini AI with API key: {api_key[:10]}...")
            
            gemini_llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.0,  # Low temperature for consistent responses
                api_key=api_key
            )
            
            # Create chat prompt template with custom instructions
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful assistant. Answer all questions to the best of your ability.

Special instructions:
- Be helpful, conversational, and friendly in all responses."""),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
            
            chat_chain = chat_prompt | gemini_llm
            
            def get_message_history(session_id: str):
                if session_id not in chat_store:
                    chat_store[session_id] = InMemoryChatMessageHistory()
                return chat_store[session_id]
            
            chat_chain = RunnableWithMessageHistory(
                chat_chain,
                get_message_history,
                input_messages_key="input",
                history_messages_key="history"
            )
            
            print("✅ Gemini AI chat initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini AI: {str(e)}")
            gemini_llm = None
            chat_chain = None
    else:
        print("⚠️ Gemini API key not found or not set properly")
        print("💡 Please set GEMINI_API_KEY in your .env file")
else:
    print("⚠️ Gemini AI dependencies not available - using fallback responses")

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await init_database()
        # Create demo users
        await create_demo_users()
        print("🚀 Application started successfully")
    except Exception as e:
        print(f"❌ Failed to initialize application: {str(e)}")
    
    yield
    
    # Shutdown
    try:
        await close_database()
        print("👋 Application shutdown complete")
    except Exception as e:
        print(f"❌ Error during shutdown: {str(e)}")

# Initialize FastAPI app
app = FastAPI(
    title="SceneSplit AI - Film Production Management API", 
    version=API_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Health check and CORS test endpoints
@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "message": "SceneSplit AI API is running",
        "version": API_VERSION,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": API_VERSION,
        "timestamp": datetime.now().isoformat()
    }

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle preflight OPTIONS requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Include routers
app.include_router(auth_router)
app.include_router(projects_router)

# Request Models
class ScriptRequest(BaseModel):
    script_content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[list] = []

class FeedbackRequest(BaseModel):
    thread_id: str
    feedback: Dict[str, str]
    needs_revision: Dict[str, bool]

# Initialize data transformer
transformer = DataTransformer()

# Response Helpers
def create_success_response(data: dict, message: str = "Success") -> JSONResponse:
    """Create standardized success JSON response with datetime handling"""
    try:
        serializable_data = json.loads(json.dumps(data, default=str))
        return JSONResponse(
            content=serializable_data,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"⚠️ JSON serialization error: {e}")
        return JSONResponse(
            content=_convert_datetime_to_string(data),
            headers={"Content-Type": "application/json"}
        )

def create_error_response(message: str, status_code: int = 500, details: str = None) -> JSONResponse:
    """Create standardized error JSON response"""
    response_data = {
        "meta": {
            "success": False,
            "version": API_VERSION,
            "timestamp": datetime.now().isoformat()
        },
        "error": {
            "message": message,
            "details": details
        }
    }
    
    return JSONResponse(
        content=response_data,
        status_code=status_code,
        headers={"Content-Type": "application/json"}
    )

def _convert_datetime_to_string(obj):
    """Recursively convert datetime objects to ISO format strings"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: _convert_datetime_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_convert_datetime_to_string(item) for item in obj]
    elif hasattr(obj, 'model_dump'):
        return _convert_datetime_to_string(obj.model_dump())
    elif hasattr(obj, 'dict'):
        return _convert_datetime_to_string(obj.dict())
    elif hasattr(obj, '__dict__'):
        return _convert_datetime_to_string(obj.__dict__)
    else:
        return obj

# File Processing Helpers
def _validate_file_type(filename: str) -> bool:
    """Validate uploaded file type"""
    if not filename:
        return False
    
    file_suffix = Path(filename).suffix.lower()
    return file_suffix in ALLOWED_FILE_TYPES

async def _process_uploaded_file(file: UploadFile) -> str:
    """Process uploaded file and return temporary file path"""
    if not _validate_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"
        )
    
    file_suffix = Path(file.filename).suffix.lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
        content = await file.read()
        temp_file.write(content)
        return temp_file.name

def _cleanup_temp_file(file_path: str):
    """Clean up temporary file safely"""
    try:
        os.unlink(file_path)
    except OSError:
        pass  # File might already be deleted

def _generate_thread_id() -> str:
    """Generate unique thread ID"""
    return f"script_{uuid.uuid4().hex[:8]}"

def _validate_script_content(content: str):
    """Validate script content"""
    if not content or len(content.strip()) < MIN_CONTENT_LENGTH:
        raise ValueError("Script content is too short or empty")

# API Endpoints
@app.post("/analyze-script-file")
async def analyze_script_file(file: UploadFile = File(...)):
    """Analyze script from uploaded PDF or text file"""
    temp_file_path = None
    
    try:
        temp_file_path = await _process_uploaded_file(file)
        thread_id = _generate_thread_id()
        
        print(f"🚀 Starting analysis for uploaded file: {file.filename}")
        
        result = await run_analyze_script_workflow_from_file(
            temp_file_path, 
            thread_id=thread_id
        )
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            result, 
            thread_id, 
            file.filename
        )
        
        return create_success_response(
            enhanced_response.model_dump(),
            f"Analysis completed for {file.filename}"
        )
        
    except ValueError as e:
        return create_error_response(str(e), status_code=400)
    except Exception as e:
        print(f"❌ File analysis failed: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("File analysis failed", details=str(e))
    finally:
        if temp_file_path:
            _cleanup_temp_file(temp_file_path)

@app.post("/analyze-script")
async def analyze_script(request: ScriptRequest):
    """Initial script analysis from text content"""
    try:
        _validate_script_content(request.script_content)
        
        thread_id = _generate_thread_id()
        print(f"🚀 Starting analysis for thread: {thread_id}")
        
        result = await run_analyze_script_workflow(
            request.script_content, 
            thread_id=thread_id
        )
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            result,
            thread_id
        )
        
        return create_success_response(
            enhanced_response.model_dump(),
            "Initial analysis completed"
        )
        
    except ValueError as e:
        return create_error_response(str(e), status_code=400)
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Analysis failed", details=str(e))

@app.post("/submit-feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit human feedback and trigger revisions"""
    try:
        print(f"📝 Processing feedback for thread: {request.thread_id}")
        
        revisions_requested = [k for k, v in request.needs_revision.items() if v]
        print(f"Revisions requested: {revisions_requested}")
        
        if not any(request.needs_revision.values()):
            return await _handle_no_revisions_needed(request.thread_id)
        
        return await _handle_revisions_needed(request)
        
    except ValueError as e:
        return create_error_response(str(e), status_code=404)
    except Exception as e:
        print(f"❌ Feedback processing failed: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Feedback processing failed", details=str(e))

async def _handle_no_revisions_needed(thread_id: str):
    """Handle case where no revisions are needed"""
    current_state = await get_workflow_state(thread_id)
    if current_state:
        current_state.human_review_complete = True
        current_state.task_complete = True
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            current_state, 
            thread_id
        )
        
        return create_success_response(
            enhanced_response.model_dump(),
            "All analyses approved. Analysis complete!"
        )
    else:
        raise ValueError("Workflow not found")

async def _handle_revisions_needed(request: FeedbackRequest):
    """Handle case where revisions are needed"""
    human_feedback = {
        "feedback": request.feedback,
        "needs_revision": request.needs_revision
    }
    
    result = await resume_workflow(request.thread_id, human_feedback)
    
    enhanced_response = transformer.transform_to_enhanced_structure(
        result, 
        request.thread_id
    )
    
    message = ("Revisions processed. Please review the updated results." 
              if not result.task_complete else "All revisions complete!")
    
    return create_success_response(
        enhanced_response.model_dump(),
        message
    )

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """Chat endpoint for AI assistant interactions"""
    try:
        message = request.message.strip()
        if not message:
            return create_error_response("Message cannot be empty", status_code=400)
        
        # Simple AI chat responses - you can integrate with a real AI service here
        # For now, providing contextual responses based on keywords
        response = await _generate_ai_response(message, request.history)
        
        return create_success_response({
            "response": response["message"],
            "actions": response.get("actions", []),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Chat failed: {str(e)}")
        return create_error_response("Failed to process chat message", details=str(e))

async def _generate_ai_response(message: str, history: list) -> dict:
    """Generate AI response using Gemini or fallback responses"""
    
    # Check for creator question first (works even without Gemini)
    message_lower = message.lower()
    creator_keywords = ['creator', 'who made you', 'who created you', 'your creator', 'who built you', 'developer']
    if any(keyword in message_lower for keyword in creator_keywords):
        return {
            "message": "Made by Team 4: Cohort 3 | Gamuda AI Academy. Powered by Gemini",
            "actions": []
        }
    
    # Always try to use Gemini AI first for any message
    if chat_chain and gemini_llm:
        try:
            # Use a simple session ID for now - you could make this user-specific
            session_id = "default"
            
            print(f"🤖 Using Gemini AI for message: {message}")
            
            response = chat_chain.invoke(
                {"input": message},
                {"configurable": {"session_id": session_id}}
            )
            
            print(f"✅ Gemini response: {response.content[:100]}...")
            
            # Simple response format - just return the content
            return {
                "message": response.content,
                "actions": []  # Keep actions minimal for general chat
            }
            
        except Exception as e:
            print(f"⚠️ Gemini AI error: {str(e)}")
            print("📋 Falling back to template responses")
            # Fall back to rule-based responses only on error
    else:
        print("⚠️ Gemini AI not available - using fallback responses")
    
    # Fallback to rule-based responses only when Gemini fails
    return _generate_fallback_response(message)

def _extract_suggested_actions(user_message: str, ai_response: str) -> list:
    """Extract suggested actions based on the conversation context"""
    actions = []
    user_lower = user_message.lower()
    response_lower = ai_response.lower()
    
    # Script-related actions
    if any(keyword in user_lower or keyword in response_lower for keyword in ['script', 'analyze', 'breakdown']):
        actions.append({"label": "Upload Script", "action": "upload-script"})
    
    # Budget-related actions
    if any(keyword in user_lower or keyword in response_lower for keyword in ['budget', 'cost', 'estimate']):
        actions.append({"label": "Create Budget", "action": "create-budget"})
    
    # Schedule-related actions
    if any(keyword in user_lower or keyword in response_lower for keyword in ['schedule', 'timeline', 'production']):
        actions.append({"label": "Plan Schedule", "action": "plan-schedule"})
    
    return actions

def _generate_fallback_response(message: str) -> dict:
    """Generate fallback response when Gemini is not available"""
    message_lower = message.lower()
    
    # Script analysis keywords
    if any(keyword in message_lower for keyword in ['script', 'analyze', 'breakdown', 'scenes', 'characters']):
        return {
            "message": "I can help you analyze scripts! Upload a script file and I'll break it down into scenes, characters, locations, and props. You can also ask me specific questions about script structure, formatting, or analysis techniques.",
            "actions": [
                {"label": "Upload Script", "action": "upload-script"},
                {"label": "Learn About Analysis", "action": "learn-analysis"}
            ]
        }
    
    # Budget keywords
    elif any(keyword in message_lower for keyword in ['budget', 'cost', 'money', 'estimate', 'pricing']):
        return {
            "message": "I can help you create detailed budgets for your film projects! I'll estimate costs for cast, crew, equipment, locations, and post-production based on your script analysis. Would you like me to generate a budget estimate?",
            "actions": [
                {"label": "Generate Budget", "action": "generate-budget"},
                {"label": "Budget Tips", "action": "budget-tips"}
            ]
        }
    
    # Scheduling keywords
    elif any(keyword in message_lower for keyword in ['schedule', 'timeline', 'shooting', 'production', 'calendar']):
        return {
            "message": "I can help you create production schedules! Based on your script breakdown, I'll suggest optimal shooting schedules, considering location logistics, cast availability, and efficient resource usage.",
            "actions": [
                {"label": "Create Schedule", "action": "create-schedule"},
                {"label": "Scheduling Tips", "action": "scheduling-tips"}
            ]
        }
    
    # Location keywords
    elif any(keyword in message_lower for keyword in ['location', 'filming', 'where', 'shoot', 'venue']):
        return {
            "message": "I can help you identify and plan locations for your project! I'll analyze your script to extract all location requirements and provide suggestions for scouting, permits, and logistics.",
            "actions": [
                {"label": "Analyze Locations", "action": "analyze-locations"},
                {"label": "Location Tips", "action": "location-tips"}
            ]
        }
    
    # Cast and crew keywords
    elif any(keyword in message_lower for keyword in ['cast', 'actor', 'crew', 'character', 'role']):
        return {
            "message": "I can help you with casting and crew planning! I'll analyze character requirements from your script and suggest crew roles needed for production.",
            "actions": [
                {"label": "Character Analysis", "action": "character-analysis"},
                {"label": "Crew Planning", "action": "crew-planning"}
            ]
        }
    
    # General help or greeting
    elif any(keyword in message_lower for keyword in ['hello', 'hi', 'help', 'what', 'how']):
        return {
            "message": "Hello! I'm your AI assistant ready to help with anything you need. I specialize in film production but can assist with general questions too. I can help you with:\n\n• Script analysis and breakdown\n• Budget estimation and planning\n• Production scheduling\n• Location and casting analysis\n• General questions and conversations\n\nWhat would you like to work on today?",
            "actions": [
                {"label": "Analyze Script", "action": "analyze-script"},
                {"label": "Create Budget", "action": "create-budget"},
                {"label": "Plan Schedule", "action": "plan-schedule"}
            ]
        }
    
    # Default response for general questions
    else:
        return {
            "message": f"I understand you're asking about: \"{message}\"\n\nI'm here to help! While I specialize in film production assistance, I can try to help with general questions too. For the best experience with film projects, I can analyze scripts, create budgets, plan schedules, and manage all aspects of production.\n\nCould you tell me more about what you'd like help with?",
            "actions": [
                {"label": "Script Help", "action": "script-help"},
                {"label": "Budget Help", "action": "budget-help"},
                {"label": "General Chat", "action": "general-chat"}
            ]
        }

@app.get("/workflow-status/{thread_id}")
async def get_workflow_status(thread_id: str):
    """Get current workflow status"""
    try:
        state = await get_workflow_state(thread_id)
        if not state:
            return create_error_response("Workflow not found", status_code=404)
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            state, 
            thread_id
        )
        
        return create_success_response(
            enhanced_response.model_dump(),
            "Status retrieved successfully"
        )
        
    except Exception as e:
        print(f"❌ Status check failed: {str(e)}")
        return create_error_response("Failed to get workflow status", details=str(e))

@app.get("/scenes/{thread_id}/{scene_id}")
async def get_scene_data(thread_id: str, scene_id: int):
    """Get specific scene data"""
    try:
        state = await get_workflow_state(thread_id)
        if not state:
            return create_error_response("Workflow not found", status_code=404)
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            state, 
            thread_id
        )
        
        scene_data = _find_scene_by_id(enhanced_response.script_breakdown.scenes, scene_id)
        if not scene_data:
            return create_error_response(f"Scene {scene_id} not found", status_code=404)
        
        return create_success_response(
            scene_data.model_dump(),
            f"Scene {scene_id} data retrieved"
        )
        
    except Exception as e:
        print(f"❌ Scene data retrieval failed: {str(e)}")
        return create_error_response("Failed to get scene data", details=str(e))

def _find_scene_by_id(scenes, scene_id: int):
    """Find scene by ID"""
    for scene in scenes:
        if scene.id == scene_id:
            return scene
    return None

@app.get("/departments/{thread_id}/{department}")
async def get_department_data(thread_id: str, department: str):
    """Get department-specific data"""
    try:
        state = await get_workflow_state(thread_id)
        if not state:
            return create_error_response("Workflow not found", status_code=404)
        
        enhanced_response = transformer.transform_to_enhanced_structure(
            state, 
            thread_id
        )
        
        department_data = _extract_department_data(enhanced_response, department)
        if department_data is None:
            return create_error_response(f"Unknown department: {department}", status_code=400)
        
        return create_success_response(
            department_data,
            f"{department.title()} data retrieved"
        )
        
    except Exception as e:
        print(f"❌ Department data retrieval failed: {str(e)}")
        return create_error_response("Failed to get department data", details=str(e))

def _extract_department_data(enhanced_response, department: str) -> Optional[dict]:
    """Extract department-specific data"""
    department_mapping = {
        "props": lambda r: r.script_breakdown.props_and_wardrobe.model_dump(),
        "locations": lambda r: r.script_breakdown.locations.model_dump(),
        "casting": lambda r: r.script_breakdown.characters.model_dump(),
        "budget": lambda r: r.production_planning.budget.model_dump(),
        "schedule": lambda r: r.production_planning.schedule.model_dump()
    }
    
    extractor = department_mapping.get(department)
    return extractor(enhanced_response) if extractor else None

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler to ensure JSON responses"""
    print(f"❌ Unhandled exception: {str(exc)}")
    print(f"Full traceback: {traceback.format_exc()}")
    
    return create_error_response(
        "Internal server error",
        status_code=500,
        details=str(exc)
    )

@app.post("/create-project-with-script")
async def create_project_with_script(
    title: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Create a new project with script analysis and save to database"""
    temp_file_path = None
    
    try:
        # Validate file
        temp_file_path = await _process_uploaded_file(file)
        thread_id = _generate_thread_id()
        
        print(f"🚀 Creating project '{title}' for user {current_user.username}")
        
        # Run script analysis
        result = await run_analyze_script_workflow_from_file(
            temp_file_path, 
            thread_id=thread_id
        )
        
        # Transform to enhanced structure
        print("🔄 Transforming analysis result to enhanced structure...")
        enhanced_response = transformer.transform_to_enhanced_structure(
            result, 
            thread_id, 
            file.filename
        )
        print("✅ Enhanced structure transformation completed")
        
        # Create project in database
        print("🔄 Extracting estimated days...")
        try:
            estimated_days = enhanced_response.script_breakdown.summary.estimated_shoot_days
            print(f"✅ Estimated days extracted: {estimated_days}")
        except AttributeError as e:
            estimated_days = 10  # Default value
            print(f"⚠️ Using default estimated days: {estimated_days}, error: {e}")
        
        print("🔄 Calculating budget...")
        try:
            budget_total = _calculate_total_budget(enhanced_response)
            print(f"✅ Budget calculated: {budget_total}")
        except Exception as e:
            budget_total = 50000.0
            print(f"⚠️ Using default budget: {budget_total}, error: {e}")
        
        print("🔄 Serializing analysis data...")
        try:
            analysis_data = enhanced_response.model_dump()
            print(f"✅ Analysis data serialized, size: {len(str(analysis_data))} chars")
        except Exception as e:
            print(f"❌ Failed to serialize analysis data: {e}")
            raise ValueError(f"Failed to serialize analysis data: {e}")
            
        print("🔄 Creating project in database...")
        try:
            project = await ProjectService.create_project(
                title=title,
                description=description,
                owner_id=str(current_user.id),  # Convert ObjectId to string
                script_filename=file.filename,
                analysis_data=analysis_data,
                budget_total=budget_total,
                estimated_duration_days=estimated_days
            )
            print(f"✅ Project created in database with ID: {project.id}")
        except Exception as db_error:
            print(f"❌ Database creation failed: {str(db_error)}")
            print(f"❌ Database error traceback: {traceback.format_exc()}")
            raise ValueError(f"Database creation failed: {str(db_error)}")
        
        print("🔄 Preparing response data...")
        response_data = {
            "project_id": str(project.id),
            "title": project.title,
            "analysis": analysis_data,
            "message": f"Project '{title}' created successfully with script analysis"
        }
        print(f"✅ Response data prepared, project_id: {response_data['project_id']}")
        
        print("🔄 Creating success response...")
        return create_success_response(response_data)
        
    except ValueError as e:
        return create_error_response(str(e), status_code=400)
    except Exception as e:
        print(f"❌ Project creation failed: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Project creation failed", details=str(e))
    finally:
        if temp_file_path:
            _cleanup_temp_file(temp_file_path)

def _calculate_total_budget(analysis_response) -> float:
    """Calculate total budget from analysis response"""
    try:
        budget_data = analysis_response.production_planning.budget
        # Simple calculation based on budget categories
        total = 0.0
        
        # Calculate based on scene budget categories
        for scene_budget in budget_data.scene_breakdown:
            # Use enum values instead of strings
            if scene_budget.category.value == "low":
                total += 5000
            elif scene_budget.category.value == "medium":
                total += 15000
            elif scene_budget.category.value == "high":
                total += 30000
            elif scene_budget.category.value == "premium":
                total += 50000
            else:
                # Default to medium if unknown category
                total += 15000
        
        # If no scene breakdown, estimate based on overall category
        if total == 0.0:
            overall_category = budget_data.overall_category.value
            if overall_category == "low":
                total = 25000
            elif overall_category == "medium":
                total = 75000
            elif overall_category == "high":
                total = 150000
            elif overall_category == "premium":
                total = 250000
            else:
                total = 75000  # Default
        
        return total
    except Exception as e:
        print(f"⚠️ Budget calculation failed: {e}")
        print(f"⚠️ Budget calculation error details: {traceback.format_exc()}")
        return 50000.0  # Return a reasonable default

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
