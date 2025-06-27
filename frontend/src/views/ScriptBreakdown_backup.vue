<template>
  <div class="transition-all duration-300" :class="sidebarExpanded ? 'ml-80' : 'ml-20'">
    <!-- Header Section Start -->
    <div
      class="w-full relative bg-[#0D1019] h-20 flex flex-row items-center justify-between py-[15px] pl-[19px] pr-[104px] box-border gap-0 text-left text-2xl text-white font-inter z-30"
      style="position: sticky; top: 0;"
    >
      <div class="flex flex-col items-start justify-start">
        <b class="relative leading-[28.8px]">Script Analysis</b>
      </div>
      <div class="flex flex-row items-center justify-start gap-4 text-sm text-darkgray">
        <div class="w-80 rounded-lg bg-darkslategray h-10 flex flex-row items-center justify-start py-0 px-4 box-border gap-3">
          <img class="w-5 relative h-5 overflow-hidden shrink-0" alt="" src="../assets/icon/Search Icon.svg" />
          <div class="flex-1 relative leading-[16.8px]">Search scenes, elements...</div>
        </div>
        <div class="rounded-lg bg-darkslategray h-10 flex flex-row items-center justify-start py-0 px-4 box-border gap-2 text-white">
          <img class="w-4 relative h-4 overflow-hidden shrink-0" alt="" src="../assets/icon/download.svg" />
          <div class="relative leading-[16.8px] font-medium">Export</div>
        </div>
        <div class="rounded-lg bg-goldenrod h-10 flex flex-row items-center justify-start py-0 px-4 box-border gap-2 cursor-pointer text-gray-100" @click="onNewProjectButtonClick">
          <img class="w-4 relative h-4 overflow-hidden shrink-0" alt="" src="../assets/icon/Plus Icon.svg" />
          <div class="relative leading-[16.8px] font-semibold">New Project</div>
        </div>
      </div>
    </div>
    <!-- Header Section End -->

    <!-- Content Area Start -->
    <div class="flex justify-center items-start min-h-[80vh] bg-gray-950 py-12">
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Script Section -->
        <div
          class="bg-[#181C23] rounded-xl p-8"
          style="width:582px; height:796px; overflow-y:auto; min-width:350px;"
        >
          <!-- Script and Status Selection -->
          <div class="flex items-center gap-4 mb-4">
            <label class="font-bold text-white mr-2">Script:</label>
            <select
              v-model="selectedProjectTitle"
              class="bg-[#232733] text-yellow-400 font-semibold rounded-lg px-4 py-2 focus:outline-none border-none"
            >
              <option
                v-for="project in projects"
                :key="project.title"
                :value="project.title"
              >
                {{ project.title }}
              </option>
            </select>
            <!-- Status Selection Buttons -->
            <div class="flex gap-2 ml-4">
              <button
                v-for="status in statuses"
                :key="status.value"
                @click="setStatus(status.value)"
                :class="[
                  'px-4 py-2 rounded-lg font-bold transition',
                  selectedStatus === status.value
                    ? 'bg-yellow-400 text-black'
                    : 'bg-[#232733] text-yellow-400 hover:bg-yellow-500 hover:text-black'
                ]"
              >
                {{ status.label }}
              </button>
            </div>
          </div>

          <div>
            <div
              v-for="scene in scenes"
              :key="scene.number"
              :class="[
                'mb-5 rounded-lg bg-[#232733] p-5 cursor-pointer transition border-2',
                selectedSceneNumber === scene.number
                  ? 'border-goldenrod shadow-lg'
                  : 'border-transparent hover:border-goldenrod/60'
              ]"
              @click="selectedSceneNumber = scene.number"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <span class="bg-goldenrod text-black font-bold rounded-full w-7 h-7 flex items-center justify-center">{{ scene.number }}</span>
                  <span class="font-bold text-white text-base">{{ scene.heading }}</span>
                </div>
                <button class="text-gray-400 hover:text-yellow-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20h9" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 3.5l4 4-12 12H4.5v-4.5l12-12z" />
                  </svg>
                </button>
              </div>
              <div class="text-white text-sm mb-1">{{ scene.notes }}</div>
              <div v-if="scene.dialogues && Array.isArray(scene.dialogues)">
                <div v-for="(dialog, idx) in scene.dialogues" :key="idx" class="flex gap-2">
                  <span class="font-bold text-xs" :class="dialog.character === 'SARAH' ? 'text-yellow-400' : 'text-[#FFD233]'">
                    {{ dialog.character }}
                  </span>
                  <span class="text-gray-100 text-sm">{{ dialog.text }}</span>
                </div>
              </div>
              <div v-if="scene.characters && scene.characters.length" class="text-white text-xs mt-2">
                <b>Characters:</b> {{ scene.characters.join(', ') }}
              </div>
              <div v-if="scene.props && scene.props.length" class="text-white text-xs">
                <b>Props:</b> {{ scene.props.join(', ') }}
              </div>
            </div>
          </div>
        </div>

        <!-- Elements Breakdown Section -->
        <div
          class="bg-[#181C23] rounded-xl p-8"
          style="width:582px; height:796px; overflow-y:auto; min-width:350px;"
        >
          <div class="flex items-center justify-between mb-4">
            <div>
              <div class="text-lg font-bold text-white">Elements Breakdown</div>
              <div class="text-white text-xs">
                <template v-if="selectedSceneNumber">
                  Scene Number: {{ selectedSceneNumber }}
                </template>
                <template v-else>
                  Select a scene to view elements breakdown.
                </template>
              </div>
            </div>
          </div>
          <!-- Tabs -->
          <div class="flex gap-2 mb-6">
            <button
              v-for="tab in elementTabs"
              :key="tab"
              @click="activeTab = tab"
              :class="[
                'px-5 py-2 rounded-md font-semibold transition',
                activeTab === tab
                  ? 'bg-goldenrod text-[#181A20]'
                  : 'bg-[#232733] text-white hover:bg-[#232733]/80'
              ]"
            >
              {{ tab }}
            </button>
          </div>
          <!-- Elements List -->
          <div v-if="selectedSceneNumber">
            <div v-for="(el, idx) in filteredElements" :key="el.type + el.name + idx" class="flex items-start gap-4 mb-6">
              <div class="flex flex-col items-center pt-1">
                <span
                  v-if="el.type === 'Cast'"
                  class="bg-yellow-400 text-black font-bold text-xs px-3 py-1 rounded mb-1"
                >CAST</span>
                <span
                  v-else-if="el.type === 'Props'"
                  class="bg-[#1DE9B6] text-black font-bold text-xs px-3 py-1 rounded mb-1"
                >PROPS</span>
                <span
                  v-else-if="el.type === 'Location'"
                  class="bg-[#A259FF] text-black font-bold text-xs px-3 py-1 rounded mb-1"
                >LOCATION</span>
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-white">{{ el.name }}</span>
                  <span class="bg-[#232733] text-white text-xs rounded-full px-2 py-0.5">{{ el.count }}</span>
                </div>
                <div class="text-white text-sm mt-1" v-if="el.description">{{ el.description }}</div>
              </div>
              <div class="flex items-center gap-2">
                <button class="text-gray-400 hover:text-yellow-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M15.232 5.232l3.536 3.536M9 11l6 6M3 21h6v-6l9.293-9.293a1 1 0 0 0-1.414-1.414L9 9.586V3H3v6h6l9.293-9.293a1 1 0 0 0-1.414-1.414L9 9.586V3H3v6h6z" />
                  </svg>
                </button>
                <button class="text-gray-400 hover:text-red-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-white text-center mt-20">
            Please select a scene to see its elements.
          </div>
        </div>
      </div>
    </div>
    <!-- Content Area End -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, inject } from 'vue'
