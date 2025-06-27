export interface Scene {
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
}

export interface Project {
  title: string
  genre: string
  status: string
  statusColor: string
  budget: string
  dueDate: string
  team: string
  scriptBreakdown?: {
    scenes: Scene[]
    // ...other breakdown fields
  }
}