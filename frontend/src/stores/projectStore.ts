import { defineStore } from 'pinia'
import { projects as staticProjects } from '../data/projects'

interface User {
  name: string
  role: string
  email: string
  type: 'registered' | 'guest'
  expiresAt?: string
}

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [...staticProjects],
    selectedProjectTitle: staticProjects[0]?.title || '',
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
    user: JSON.parse(localStorage.getItem('userData') || 'null') as User | null
  }),
  getters: {
    selectedProject(state) {
      return state.projects.find(p => p.title === state.selectedProjectTitle)
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
    setSelectedProject(title: string) {
      this.selectedProjectTitle = title
    },
    setProjects(newProjects: any[]) {
      this.projects = newProjects
    },
    addProject(project: any) {
      // Add timestamp to new projects for sorting
      const projectWithTimestamp = {
        ...project,
        createdAt: new Date().toISOString()
      }
      this.projects.push(projectWithTimestamp)
    },
    removeProject(projectTitle: string) {
      this.projects = this.projects.filter(p => p.title !== projectTitle)
    },
    updateProjectStatus(projectTitle: string, status: string, statusColor: string) {
      const project = this.projects.find(p => p.title === projectTitle)
      if (project) {
        project.status = status
        project.statusColor = statusColor
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
    logout() {
      this.isLoggedIn = false
      this.user = null
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('userData')
      localStorage.removeItem('guestAccessStart')
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
      }
    }
  }
})