import { useProjectStore } from '../stores/projectStore'
import { useRouter } from 'vue-router'

const sidebarExpanded = inject('sidebarExpanded', false)

const router = useRouter()
const projectStore = useProjectStore()
const projects = projectStore.projects
const selectedProjectTitle = ref(projectStore.selectedProjectTitle || projects[0]?.title || '')
const selectedProject = computed(() =>
  projects.find(p => p.title === selectedProjectTitle.value)
)
type Dialogue = {
  character: string
  text: string
}

type Scene = {
  number: number
  heading: string
  location: string
  time: string
  characters: string[]
  props: string[]
  wardrobe: string[]
  sfx: string[]
  notes: string
  budget: string
  dialogues?: Dialogue[]
}

const scenes = computed<Scene[]>(() => selectedProject.value?.scriptBreakdown?.scenes || [])
type ElementsType = {
  characters?: Array<{ name: string; description?: string }>
  props?: Array<{ name: string; description?: string }>
  locations?: Array<{ name: string; description?: string }>
}

const elements = computed<ElementsType>(() => selectedProject.value?.scriptBreakdown?.elements || {})

// Track selected scene
const selectedSceneNumber = ref<number|null>(null)

// Tabs for filtering elements
const elementTabs = ['All', 'Cast', 'Props', 'Locations']
const activeTab = ref('All')

