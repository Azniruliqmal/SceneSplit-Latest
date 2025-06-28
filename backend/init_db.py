"""
Database initialization script for SceneSplit AI
"""
import asyncio
from database.config import init_database, close_database
from database.models import User, Project, UserRole, ProjectStatus
from database.services import UserService, ProjectService
from auth.auth import get_password_hash
import json


async def create_demo_users():
    """Create demo users for testing"""
    demo_users = [
        {
            "email": "admin@scenesplit.com",
            "username": "admin",
            "password": "password123",
            "full_name": "Admin User",
            "role": UserRole.ADMIN
        },
        {
            "email": "director@scenesplit.com", 
            "username": "director",
            "password": "director123",
            "full_name": "John Director",
            "role": UserRole.DIRECTOR
        },
        {
            "email": "producer@scenesplit.com",
            "username": "producer", 
            "password": "producer123",
            "full_name": "Sarah Producer",
            "role": UserRole.PRODUCER
        }
    ]
    
    for user_data in demo_users:
        # Check if user already exists
        existing_user = await UserService.get_user_by_email(user_data["email"])
        if not existing_user:
            hashed_password = get_password_hash(user_data["password"])
            
            await UserService.create_user(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=hashed_password,
                full_name=user_data["full_name"],
                role=user_data["role"],
                is_active=True,
                is_verified=True
            )
            print(f"✅ Created demo user: {user_data['email']}")
        else:
            print(f"📝 Demo user already exists: {user_data['email']}")


