import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStudyStore = defineStore('study', () => {
  const study = ref({
    id: null,
    cards: [],
  })
  return {
    study,
  }
})
