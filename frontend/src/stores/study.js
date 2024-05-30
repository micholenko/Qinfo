import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStudyStore = defineStore('study', () => {
  const study = ref({
    id: null,
    title: '',
    description: '',
    question: '',
    created_time: '',
    cards: [],
    participants: [],
    rounds: [],
    positions: [],
    distributions: [],
  })
  return {
    study,
  }
})
