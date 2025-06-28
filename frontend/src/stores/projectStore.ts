import { defineStore } from 'pinia'
import { projectsAPI, authAPI } from '../api'

interface User {
  name: string
  role: string
  email: string
  type: 'registered' | 'guest'
  expiresAt?: string
}

interface Project {
  id: string
  title: string
  description?: string
  status: string
  statusColor: string
  budget?: string
  dueDate?: string
  team?: string
  createdAt: string
  genre?: string
  scriptBreakdown?: any
  analysis_data?: any
  budget_total?: number
  estimated_duration_days?: number
}

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [] as Project[],
    selectedProjectId: '',
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
    user: JSON.parse(localStorage.getItem('userData') || 'null') as User | null,
    loading: false,
    error: null as string | null
  }),
  getters: {
    selectedProject(state): Project | undefined {
      return state.projects.find(p => p.id === state.selectedProjectId)
    },
    selectedProjectTitle(state): string {
      const project = state.projects.find(p => p.id === state.selectedProjectId)
      return project?.title || ''
    },
    isGuestUser(state): boolean {
      return state.user?.type === 'guest'
    },
    guestAccessExpired(state): boolean {
      if (!state.user || state.user.type !== 'guest' || !state.user.expiresAt) {
        return false
      }
      return new Date() > new Date(state.user.expiresAt)
    },
    daysUntilGuestExpiry(state): number {
      if (!state.user || state.user.type !== 'guest' || !state.user.expiresAt) {
        return 0
      }
      const now = new Date()
      const expiry = new Date(state.user.expiresAt)
      const diffTime = expiry.getTime() - now.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return Math.max(0, diffDays)
    }
  },
  actions: {
    // Project Management
    async fetchProjects() {
      this.loading = true
      this.error = null
      try {
        const response: any = await projectsAPI.getProjects()
        // Handle different response formats
        const projectsData = Array.isArray(response) ? response : (response.projects || [])
        this.projects = projectsData.map((project: any) => this.transformProjectData(project))
      } catch (error: any) {
        this.error = error.response?.data?.error?.message || 'Failed to fetch projects'
        console.error('Failed to fetch projects:', error)
      } finally {
        this.loading = false
      }
    },

    async createProjectWithScript(title: string, description: string, file: File) {
      this.loading = true
      this.error = null
      try {
        const response = await projectsAPI.createProject({ title, description, file })
        const newProject = this.transformProjectData(response)
        this.projects.unshift(newProject)
        return newProject
      } catch (error: any) {
        this.error = error.response?.data?.error?.message || 'Failed to create project'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getProjectAnalysis(projectId: string) {
      try {
        const response = await projectsAPI.getProjectAnalysis(projectId)
        return response.analysis_data
      } catch (error: any) {
        this.error = error.response?.data?.error?.message || 'Failed to get project analysis'
        throw error
      }
    },

    async updateProjectAnalysis(projectId: string, analysisData: any) {
      try {
        await projectsAPI.updateProjectAnalysis(projectId, analysisData)
        // Update local project data
        const project = this.projects.find(p => p.id === projectId)
        if (project) {
          project.analysis_data = analysisData
          project.scriptBreakdown = analysisData.script_breakdown
        }
      } catch (error: any) {
        this.error = error.response?.data?.error?.message || 'Failed to update project analysis'
        throw error
      }
    },

    setSelectedProject(projectIdOrTitle: string) {
      // Support both ID and title for backward compatibility
      const project = this.projects.find(p => 
        p.id === projectIdOrTitle || p.title === projectIdOrTitle
      )
      if (project) {
        this.selectedProjectId = project.id
      }
    },

    transformProjectData(apiProject: any): Project {
      return {
        id: apiProject.id,
        title: apiProject.title,
        description: apiProject.description,
        status: this.mapStatus(apiProject.status),
        statusColor: this.getStatusColor(apiProject.status),
        budget: apiProject.budget_total ? `$${(apiProject.budget_total / 1000).toFixed(0)}K` : '$0K',
        dueDate: apiProject.estimated_duration_days ? 
          new Date(Date.now() + apiProject.estimated_duration_days * 24 * 60 * 60 * 1000).toLocaleDateString() : 
          'TBD',
        team: '6 members', // Default team size
        createdAt: apiProject.created_at,
        genre: 'Feature Film • Drama', // Default genre
        scriptBreakdown: apiProject.analysis_data?.script_breakdown,
        analysis_data: apiProject.analysis_data,
        budget_total: apiProject.budget_total,
        estimated_duration_days: apiProject.estimated_duration_days
      }
    },

    mapStatus(apiStatus: string): string {
      const statusMap: Record<string, string> = {
        'draft': 'ACTIVE',
        'in_progress': 'ACTIVE', 
        'review': 'REVIEW',
        'completed': 'COMPLETED',
        'archived': 'COMPLETED'
      }
      return statusMap[apiStatus] || 'ACTIVE'
    },

    getStatusColor(status: string): string {
      const colorMap: Record<string, string> = {
        'ACTIVE': 'bg-yellow-400 text-black',
        'REVIEW': 'bg-[#232733] text-white',
        'COMPLETED': 'bg-green-400 text-black'
      }
      return colorMap[this.mapStatus(status)] || 'bg-yellow-400 text-black'
    },

    async updateProjectStatus(projectIdOrTitle: string, status: string, statusColor: string) {
      const project = this.projects.find(p => 
        p.id === projectIdOrTitle || p.title === projectIdOrTitle
      )
      if (project) {
        try {
          await projectsAPI.updateProject(project.id, { status })
          project.status = status
          project.statusColor = statusColor
        } catch (error: any) {
          this.error = error.response?.data?.error?.message || 'Failed to update project status'
          throw error
        }
      }
    },

    async removeProject(projectIdOrTitle: string) {
      const project = this.projects.find(p => 
        p.id === projectIdOrTitle || p.title === projectIdOrTitle
      )
      if (project) {
        try {
          await projectsAPI.deleteProject(project.id)
          this.projects = this.projects.filter(p => p.id !== project.id)
        } catch (error: any) {
          this.error = error.response?.data?.error?.message || 'Failed to delete project'
          throw error
        }
      }
    },

    // Authentication
    async login(email: string, password: string) {
      this.loading = true
      this.error = null
      try {
        const response = await authAPI.login({ email, password })
        
        // Store the access token
        localStorage.setItem('access_token', response.access_token)
        
        // Set user data
        const userData = {
          name: response.user.full_name || response.user.username,
          role: response.user.role,
          email: response.user.email,
          type: 'registered' as const
        }
        
        this.setUser(userData)
        this.setLogin(true)
        
        // Fetch projects after successful login
        await this.fetchProjects()
        
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Login failed'
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    setLogin(status: boolean) {
      this.isLoggedIn = status
      localStorage.setItem('isLoggedIn', status ? 'true' : 'false')
    },

    setUser(user: User) {
      this.user = user
      localStorage.setItem('userData', JSON.stringify(user))
    },

    async logout() {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.isLoggedIn = false
        this.user = null
        this.projects = []
        this.selectedProjectId = ''
        localStorage.removeItem('isLoggedIn')
        localStorage.removeItem('userData')
        localStorage.removeItem('access_token')
      }
    },

    checkGuestAccess() {
      if (this.user?.type === 'guest' && this.guestAccessExpired) {
        this.logout()
        return false
      }
      return true
    },

    initializeFromStorage() {
      // Restore user data on app initialization
      const storedUser = localStorage.getItem('userData')
      if (storedUser) {
        this.user = JSON.parse(storedUser)
        this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
        
        // Check if guest access has expired
        if (this.user?.type === 'guest') {
          this.checkGuestAccess()
        }

        // Fetch projects if logged in
        if (this.isLoggedIn) {
          this.fetchProjects()
        }
      }
    }
  }
})