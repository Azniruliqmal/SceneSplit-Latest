# SceneSplit AI - Film Production Management System

SceneSplit AI is an intelligent film production management application that helps filmmakers analyze scripts, create budgets, plan schedules, and manage all aspects of film production with the power of AI.

## 🚀 Features

- **AI-Powered Script Analysis**: Automatic breakdown of scenes, characters, locations, and props
- **Smart Budget Generation**: AI-driven cost estimation and budget planning
- **Production Scheduling**: Intelligent timeline and resource planning
- **AI Assistant**: General-purpose AI chat with custom film production expertise
- **User Authentication**: Support for registered users and guest access
- **Modern UI**: Clean, responsive interface with glass-morphism design

## 📋 Prerequisites

Before running the application, make sure you have:

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git**
- **Google Gemini API Key** (for AI features)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd draft-ss-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt


# Edit .env file and add your Gemini API key
# GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Getting Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create environment file (if needed)

```

## 🚀 Running the Application

### Start Backend Server

```bash
# From backend directory
cd backend

# Start FastAPI server
python -m uvicorn api:app --reload 
```

The backend will be available at: `http://localhost:8000`

### Start Frontend Development Server

```bash
# From frontend directory (open new terminal)
cd frontend

# Start Vite development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 👥 Demo User Accounts

### Registered Users

You can login with these demo accounts:

| Email | Password | Role |
|-------|----------|------|
| `admin@scenesplit.com` | `password123` | Administrator |
| `director@scenesplit.com` | `director123` | Director |
| `producer@scenesplit.com` | `producer123` | Producer |

### Guest Access

Alternatively, you can use **Guest Access**:
1. Click "Continue as Guest" on the login page
2. Enter your name (email optional)
3. Accept terms and conditions
4. Access is limited to 7 days

## 🤖 AI Assistant Features

The AI Assistant can help with:

### General Conversations
- Ask any general questions
- Get helpful responses on various topics

### Film Production Assistance
- **Script Analysis**: "Analyze my script for characters and locations"
- **Budget Planning**: "Help me create a budget for my film"
- **Scheduling**: "Create a production schedule"
- **Location Scouting**: "Suggest locations for my scenes"
- **Casting**: "Analyze character requirements"

## 📁 Project Structure

```
draft-ss-app/
├── backend/                 # FastAPI backend
│   ├── agents/             # AI analysis agents
│   ├── graph/              # Workflow management
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── api.py              # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia state management
│   │   ├── assets/        # Static assets
│   │   └── router/        # Vue Router configuration
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # This file
```

## 🛠️ API Endpoints

### Script Analysis
- `POST /analyze-script` - Analyze script from text
- `POST /analyze-script-file` - Analyze uploaded script file
- `POST /submit-feedback` - Submit human feedback for revisions

### AI Chat
- `POST /chat` - Chat with AI assistant

### Workflow Management
- `GET /workflow-status/{thread_id}` - Get workflow status
- `GET /scenes/{thread_id}/{scene_id}` - Get specific scene data
- `GET /departments/{thread_id}/{department}` - Get department data

### Health Check
- `GET /health` - API health status

## 🎯 Usage Examples

### 1. Script Analysis
1. Login or use guest access
2. Navigate to "New Project"
3. Upload a script file (.pdf, .txt, .fountain) or paste script content
4. Click "Analyze Script"
5. Review the AI-generated breakdown
6. Provide feedback for improvements

### 2. AI Chat
1. Click the AI Assistant button (bottom-right corner)
2. Ask questions like:
   - "How do I create a budget for a short film?"
   - "What are the key elements of script breakdown?"
   - "Help me plan a 3-day shoot schedule"

### 3. Budget Planning
1. Complete script analysis first
2. Navigate to "Budget" section
3. Review AI-generated budget estimates
4. Modify costs as needed

## 🔧 Development

### Backend Development
```bash
# Run with auto-reload
python -m uvicorn api:app --reload

# Run tests (if available)
python -m pytest

# Check code style
black . --check
```

### Frontend Development
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🌐 Environment Variables

### Backend (.env)
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=SceneSplit AI
```

## 🚨 Troubleshooting

### Common Issues

**Backend not starting:**
- Check if Python dependencies are installed: `pip install -r requirements.txt`
- Verify Gemini API key is set in `.env`
- Ensure port 8000 is available

**Frontend not loading:**
- Check if Node.js dependencies are installed: `npm install`
- Verify backend is running on port 8000
- Clear browser cache and try again

**AI features not working:**
- Verify Gemini API key is valid and has quota
- Check backend console for error messages
- Ensure internet connection is stable

**Login issues:**
- Use exact demo credentials provided above
- Check if backend authentication endpoints are working
- Clear browser localStorage if needed

## 📝 License

This project is proprietary software developed for Gamuda Cohort 3.

## 👨‍💻 Developer

Created by **Aznir** for Gamuda Cohort 3 program.

---

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure environment variables are properly set
4. Check both backend and frontend console logs for errors

Happy filmmaking with SceneSplit AI! 🎬✨
