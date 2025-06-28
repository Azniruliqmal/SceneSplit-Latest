"""
Database Models for SceneSplit AI using Beanie ODM
"""
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    PRODUCER = "producer"
    DIRECTOR = "director"
    USER = "user"
    GUEST = "guest"
    DEMO = "demo"

class ProjectStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class SceneType(str, Enum):
    INTERIOR = "interior"
    EXTERIOR = "exterior"
    INSERT = "insert"
    MONTAGE = "montage"

class TimeOfDay(str, Enum):
    DAY = "day"
    NIGHT = "night"
    DAWN = "dawn"
    DUSK = "dusk"
    CONTINUOUS = "continuous"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base Models
class BaseDocument(Document):
    """Base document with common fields"""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        use_state_management = True

# User Model
class User(BaseDocument):
    """User document model"""
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False
    profile_picture: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    class Settings:
        name = "users"

# Project Model
class Project(BaseDocument):
    """Project document model"""
    title: str
    description: Optional[str] = None
    owner_id: str
    status: ProjectStatus = ProjectStatus.DRAFT
    script_content: Optional[str] = None
    script_filename: Optional[str] = None
    analysis_data: Dict[str, Any] = Field(default_factory=dict)
    collaborators: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    budget_total: Optional[float] = None
    estimated_duration_days: Optional[int] = None
    
    class Settings:
        name = "projects"

# Scene Model
class Scene(BaseDocument):
    """Scene document model"""
    project_id: str
    scene_number: int
    title: str
    description: Optional[str] = None
    scene_type: SceneType
    location: str
    time_of_day: TimeOfDay
    characters: List[str] = Field(default_factory=list)
    props: List[str] = Field(default_factory=list)
    estimated_duration_minutes: Optional[int] = None
    priority: Priority = Priority.MEDIUM
    notes: Optional[str] = None
    
    class Settings:
        name = "scenes"

# Character Model
class Character(BaseDocument):
    """Character document model"""
    project_id: str
    name: str
    description: Optional[str] = None
    role_type: str  # "lead", "supporting", "background"
    age_range: Optional[str] = None
    gender: Optional[str] = None
    appearance_notes: Optional[str] = None
    personality_notes: Optional[str] = None
    scene_count: int = 0
    dialogue_count: int = 0
    
    class Settings:
        name = "characters"

# Location Model
class Location(BaseDocument):
    """Location document model"""
    project_id: str
    name: str
    location_type: SceneType
    description: Optional[str] = None
    address: Optional[str] = None
    contact_info: Optional[str] = None
    availability: Optional[str] = None
    cost_per_day: Optional[float] = None
    requirements: List[str] = Field(default_factory=list)
    scene_count: int = 0
    
    class Settings:
        name = "locations"

# Props Model
class Props(BaseDocument):
    """Props document model"""
    project_id: str
    name: str
    category: str  # "props", "wardrobe", "makeup", "special_effects"
    description: Optional[str] = None
    quantity_needed: int = 1
    estimated_cost: Optional[float] = None
    source: Optional[str] = None  # "purchase", "rent", "make", "owned"
    priority: Priority = Priority.MEDIUM
    scenes: List[str] = Field(default_factory=list)
    
    class Settings:
        name = "props"

# Budget Model
class Budget(BaseDocument):
    """Budget document model"""
    project_id: str
    category: str
    item_name: str
    description: Optional[str] = None
    estimated_cost: float
    actual_cost: Optional[float] = None
    quantity: int = 1
    unit: str = "each"
    vendor: Optional[str] = None
    notes: Optional[str] = None
    approved: bool = False
    
    class Settings:
        name = "budgets"

# Project Collaborator Model
class ProjectCollaborator(BaseDocument):
    """Project collaborator document model"""
    project_id: str
    user_id: str
    role: str  # "director", "producer", "writer", "editor", etc.
    permissions: List[str] = Field(default_factory=list)
    invited_by: str
    invitation_accepted: bool = False
    invitation_date: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "project_collaborators"

# Comment Model
class Comment(BaseDocument):
    """Comment document model"""
    project_id: str
    user_id: str
    content: str
    target_type: str  # "project", "scene", "character", "location"
    target_id: str
    parent_comment_id: Optional[str] = None
    edited: bool = False
    
    class Settings:
        name = "comments"

# File Upload Model
class FileUpload(BaseDocument):
    """File upload document model"""
    project_id: Optional[str] = None
    user_id: str
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    file_path: str
    upload_purpose: str  # "script", "reference", "asset", etc.
    processed: bool = False
    processing_status: Optional[str] = None
    
    class Settings:
        name = "file_uploads"
