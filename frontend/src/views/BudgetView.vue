<template>
  <div class="transition-all duration-300" :class="sidebarExpanded ? 'ml-64' : 'ml-16'">
    <!-- Header Section -->
    <div
      class="w-full relative bg-background-primary h-20 flex flex-row items-center justify-between py-[15px] pl-[19px] pr-[104px] box-border gap-0 text-left text-2xl text-white font-inter z-30 border-b border-gray-700"
      style="position: sticky; top: 0;"
    >
      <div class="flex items-center gap-6">
        <h1 class="relative leading-[28.8px] font-inter-bold">Budget Management</h1>
        <select
          v-model="selectedProjectTitle"
          class="bg-background-tertiary text-secondary font-inter-semibold rounded-lg px-4 py-2 focus:outline-none border border-gray-600 focus:border-secondary transition-colors"
          @change="onProjectChange"
        >
          <option
            v-for="project in projects"
            :key="project.title"
            :value="project.title"
            class="bg-background-tertiary text-white"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      <div class="flex flex-row items-center justify-start gap-4 text-sm text-text-secondary">
        <div class="w-[100px] rounded-lg bg-gray-700 h-10 flex flex-row items-center justify-center gap-2 text-text-secondary cursor-pointer hover:bg-gray-600 transition-colors">
          <img class="w-4 h-4" alt="" src="../assets/icon/download.svg" />
          <div class="leading-[16.8px] font-inter-medium">Export</div>
        </div>
        <div class="w-[120px] rounded-lg bg-secondary h-10 flex flex-row items-center justify-center gap-1 cursor-pointer text-black hover:bg-secondary-hover transition-colors" @click="showAI = true">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
          </svg>
          <div class="leading-[16.8px] font-inter-semibold">AI Assistant</div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="bg-background-primary h-[calc(100vh-80px)] overflow-y-auto">
      <div class="p-6">
        <div class="max-w-7xl mx-auto flex flex-col gap-6">
          <!-- Budget Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-background-secondary rounded-xl p-6 flex flex-col gap-2 border border-gray-700">
              <div class="flex items-center gap-2 text-text-muted text-sm font-inter-regular">
                Total Budget
                <svg class="w-4 h-4 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 8v4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="text-2xl font-inter-bold text-white">{{ summary.totalBudget }}</div>
              <div class="text-text-muted text-xs font-inter-regular">Approved budget</div>
            </div>
            <div class="bg-background-secondary rounded-xl p-6 flex flex-col gap-2 border border-gray-700">
              <div class="flex items-center gap-2 text-text-muted text-sm font-inter-regular">
                Spent
                <svg class="w-4 h-4 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="text-2xl font-inter-bold text-white">{{ summary.spent }}</div>
              <div class="text-text-muted text-xs font-inter-regular">{{ summary.spentPercent }}% of budget</div>
            </div>
            <div class="bg-background-secondary rounded-xl p-6 flex flex-col gap-2 border border-gray-700">
              <div class="flex items-center gap-2 text-text-muted text-sm font-inter-regular">
                Remaining
                <svg class="w-4 h-4 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <div class="text-2xl font-inter-bold text-white">{{ summary.remaining }}</div>
              <div class="text-text-muted text-xs font-inter-regular">{{ summary.remainingPercent }}% remaining</div>
            </div>
            <div class="bg-background-secondary rounded-xl p-6 flex flex-col gap-2 border border-gray-700">
              <div class="flex items-center gap-2 text-text-muted text-sm font-inter-regular">
                Projected Total
                <svg class="w-4 h-4 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 8v4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="text-2xl font-inter-bold text-white">{{ summary.projectedTotal }}</div>
              <div class="text-text-muted text-xs font-inter-regular">{{ summary.projectedNote }}</div>
            </div>
          </div>

          <!-- Budget Breakdown -->
          <div class="bg-background-secondary rounded-2xl p-8 border border-gray-700">
            <div class="flex items-center justify-between mb-6">
              <div class="text-lg font-inter-bold text-white">Budget Breakdown by Category</div>
              <div class="flex items-center gap-2">
                <button class="bg-background-tertiary rounded-lg px-3 py-2 text-text-muted hover:text-white transition-colors flex items-center gap-1 border border-gray-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
                <button class="bg-background-tertiary rounded-lg px-3 py-2 text-text-muted hover:text-white transition-colors flex items-center gap-1 border border-gray-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 8v4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="breakdown.length" class="space-y-5">
              <div v-for="cat in breakdown" :key="cat.name" class="mb-5">
                <div class="flex items-center justify-between mb-2">
                  <div class="font-inter-semibold text-white" :style="{ color: cat.color }">{{ cat.name }}</div>
                  <div class="font-inter-semibold text-white" :style="{ color: cat.color }">{{ cat.amount }}</div>
                </div>
                <div class="flex items-center gap-4">
                  <div class="flex-1 h-3 rounded-lg bg-background-tertiary relative overflow-hidden">
                    <div
                      class="h-3 rounded-lg absolute left-0 top-0 transition-all duration-300"
                      :style="{ width: cat.percent + '%', background: cat.color }"
                    ></div>
                  </div>
                  <div class="text-text-muted text-xs w-14 font-inter-regular">{{ cat.percent }}%</div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12">
              <div class="text-text-muted font-inter-regular mb-4">No budget data available for this project.</div>
              <div class="text-text-muted text-sm font-inter-regular">Budget breakdown will appear here once the project has budget information.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Assistant Panel -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      enter-from-class="transform translate-x-full"
      enter-to-class="transform translate-x-0"
      leave-active-class="transition-transform duration-300 ease-in"
      leave-from-class="transform translate-x-0"
      leave-to-class="transform translate-x-full"
    >
      <AIChatPanel v-if="showAI" class="fixed top-0 right-0 z-50" @close="showAI = false" />
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject, watch } from 'vue'
import AIChatPanel from '../components/AIChatPanel.vue'
import { useProjectStore } from '../stores/projectStore'

