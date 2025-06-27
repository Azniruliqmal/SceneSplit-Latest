<template>
  <div class="min-h-screen flex items-center justify-center bg-background-primary">
    <div class="bg-background-secondary rounded-2xl shadow-2xl p-12 w-full max-w-md flex flex-col items-center border border-gray-700">
      <!-- Logo and Branding -->
      <div class="flex items-center justify-center mb-4">
        <div class="bg-secondary rounded-lg p-2 mr-3">
          <svg class="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
          </svg>
        </div>
        <div class="text-center">
          <div class="text-xs text-secondary font-inter-semibold mb-1">SceneSplit AI</div>
        </div>
      </div>
      
      <h1 class="text-3xl font-inter-bold text-white mb-2 text-center">
        Scene<span class="font-inter-regular italic text-secondary">Split</span>
      </h1>
      <p class="text-text-muted text-sm mb-8 font-inter-regular text-center">Your AI Buddy for Filmmakers</p>

      <!-- Guest Access Form -->
      <form @submit.prevent="onGuest" class="w-full space-y-6">
        <!-- Name Field -->
        <div class="space-y-2">
          <label class="block text-text-secondary text-sm font-inter-medium" for="name">Your Name</label>
          <input
            v-model="name"
            id="name"
            type="text"
            required
            class="w-full px-4 py-3 rounded-lg bg-background-tertiary text-white border border-gray-600 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all font-inter-regular placeholder-text-muted"
            placeholder="John Doe"
          />
        </div>

        <!-- Email Field (Optional) -->
        <div class="space-y-2">
          <label class="block text-text-secondary text-sm font-inter-medium" for="guestEmail">Email (optional)</label>
          <input
            v-model="guestEmail"
            id="guestEmail"
            type="email"
            class="w-full px-4 py-3 rounded-lg bg-background-tertiary text-white border border-gray-600 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all font-inter-regular placeholder-text-muted"
            placeholder="your@email.com"
          />
        </div>

        <!-- Terms Agreement -->
        <div class="space-y-3">
          <div class="flex items-start space-x-3">
            <input 
              type="checkbox" 
              id="agree" 
              v-model="agree" 
              required 
              class="mt-0.5 w-4 h-4 text-secondary bg-background-tertiary border border-gray-600 rounded focus:ring-secondary focus:ring-2"
            />
            <label for="agree" class="text-secondary text-sm font-inter-regular cursor-pointer">
              I agree to the <span class="underline hover:text-secondary-hover">Terms of Service</span> and <span class="underline hover:text-secondary-hover">Privacy Policy</span>
            </label>
          </div>
          
          <div class="bg-background-tertiary rounded-lg p-4 border border-gray-600">
            <div class="flex items-center space-x-2 text-text-muted">
              <svg class="w-5 h-5 text-secondary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-sm font-inter-regular">Note: Guest access is limited to 7 days</span>
            </div>
          </div>
        </div>

        <!-- Continue as Guest Button -->
        <button
          type="submit"
          :disabled="isLoading || !agree"
          class="w-full bg-secondary text-black font-inter-semibold py-3 rounded-lg hover:bg-secondary-hover transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-black" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Setting up...' : 'Continue as Guest' }}
        </button>

        <!-- Back to Login Button -->
        <button
          type="button"
          class="w-full border border-gray-600 text-text-secondary font-inter-semibold py-3 rounded-lg hover:bg-background-tertiary hover:text-white transition-all duration-200"
          @click="goToLogin"
        >
          Back to Login
        </button>

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

const name = ref('')
const guestEmail = ref('')
const agree = ref(false)
const error = ref('')
const isLoading = ref(false)
const router = useRouter()
const projectStore = useProjectStore()

async function onGuest() {
  if (!name.value.trim()) {
    error.value = 'Please enter your name'
    return
  }

  if (!agree.value) {
    error.value = 'Please agree to the Terms of Service and Privacy Policy'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Simulate setup delay
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Calculate guest access expiry (7 days from now)
    const expiryDate = new Date()
    expiryDate.setDate(expiryDate.getDate() + 7)

    // Set authentication state for guest
    projectStore.setLogin(true)
    projectStore.setUser({
      name: name.value.trim(),
      role: 'Guest User',
      email: guestEmail.value || `guest_${Date.now()}@temp.local`,
      type: 'guest',
      expiresAt: expiryDate.toISOString()
    })
    
    // Store guest data in localStorage for persistence
    localStorage.setItem('userData', JSON.stringify({
      name: name.value.trim(),
      role: 'Guest User',
      email: guestEmail.value || `guest_${Date.now()}@temp.local`,
      type: 'guest',
      expiresAt: expiryDate.toISOString()
    }))
    
    // Store guest access timestamp
    localStorage.setItem('guestAccessStart', new Date().toISOString())
    
    router.push({ name: 'ProjectsView' })
  } catch (err) {
    error.value = 'Failed to set up guest access. Please try again.'
  } finally {
    isLoading.value = false
  }
}

function goToLogin() {
  router.push({ name: 'Login' })
}
</script>