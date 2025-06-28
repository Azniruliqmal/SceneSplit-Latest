"""
Database Services for SceneSplit AI
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import traceback
from bson import ObjectId
from database.models import (
    User, Project, Scene, Character, Location, Props, Budget,
    ProjectCollaborator, Comment, FileUpload, UserRole, ProjectStatus
)
from beanie.operators import In
import uuid

# User Services
class UserService:
    @staticmethod
    async def create_user(email: str, username: str, hashed_password: str, **kwargs) -> User:
        """Create a new user"""
        user_data = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            **kwargs
        }
        user = User(**user_data)
        return await user.insert()
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            # Convert string to ObjectId for MongoDB query
            object_id = ObjectId(user_id)
            return await User.find_one(User.id == object_id)
        except:
            # If conversion fails, try direct string comparison as fallback
            return await User.find_one(User.id == user_id)
    
    @staticmethod
    async def update_user(user_id: str, **kwargs) -> Optional[User]:
        """Update user"""
        user = await User.find_one(User.id == user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.updated_at = datetime.now()
            await user.save()
        return user

# Project Services
class ProjectService:
    @staticmethod
    async def create_project(title: str, owner_id: str, **kwargs) -> Project:
        """Create a new project"""
        try:
            print(f"📝 ProjectService.create_project called with title: {title}")
            print(f"📝 Owner ID: {owner_id}")
            print(f"📝 Additional kwargs: {list(kwargs.keys())}")
            
            project_data = {
                "title": title,
                "owner_id": owner_id,
                **kwargs
            }
            
            print(f"📝 Creating Project instance with data keys: {list(project_data.keys())}")
            project = Project(**project_data)
            print(f"📝 Project instance created, inserting into database...")
            
            result = await project.insert()
            print(f"📝 Project inserted successfully with ID: {result.id}")
            return result
        except Exception as e:
            print(f"❌ ProjectService.create_project failed: {str(e)}")
            print(f"❌ Full error traceback: {traceback.format_exc()}")
            raise
    
    @staticmethod
    async def get_project_by_id(project_id: str) -> Optional[Project]:
        """Get project by ID"""
        try:
            object_id = ObjectId(project_id)
            return await Project.find_one(Project.id == object_id)
        except:
            return await Project.find_one(Project.id == project_id)
    
    @staticmethod
    async def get_projects_by_owner(owner_id: str) -> List[Project]:
        """Get projects by owner"""
        return await Project.find(Project.owner_id == owner_id).to_list()
    
    @staticmethod
    async def get_projects_by_collaborator(user_id: str) -> List[Project]:
        """Get projects where user is a collaborator"""
        return await Project.find(In(Project.collaborators, [user_id])).to_list()
    
    @staticmethod
    async def update_project(project_id: str, **kwargs) -> Optional[Project]:
        """Update project"""
        try:
            object_id = ObjectId(project_id)
            project = await Project.find_one(Project.id == object_id)
        except:
            project = await Project.find_one(Project.id == project_id)
            
        if project:
            for key, value in kwargs.items():
                setattr(project, key, value)
            project.updated_at = datetime.now()
            await project.save()
        return project
    
    @staticmethod
    async def delete_project(project_id: str) -> bool:
        """Delete project"""
        try:
            object_id = ObjectId(project_id)
            project = await Project.find_one(Project.id == object_id)
        except:
            project = await Project.find_one(Project.id == project_id)
            
        if project:
            await project.delete()
            return True
        return False

# Scene Services
class SceneService:
    @staticmethod
    async def create_scene(project_id: str, **kwargs) -> Scene:
        """Create a new scene"""
        scene_data = {
            "project_id": project_id,
            **kwargs
        }
        scene = Scene(**scene_data)
        return await scene.insert()
    
    @staticmethod
    async def get_scenes_by_project(project_id: str) -> List[Scene]:
        """Get scenes by project"""
        return await Scene.find(Scene.project_id == project_id).to_list()
    
    @staticmethod
    async def get_scene_by_id(scene_id: str) -> Optional[Scene]:
        """Get scene by ID"""
        return await Scene.find_one(Scene.id == scene_id)
    
    @staticmethod
    async def update_scene(scene_id: str, **kwargs) -> Optional[Scene]:
        """Update scene"""
        scene = await Scene.find_one(Scene.id == scene_id)
        if scene:
            for key, value in kwargs.items():
                setattr(scene, key, value)
            scene.updated_at = datetime.now()
            await scene.save()
        return scene

# Character Services
class CharacterService:
    @staticmethod
    async def create_character(project_id: str, **kwargs) -> Character:
        """Create a new character"""
        character_data = {
            "project_id": project_id,
            **kwargs
        }
        character = Character(**character_data)
        return await character.insert()
    
    @staticmethod
    async def get_characters_by_project(project_id: str) -> List[Character]:
        """Get characters by project"""
        return await Character.find(Character.project_id == project_id).to_list()
    
    @staticmethod
    async def get_character_by_id(character_id: str) -> Optional[Character]:
        """Get character by ID"""
        return await Character.find_one(Character.id == character_id)

# Location Services
class LocationService:
    @staticmethod
    async def create_location(project_id: str, **kwargs) -> Location:
        """Create a new location"""
        location_data = {
            "project_id": project_id,
            **kwargs
        }
        location = Location(**location_data)
        return await location.insert()
    
    @staticmethod
    async def get_locations_by_project(project_id: str) -> List[Location]:
        """Get locations by project"""
        return await Location.find(Location.project_id == project_id).to_list()

# Props Services
class PropsService:
    @staticmethod
    async def create_props(project_id: str, **kwargs) -> Props:
        """Create new props"""
        props_data = {
            "project_id": project_id,
            **kwargs
        }
        props = Props(**props_data)
        return await props.insert()
    
    @staticmethod
    async def get_props_by_project(project_id: str) -> List[Props]:
        """Get props by project"""
        return await Props.find(Props.project_id == project_id).to_list()

# Budget Services
class BudgetService:
    @staticmethod
    async def create_budget_item(project_id: str, **kwargs) -> Budget:
        """Create a new budget item"""
        budget_data = {
            "project_id": project_id,
            **kwargs
        }
        budget = Budget(**budget_data)
        return await budget.insert()
    
    @staticmethod
    async def get_budget_by_project(project_id: str) -> List[Budget]:
        """Get budget items by project"""
        return await Budget.find(Budget.project_id == project_id).to_list()
    
    @staticmethod
    async def get_total_budget(project_id: str) -> float:
        """Calculate total budget for project"""
        budget_items = await BudgetService.get_budget_by_project(project_id)
        return sum(item.estimated_cost * item.quantity for item in budget_items)

# File Upload Services
class FileUploadService:
    @staticmethod
    async def create_file_upload(user_id: str, **kwargs) -> FileUpload:
        """Create a new file upload record"""
        file_data = {
            "user_id": user_id,
            **kwargs
        }
        file_upload = FileUpload(**file_data)
        return await file_upload.insert()
    
    @staticmethod
    async def get_files_by_project(project_id: str) -> List[FileUpload]:
        """Get files by project"""
        return await FileUpload.find(FileUpload.project_id == project_id).to_list()
    
    @staticmethod
    async def get_files_by_user(user_id: str) -> List[FileUpload]:
        """Get files by user"""
        return await FileUpload.find(FileUpload.user_id == user_id).to_list()

# Comment Services
class CommentService:
    @staticmethod
    async def create_comment(project_id: str, user_id: str, **kwargs) -> Comment:
        """Create a new comment"""
        comment_data = {
            "project_id": project_id,
            "user_id": user_id,
            **kwargs
        }
        comment = Comment(**comment_data)
        return await comment.insert()
    
    @staticmethod
    async def get_comments_by_target(target_type: str, target_id: str) -> List[Comment]:
        """Get comments by target"""
        return await Comment.find(
            Comment.target_type == target_type,
            Comment.target_id == target_id
        ).to_list()

# Collaborator Services
class CollaboratorService:
    @staticmethod
    async def add_collaborator(project_id: str, user_id: str, invited_by: str, **kwargs) -> ProjectCollaborator:
        """Add a collaborator to project"""
        collaborator_data = {
            "project_id": project_id,
            "user_id": user_id,
            "invited_by": invited_by,
            **kwargs
        }
        collaborator = ProjectCollaborator(**collaborator_data)
        return await collaborator.insert()
    
    @staticmethod
    async def get_collaborators_by_project(project_id: str) -> List[ProjectCollaborator]:
        """Get collaborators by project"""
        return await ProjectCollaborator.find(ProjectCollaborator.project_id == project_id).to_list()
    
    @staticmethod
    async def accept_invitation(project_id: str, user_id: str) -> Optional[ProjectCollaborator]:
        """Accept collaboration invitation"""
        collaborator = await ProjectCollaborator.find_one(
            ProjectCollaborator.project_id == project_id,
            ProjectCollaborator.user_id == user_id
        )
        if collaborator:
            collaborator.invitation_accepted = True
            collaborator.updated_at = datetime.now()
            await collaborator.save()
        return collaborator