const sidebarExpanded = inject('sidebarExpanded', ref(false))

const showAI = ref(false)
const projectStore = useProjectStore()
const projects = computed(() => projectStore.projects)
const selectedProjectTitle = ref(projectStore.selectedProjectTitle || projects.value[0]?.title || '')

// Find the selected project object
const selectedProject = computed(() =>
  projects.value.find(p => p.title === selectedProjectTitle.value)
)

// Handle project change
function onProjectChange() {
  projectStore.setSelectedProject(selectedProjectTitle.value)
}

// Helper: parse RM value to number
function parseRM(val: string | number) {
  if (!val) return 0
  const stringVal = String(val)
  return Number(stringVal.replace(/[^\d.]/g, ''))
}

// Budget summary logic
const summary = computed(() => {
  const project = selectedProject.value
  if (!project?.scriptBreakdown?.budget) {
    return {
      totalBudget: 'RM 0',
      spent: 'RM 0',
      spentPercent: 0,
      remaining: 'RM 0',
      remainingPercent: 0,
      projectedTotal: 'RM 0',
      projectedNote: 'No data'
    }
  }

  const budgetObj = project.scriptBreakdown.budget
  
  // Sum all categories for total
  const totalBudget = Object.values(budgetObj)
    .map(v => parseRM(v))
    .reduce((a, b) => a + b, 0)
  
  // Calculate spent, remaining, and projected amounts
  const spentPercent = 75 // Demo percentage
  const spent = Math.round(totalBudget * (spentPercent / 100))
  const remaining = totalBudget - spent
  const remainingPercent = Math.round((remaining / totalBudget) * 100)
  const projected = Math.round(totalBudget * 0.97)
  const projectedDiff = totalBudget - projected
  
  return {
    totalBudget: `RM ${totalBudget.toLocaleString()}`,
    spent: `RM ${spent.toLocaleString()}`,
    spentPercent,
    remaining: `RM ${remaining.toLocaleString()}`,
    remainingPercent,
    projectedTotal: `RM ${projected.toLocaleString()}`,
    projectedNote: projectedDiff > 0 ? `${Math.round((projectedDiff / totalBudget) * 100)}% under budget` : 'On track'
  }
})

// Budget breakdown by category with improved colors
const categoryColors: Record<string, string> = {
  talent: '#00C6FB',
  location: '#FFD233', 
  propsSet: '#3DD65B',
  wardrobeMakeup: '#A259FF',
  sfxVfx: '#FF6B6B',
  crew: '#FF9900',
  miscellaneous: '#FFB300'
}

const breakdown = computed(() => {
  const project = selectedProject.value
  if (!project?.scriptBreakdown?.budget) {
    return []
  }

  const budgetObj = project.scriptBreakdown.budget
  const total = Object.values(budgetObj)
    .map(v => parseRM(v))
    .reduce((a, b) => a + b, 0)
  
  if (total === 0) return []

  return Object.entries(budgetObj)
    .map(([key, val]) => {
      const amount = parseRM(val)
      return {
        name: formatCategoryName(key),
        amount: `RM ${amount.toLocaleString()}`,
        percent: +(amount / total * 100).toFixed(1),
        color: categoryColors[key] || '#888888'
      }
    })
    .filter(item => item.percent > 0)
    .sort((a, b) => b.percent - a.percent) // Sort by percentage descending
})

// Helper function to format category names
function formatCategoryName(key: string): string {
  const nameMap: Record<string, string> = {
    talent: 'Talent',
    location: 'Location',
    propsSet: 'Props & Set',
    wardrobeMakeup: 'Wardrobe & Makeup',
    sfxVfx: 'SFX & VFX',
    crew: 'Crew',
    miscellaneous: 'Miscellaneous'
  }
  
  return nameMap[key] || key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, s => s.toUpperCase())
}

// Watch for project changes
watch(selectedProject, (newProject) => {
  if (newProject) {
    projectStore.setSelectedProject(newProject.title)
  }
}, { immediate: true })
</script>

<style scoped>
div[style*="linear-gradient"] {
  background: linear-gradient(90deg, #00C6FB 0%, #005BEA 100%) !important;
}
</style>
