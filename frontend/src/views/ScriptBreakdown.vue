<template>
  <div class="transition-all duration-300" :class="sidebarExpanded ? 'ml-64' : 'ml-16'">
    <!-- Header Section Start -->
    <div
      class="w-full relative bg-background-primary h-20 flex flex-row items-center justify-between py-[15px] pl-[19px] pr-[104px] box-border gap-0 text-left text-2xl text-white font-inter z-30 border-b border-gray-700"
      style="position: sticky; top: 0;"
    >
      <div class="flex flex-col items-start justify-start">
        <h1 class="relative leading-[28.8px] font-inter-bold">Script Analysis</h1>
      </div>
      <div class="flex flex-row items-center justify-start gap-4 text-sm text-text-secondary">
        <div class="w-60 rounded-lg bg-background-tertiary h-10 flex flex-row items-center justify-start py-0 px-4 box-border gap-2 shadow-md transition-all duration-200 focus-within:ring-2 focus-within:ring-secondary hover:shadow-lg border border-gray-600">
          <img class="w-5 h-5 object-cover" alt="" src="../assets/icon/Search Icon.svg" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search scenes, elements..."
            class="leading-[16.8px] bg-transparent outline-none text-white placeholder-text-muted w-full rounded-md transition-all duration-200 font-inter-regular"
          />
        </div>
        <div class="w-[100px] rounded-lg bg-gray-700 h-10 flex flex-row items-center justify-center gap-2 text-text-secondary cursor-pointer hover:bg-gray-600 transition-colors" @click="exportScenes">
          <img class="w-4 h-4" alt="" src="../assets/icon/download.svg" />
          <div class="leading-[16.8px] font-inter-medium">Export</div>
        </div>
        <div class="w-[120px] rounded-lg bg-secondary h-10 flex flex-row items-center justify-center gap-1 cursor-pointer text-black hover:bg-secondary-hover transition-colors" @click="goToNewProject">
          <img class="w-4 h-4 object-cover" alt="" src="../assets/icon/Plus Icon.svg" />
          <div class="leading-[16.8px] font-inter-semibold">New Project</div>
        </div>
      </div>
    </div>
    <!-- Header Section End -->

    <!-- Main Content -->
    <div class="bg-background-primary h-[calc(100vh-80px)] overflow-hidden">
      <div class="flex h-full">
        <!-- Script Panel Component -->
        <ScriptPanel
          :projects="projects"
          :selected-project-title="selectedProjectTitle"
          :selected-project="selectedProject"
          :scenes="scenes"
          :filtered-scenes="filteredScenes"
          :selected-scene-number="selectedSceneNumber"
          @project-change="onProjectChange"
          @scene-select="selectScene"
          @new-project="goToNewProject"
          @export-scenes="exportScenes"
          @jump-to-scene="jumpToSceneHandler"
        />

        <!-- Elements Panel Component -->
        <ElementsPanel
          :selected-scene-number="selectedSceneNumber"
          :selected-scene="selectedScene"
          :active-tab="activeTab"
          :element-tabs="elementTabs"
          :filtered-elements="filteredElements"
          @tab-change="activeTab = $event"
          @show-ai="showAI = true"
        />
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
import { ref, computed, watch, inject, onMounted } from 'vue'
import { useProjectStore } from '../stores/projectStore'
import { useRouter } from 'vue-router'
import ScriptPanel from '../components/ScriptPanel.vue'
import ElementsPanel from '../components/ElementsPanel.vue'
import AIChatPanel from '../components/AIChatPanel.vue'

// Inject sidebar state
const sidebarExpanded = inject('sidebarExpanded', ref(false))

const router = useRouter()
const projectStore = useProjectStore()

// Reactive state
const searchQuery = ref('')
const selectedProjectId = ref(projectStore.selectedProjectId || projectStore.projects[0]?.id || '')
const selectedSceneNumber = ref<number | null>(null)
const activeTab = ref('All')
const showAI = ref(false)
const analysisData = ref<any>(null)
const loading = ref(false)

// Element tabs for filtering
const elementTabs = ['All', 'Cast', 'Props', 'Locations']

// Computed properties
const projects = computed(() => projectStore.projects)

const selectedProject = computed(() => {
  if (selectedProjectId.value) {
    return projects.value.find(p => p.id === selectedProjectId.value)
  }
  return projects.value[0] // Fallback to first project
})

const scenes = computed(() => {
  if (analysisData.value?.script_breakdown?.scenes) {
    return analysisData.value.script_breakdown.scenes
  }
  return selectedProject.value?.scriptBreakdown?.scenes || []
})

const selectedScene = computed(() =>
  scenes.value.find(s => s.number === selectedSceneNumber.value)
)

const filteredScenes = computed(() => {
  if (!searchQuery.value.trim()) return scenes.value
  
  const query = searchQuery.value.trim().toLowerCase()
  return scenes.value.filter(scene =>
    scene.heading?.toLowerCase().includes(query) ||
    scene.notes?.toLowerCase().includes(query) ||
    scene.characters?.some(char => char.toLowerCase().includes(query)) ||
    scene.props?.some(prop => prop.toLowerCase().includes(query))
  )
})

