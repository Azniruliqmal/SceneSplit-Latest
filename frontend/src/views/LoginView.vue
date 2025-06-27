<template>
  <div class="min-h-screen flex items-center justify-center bg-background-primary relative overflow-hidden">
    <!-- Background Image -->
    <div 
      class="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-30"
      style="background-image: url('/src/assets/image/bg-posters.png')"
    ></div>
    
    <!-- Dark Overlay -->
    <div class="absolute inset-0 bg-black bg-opacity-50"></div>
    
    <div class="bg-background-secondary/80 backdrop-blur-sm rounded-2xl shadow-2xl p-12 w-full max-w-md flex flex-col items-center border border-gray-700/50 relative z-10">
      <!-- Logo -->
      <div class="flex items-center justify-center mb-6">
        <div class="flex flex-col items-center">
          <img 
            src="/src/assets/image/Logo.png" 
            alt="SceneSplit AI Logo" 
            class="h-20 w-auto mb-3"
          />
          <span class="text-2xl font-inter-bold text-white -mb-5">
            Scene<span class="text-secondary font-inter-regular italic">Split</span> AI
          </span>
        </div>
      </div>
      
      <p class="text-text-muted text-sm mb-8 font-inter-regular text-center">Your AI Buddy for Filmmakers</p>

      <!-- Login Form -->
      <form @submit.prevent="onLogin" class="w-full space-y-6">
        <!-- Email Field -->
        <div class="space-y-2">
          <label class="block text-text-secondary text-sm font-inter-medium" for="email">Email</label>
          <input
            v-model="email"
            id="email"
            type="email"
            required
            class="w-full px-4 py-3 rounded-lg bg-background-tertiary text-white border border-gray-600 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all font-inter-regular placeholder-text-muted"
            placeholder="your@email.com"
          />
        </div>

        <!-- Password Field -->
        <div class="space-y-2">
          <label class="block text-text-secondary text-sm font-inter-medium" for="password">Password</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="w-full px-4 py-3 rounded-lg bg-background-tertiary text-white border border-gray-600 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all font-inter-regular placeholder-text-muted"
            placeholder="••••••••"
          />
        </div>

        <!-- Forgot Password -->
        <div class="flex justify-end">
          <a href="#" class="text-text-muted text-sm hover:text-secondary transition-colors font-inter-regular">Forgot password?</a>
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-secondary text-black font-inter-semibold py-3 rounded-lg hover:bg-secondary-hover transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-black" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Signing In...' : 'Sign In' }}
        </button>

        <!-- Continue as Guest Button -->
        <button
          type="button"
          class="w-full border border-secondary text-secondary font-inter-semibold py-3 rounded-lg hover:bg-secondary hover:text-black transition-all duration-200"
          @click="goToGuest"
        >
          Continue as Guest
        </button>

        <!-- Divider -->
        <div class="flex items-center my-6">
          <div class="flex-1 h-px bg-gray-700"></div>
          <span class="mx-4 text-text-muted text-sm font-inter-regular">or</span>
          <div class="flex-1 h-px bg-gray-700"></div>
        </div>

        <!-- Social Login -->
        <div class="flex justify-center gap-4">
          <button 
            type="button" 
            class="bg-background-tertiary hover:bg-gray-600 rounded-lg p-3 transition-colors border border-gray-600"
            @click="socialLogin('google')"
          >
            <svg class="w-6 h-6" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
          </button>
          <button 
            type="button" 
            class="bg-background-tertiary hover:bg-gray-600 rounded-lg p-3 transition-colors border border-gray-600"
            @click="socialLogin('apple')"
          >
            <svg class="w-6 h-6" fill="white" viewBox="0 0 24 24">
              <path d="M18.71 19.5c-.83 1.24-1.71 2.45-2.86 2.45-1.03 0-1.29-.61-2.56-.61-1.26 0-1.65.63-2.64.63-1.14 0-2.08-1.33-2.93-2.54C5.78 16.93 5 14.94 5 13.04c0-3.36 2.19-5.14 4.35-5.14 1.13 0 2.08.74 2.8.74.71 0 1.82-.83 3.07-.83 1.08 0 3.04.31 4.01 2.33-.35.21-2.39 1.39-2.39 4.22 0 3.01 2.67 4.06 2.67 4.09-.03.07-.42 1.48-1.35 2.92-.78 1.14-1.55 2.3-2.86 2.3z"/>
              <path d="M15.94 2.91c-.69.85-1.94 1.53-3.07 1.53-.15-1.09.27-2.27.94-3.03.71-.85 2.01-1.52 2.94-1.52.13 1.1-.25 2.25-.94 3.03h.13z"/>
            </svg>
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
          <div class="text-red-400 text-sm font-inter-regular text-center">{{ error }}</div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/projectStore'

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const router = useRouter()
const projectStore = useProjectStore()

// Demo users for testing
const demoUsers = [
  {
    email: 'admin@scenesplit.com',
    password: 'password123',
    name: 'Admin User',
    role: 'Administrator'
  },
  {
    email: 'director@scenesplit.com',
    password: 'director123',
    name: 'John Director',
    role: 'Director'
  },
  {
    email: 'producer@scenesplit.com',
    password: 'producer123',
    name: 'Sarah Producer',
    role: 'Producer'
  }
]

async function onLogin() {
  if (!email.value || !password.value) {
    error.value = 'Please enter both email and password'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Check against demo users
    const user = demoUsers.find(u => u.email === email.value && u.password === password.value)
    
    if (user) {
      // Set authentication state
      projectStore.setLogin(true)
      projectStore.setUser({
        name: user.name,
        role: user.role,
        email: user.email,
        type: 'registered'
      })
      
      // Store user data in localStorage for persistence
      localStorage.setItem('userData', JSON.stringify({
        name: user.name,
        role: user.role,
        email: user.email,
        type: 'registered'
      }))
      
      router.push({ name: 'ProjectsView' })
    } else {
      error.value = 'Invalid email or password. Try: admin@scenesplit.com / password123'
    }
  } catch (err) {
    error.value = 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

function goToGuest() {
  router.push({ name: 'GuestAccess' })
}

function socialLogin(provider: string) {
  error.value = `${provider} login is not implemented yet. Use demo credentials: admin@scenesplit.com / password123`
}
</script>