// Statuses for project status selection
const statuses = [
  { label: 'ACTIVE', value: 'ACTIVE' },
  { label: 'IN REVIEW', value: 'REVIEW' },
  { label: 'COMPLETED', value: 'COMPLETED' }
]

// Make status reactive to project selection
const selectedStatus = ref(selectedProject.value?.status || 'ACTIVE')

// Watch for project change and update status accordingly
watch(selectedProject, (newProject) => {
  selectedStatus.value = newProject?.status || 'ACTIVE'
})

// When status is changed, update the project object in-memory
function setStatus(status: string) {
  selectedStatus.value = status
  // Update the status in the projects array (in-memory only)
  const project = projects.find(p => p.title === selectedProjectTitle.value)
  if (project) project.status = status
}

// Helper: Get elements for a scene
function getSceneElements(scene) {
  if (!scene) return []
  let list: any[] = []
  if (activeTab.value === 'All' || activeTab.value === 'Cast') {
    list = list.concat(
      (scene.characters || []).map(name => ({
        type: 'Cast',
        name,
        description: (elements.value.characters || []).find(c => c.name === name)?.description || '',
        count: 1
      }))
    )
  }
  if (activeTab.value === 'All' || activeTab.value === 'Props') {
    list = list.concat(
      (scene.props || []).map(name => ({
        type: 'Props',
        name,
        description: '', // Add more details if available
        count: 1
      }))
    )
  }
  if (activeTab.value === 'All' || activeTab.value === 'Locations') {
    list = list.concat(
      scene.location
        ? [{
            type: 'Location',
            name: scene.location,
            description: '',
            count: 1
          }]
        : []
    )
  }
  return list
}

const filteredElements = computed(() => {
  if (!selectedSceneNumber.value) return []
  const scene = scenes.value.find(s => s.number === selectedSceneNumber.value)
  return getSceneElements(scene)
})

// Login form state
const email = ref('')
const password = ref('')
const error = ref('')

// Login function
function onLogin() {
  if (email.value && password.value) {
    projectStore.setLogin(true)
    projectStore.setUser({
      name: email.value.split('@')[0],
      role: 'Director',
      email: email.value,
    })
    router.push({ name: 'ScriptBreakdown' })
  } else {
    error.value = 'Please enter email and password'
  }
}

// Handler for New Project button
function onNewProjectButtonClick() {
  // Placeholder: Implement your logic here, e.g., open a modal or navigate
  alert('New Project button clicked!')
}
</script>