async def create_demo_projects():
    """Create demo projects for testing"""
    # Get admin user to own the demo projects
    admin_user = await UserService.get_user_by_email("admin@scenesplit.com")
    if not admin_user:
        print("❌ Admin user not found. Cannot create demo projects.")
        return
    
    # Sample analysis data structure
    demo_analysis_data = {
        "meta": {
            "success": True,
            "version": "2.0.0",
            "timestamp": "2024-12-01T10:00:00Z",
            "processing_time_ms": 5000
        },
        "script_breakdown": {
            "summary": {
                "total_scenes": 6,
                "total_characters": 4,
                "total_locations": 3,
                "estimated_shoot_days": 5,
                "budget_category": "medium"
            },
            "scenes": [
                {
                    "id": 1,
                    "header": "INT. HOSPITAL LOBBY - DAY",
                    "location": {
                        "name": "Hospital Lobby",
                        "type": "interior",
                        "time_of_day": "day"
                    },
                    "content": {
                        "estimated_pages": 1.5,
                        "dialogue_lines": ["Excuse me, I have an appointment with Dr. Amir at 2 PM."],
                        "action_lines": ["Nurul approaches the reception desk"],
                        "special_requirements": ["Hospital set decoration"]
                    },
                    "characters": ["NURUL", "RECEPTIONIST"],
                    "props": ["Reception desk", "Chairs", "Files"],
                    "analysis": {
                        "narrative": {
                            "purpose": "Establishing scene",
                            "dramatic_weight": "low",
                            "emotional_tone": "Neutral",
                            "content_type": "dialogue_heavy"
                        },
                        "production": {
                            "complexity": "simple",
                            "estimated_shoot_hours": 4,
                            "setup_hours": 2,
                            "crew_size": "standard",
                            "equipment_needs": ["Basic lighting", "Camera"]
                        },
                        "cost": {
                            "category": "low",
                            "factors": ["Simple dialogue scene", "Standard crew"]
                        }
                    }
                }
            ],
            "characters": {
                "main": [
                    {
                        "name": "NURUL",
                        "scenes": [1, 2, 3, 4, 5, 6],
                        "scene_count": 6,
                        "role_type": "protagonist",
                        "casting_notes": "Pregnant woman, 25-35 years old"
                    },
                    {
                        "name": "DR. AMIR",
                        "scenes": [2, 3, 4],
                        "scene_count": 3,
                        "role_type": "supporting",
                        "casting_notes": "Experienced doctor, 40-55 years old"
                    }
                ],
                "supporting": [
                    {
                        "name": "RECEPTIONIST",
                        "scenes": [1],
                        "scene_count": 1,
                        "role_type": "supporting",
                        "casting_notes": "Friendly hospital staff"
                    }
                ],
                "interactions": []
            },
            "locations": {
                "interior": [
                    {
                        "name": "Hospital Lobby",
                        "scenes": [1],
                        "setup_complexity": "simple",
                        "permit_required": False,
                        "equipment_access": "Good"
                    },
                    {
                        "name": "Delivery Room",
                        "scenes": [2, 3, 4, 5, 6],
                        "setup_complexity": "complex",
                        "permit_required": True,
                        "equipment_access": "Limited"
                    }
                ],
                "exterior": [],
                "shooting_groups": [
                    {
                        "location": "Hospital Lobby",
                        "scenes": [1],
                        "estimated_days": 1
                    },
                    {
                        "location": "Delivery Room", 
                        "scenes": [2, 3, 4, 5, 6],
                        "estimated_days": 4
                    }
                ]
            },
            "props_and_wardrobe": {
                "props": {
                    "by_category": {
                        "medical": ["IV stand", "Baby cot", "Medical tools"],
                        "furniture": ["Reception desk", "Chairs", "Hospital bed"],
                        "documents": ["Files", "Medical charts"]
                    },
                    "by_scene": [
                        {
                            "scene_id": 1,
                            "required": ["Reception desk", "Chairs", "Files"],
                            "complexity": "simple"
                        }
                    ]
                },
                "wardrobe": {
                    "by_character": {
                        "NURUL": {
                            "scenes": [1, 2, 3, 4, 5, 6],
                            "requirements": ["Casual wear", "Patient gown"],
                            "changes": 2
                        }
                    }
                },
                "set_decoration": [
                    {
                        "location": "Hospital Lobby",
                        "requirements": ["Hospital signage", "Medical posters", "Waiting area setup"]
                    }
                ]
            }
        },
        "production_planning": {
            "schedule": {
                "total_shoot_days": 5,
                "by_location": [
                    {
                        "location": "Hospital Lobby",
                        "scenes": [1],
                        "estimated_days": 1,
                        "priority": "medium"
                    }
                ],
                "cast_schedule": {
                    "NURUL": {
                        "scenes": [1, 2, 3, 4, 5, 6],
                        "total_days": 5,
                        "consecutive": True
                    }
                }
            },
            "budget": {
                "overall_category": "medium",
                "major_cost_drivers": ["Location fees", "Medical equipment rental", "Cast"],
                "optimization_opportunities": ["Bundle location shoots", "Use existing medical equipment"],
                "scene_breakdown": [
                    {
                        "scene_id": 1,
                        "category": "low",
                        "factors": ["Simple dialogue", "Standard crew"]
                    }
                ]
            },
            "crew_requirements": {
                "core_crew": ["Director", "DP", "Sound", "Gaffer", "Script Supervisor"],
                "by_scene": [
                    {
                        "scene_id": 1,
                        "crew_size": "standard",
                        "specialists": ["Medical consultant"]
                    }
                ]
            }
        }
    }
    
    demo_projects = [
        {
            "title": "Bilik Persalinan",
            "description": "A Malaysian drama about childbirth in a hospital setting",
            "status": ProjectStatus.REVIEW,
            "script_filename": "bilik_persalinan.pdf",
            "analysis_data": demo_analysis_data,
            "budget_total": 85000.0,
            "estimated_duration_days": 5
        },
        {
            "title": "Urban Legends",
            "description": "Short horror film exploring urban myths",
            "status": ProjectStatus.IN_PROGRESS,
            "script_filename": "urban_legends.fountain", 
            "analysis_data": demo_analysis_data,
            "budget_total": 120000.0,
            "estimated_duration_days": 8
        }
    ]
    
    for project_data in demo_projects:
        # Check if project already exists
        existing_projects = await ProjectService.get_projects_by_owner(admin_user.id)
        project_exists = any(p.title == project_data["title"] for p in existing_projects)
        
        if not project_exists:
            await ProjectService.create_project(
                title=project_data["title"],
                description=project_data["description"],
                owner_id=admin_user.id,
                status=project_data["status"],
                script_filename=project_data["script_filename"],
                analysis_data=project_data["analysis_data"],
                budget_total=project_data["budget_total"],
                estimated_duration_days=project_data["estimated_duration_days"]
            )
            print(f"✅ Created demo project: {project_data['title']}")
        else:
            print(f"📝 Demo project already exists: {project_data['title']}")


async def main():
    """Initialize database with demo data"""
    print("🚀 Initializing database...")
    
    try:
        # Initialize database connection
        await init_database()
        print("✅ Database connection established")
        
        # Create demo users
        print("\n👤 Creating demo users...")
        await create_demo_users()
        
        # Create demo projects
        print("\n📁 Creating demo projects...")
        await create_demo_projects()
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nDemo users created:")
        print("  - admin@scenesplit.com / password123 (Admin)")
        print("  - director@scenesplit.com / director123 (Director)")
        print("  - producer@scenesplit.com / producer123 (Producer)")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        raise
    finally:
        await close_database()
        print("👋 Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())