const filteredElements = computed(() => {
  if (!selectedSceneNumber.value || !selectedScene.value) return []
  
  const scene = selectedScene.value
  let elements: any[] = []
  
  // Add characters
  if (activeTab.value === 'All' || activeTab.value === 'Cast') {
    elements = elements.concat(
      (scene.characters || []).map(name => ({
        type: 'Cast',
        name,
        description: getCharacterDescription(name),
        count: 1
      }))
    )
  }
  
  // Add props
  if (activeTab.value === 'All' || activeTab.value === 'Props') {
    elements = elements.concat(
      (scene.props || []).map(name => ({
        type: 'Props',
        name,
        description: '',
        count: 1
      }))
    )
  }
  
  // Add locations
  if (activeTab.value === 'All' || activeTab.value === 'Locations') {
    if (scene.location) {
      elements.push({
        type: 'Locations',
        name: scene.location,
        description: '',
        count: 1
      })
    }
  }
  
  return elements
})

// Helper functions
function getCharacterDescription(characterName: string): string {
  // You can expand this to get descriptions from project data
  const characterDescriptions: Record<string, string> = {
    'SARAH': '30s, determined woman, protagonist',
    'PARK RANGER': 'Middle-aged, experienced, warning about storm',
    'NURUL': 'Expectant mother, main character',
    'DR. AMIR': 'Experienced doctor',
    'MIDWIFE': 'Skilled healthcare professional',
    'HUSBAND': 'Supportive partner'
  }
  return characterDescriptions[characterName] || ''
}

function selectScene(sceneNumber: number) {
  selectedSceneNumber.value = sceneNumber
}

function onProjectChange(projectId: string) {
  selectedProjectId.value = projectId
  selectedSceneNumber.value = null
  projectStore.setSelectedProject(projectId)
  loadAnalysisData()
}

async function loadAnalysisData() {
  if (!selectedProjectId.value) return
  
  loading.value = true
  try {
    const data = await projectStore.getProjectAnalysis(selectedProjectId.value)
    analysisData.value = data
  } catch (error) {
    console.error('Failed to load analysis data:', error)
    // Fallback to project data if API fails
    const project = selectedProject.value
    if (project?.analysis_data) {
      analysisData.value = project.analysis_data
    }
  } finally {
    loading.value = false
  }
}

function goToNewProject() {
  router.push({ name: 'NewProject' })
}

function jumpToSceneHandler(sceneNumber: number) {
  if (sceneNumber) {
    selectScene(sceneNumber)
  }
}

function exportScenes() {
  if (!selectedProject.value || !scenes.value.length) {
    showNotification('No scenes to export', 'error')
    return
  }
  
  try {
    // Create CSV content
    const csvContent = generateSceneCSV(scenes.value, selectedProject.value.title)
    
    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `${selectedProject.value.title}_scenes.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    showNotification(`Exported ${scenes.value.length} scenes successfully!`, 'success')
  } catch (error) {
    showNotification('Failed to export scenes', 'error')
    console.error('Export error:', error)
  }
}

function showNotification(message: string, type: 'success' | 'error' = 'success') {
  // Simple notification implementation
  const notification = document.createElement('div')
  notification.className = `fixed top-4 right-4 z-50 px-4 py-3 rounded-lg text-white font-inter-medium transition-all duration-300 ${
    type === 'success' ? 'bg-green-600' : 'bg-red-600'
  }`
  notification.textContent = message
  document.body.appendChild(notification)
  
  setTimeout(() => {
    notification.style.opacity = '0'
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}

function generateSceneCSV(scenes: any[], projectTitle: string): string {
  const headers = [
    'Scene #', 
    'Heading', 
    'Location', 
    'Time of Day',
    'Characters', 
    'Character Count',
    'Props', 
    'Props Count',
    'Description',
    'Duration (Est.)'
  ]
  
  const rows = scenes.map(scene => [
    scene.number,
    `"${scene.heading || ''}"`,
    `"${scene.location || ''}"`,
    `"${scene.timeOfDay || 'DAY'}"`,
    `"${(scene.characters || []).join(', ')}"`,
    scene.characters?.length || 0,
    `"${(scene.props || []).join(', ')}"`,
    scene.props?.length || 0,
    `"${scene.notes || ''}"`,
    `"${scene.estimatedDuration || 'TBD'}"`,
  ])
  
  const totalScenes = scenes.length
  const totalCharacters = new Set(scenes.flatMap(s => s.characters || [])).size
  const totalProps = new Set(scenes.flatMap(s => s.props || [])).size
  const totalLocations = new Set(scenes.map(s => s.location).filter(Boolean)).size
  
  const csvContent = [
    `# Scene Breakdown Export - ${projectTitle}`,
    `# Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}`,
    `# Summary: ${totalScenes} scenes, ${totalCharacters} unique characters, ${totalProps} props, ${totalLocations} locations`,
    '',
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')
  
  return csvContent
}

// Watch for project changes
watch(selectedProject, (newProject) => {
  if (newProject) {
    projectStore.setSelectedProject(newProject.id)
  }
}, { immediate: true })

// Watch for store selectedProjectId changes (e.g., when navigating from Projects page)
watch(() => projectStore.selectedProjectId, (newId) => {
  if (newId && newId !== selectedProjectId.value) {
    selectedProjectId.value = newId
    loadAnalysisData()
  }
}, { immediate: true })

// Load analysis data when component mounts
onMounted(() => {
  if (selectedProjectId.value) {
    loadAnalysisData()
  }
})
</script>
