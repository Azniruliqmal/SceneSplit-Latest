<template>
  <div class="w-1/2 bg-background-secondary border-r border-gray-700 flex flex-col">
    <!-- Script Header - Sticky -->
    <div class="flex-shrink-0 p-6 border-b border-gray-700 bg-background-secondary sticky top-0 z-10">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-white text-lg font-inter-bold mb-1">Script: {{ selectedProject?.title || 'No Project Selected' }}</h2>
          <p class="text-text-muted text-sm font-inter-regular">Scene 1-{{ scenes.length }} Analysis</p>
        </div>
        <div class="flex gap-2">
          <button
            class="bg-secondary text-black px-4 py-2 rounded-lg font-inter-semibold text-sm hover:bg-secondary-hover transition-colors"
          >
            All Scenes
          </button>
          <button class="text-text-secondary hover:text-white transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Project Selector -->
      <div class="flex items-center gap-4 mb-4">
        <label class="text-white font-inter-medium text-sm">Script:</label>
        <select
          :model-value="selectedProjectTitle"
          @update:model-value="$emit('project-change', $event)"
          class="bg-background-tertiary text-secondary font-inter-semibold rounded-lg px-4 py-2 focus:outline-none border border-gray-600 focus:border-secondary transition-colors"
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
        
        <!-- Status Badges -->
        <div class="flex gap-2">
          <span
            v-if="selectedProject"
            :class="['text-xs font-inter-bold px-3 py-1 rounded whitespace-nowrap', selectedProject.statusColor]"
          >
            {{ selectedProject.status }}
          </span>
        </div>
      </div>
    </div>

    <!-- Scenes List - Scrollable -->
    <div class="flex-1 overflow-y-auto p-6">
      <div
        v-for="scene in filteredScenes"
        :key="scene.number"
        :class="[
          'mb-4 rounded-lg bg-background-tertiary p-6 cursor-pointer transition-all duration-200 border-2',
          selectedSceneNumber === scene.number
            ? 'border-secondary shadow-lg'
            : 'border-transparent hover:border-gray-600'
        ]"
        @click="$emit('scene-select', scene.number)"
      >
        <!-- Scene Header -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-3">
            <span class="bg-secondary text-black font-inter-bold rounded-full w-8 h-8 flex items-center justify-center text-sm">
              {{ scene.number }}
            </span>
            <span class="font-inter-bold text-white text-base">{{ scene.heading }}</span>
          </div>
          <button class="text-text-muted hover:text-secondary transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </button>
        </div>
        
        <!-- Scene Description -->
        <div class="text-text-muted text-sm mb-3 font-inter-regular">{{ scene.notes }}</div>
        
        <!-- Scene Dialogue -->
        <div v-if="scene.dialogues && scene.dialogues.length" class="mb-3">
          <div v-for="(dialogue, idx) in scene.dialogues.slice(0, 2)" :key="idx" class="mb-2">
            <div class="text-secondary font-inter-semibold text-sm mb-1">{{ dialogue.character }}</div>
            <div class="text-white text-sm font-inter-regular">{{ dialogue.text }}</div>
          </div>
          <div v-if="scene.dialogues.length > 2" class="text-text-muted text-xs font-inter-regular">
            +{{ scene.dialogues.length - 2 }} more dialogues...
          </div>
        </div>
        
        <!-- Scene Elements Summary -->
        <div class="flex flex-wrap gap-2 text-xs">
          <div v-if="scene.characters && scene.characters.length" class="text-text-muted font-inter-regular">
            <span class="font-inter-semibold text-white">Characters:</span> {{ scene.characters.join(', ') }}
          </div>
          <div v-if="scene.props && scene.props.length" class="text-text-muted font-inter-regular">
            <span class="font-inter-semibold text-white">Props:</span> {{ scene.props.join(', ') }}
          </div>
        </div>
      </div>
      
      <!-- No Scenes Message -->
      <div v-if="!filteredScenes.length" class="text-center py-12">
        <div class="text-text-muted font-inter-regular mb-4">No scenes found for this project.</div>
        <button
          @click="$emit('new-project')"
          class="bg-secondary text-black px-4 py-2 rounded-lg font-inter-semibold hover:bg-secondary-hover transition-colors"
        >
          Upload New Script
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Props
const props = defineProps<{
  projects: any[]
  selectedProjectTitle: string
  selectedProject: any
  scenes: any[]
  filteredScenes: any[]
  selectedSceneNumber: number | null
}>()

// Emits
const emit = defineEmits<{
  'project-change': [value: string]
  'scene-select': [sceneNumber: number]
  'new-project': []
}>()
</script>
