<script setup>
import { onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import InteractiveAnalysis from '@/components/InteractiveAnalysis.vue'

const studyStore = useStudyStore()
let studyId = useRoute().params.id
const roundId = useRoute().params.roundId

// fetch matrix
onMounted(() => {
  fetch(`http://localhost:5000/rounds/${roundId}/matrix`)
    .then((response) => response.json())
    .then((data) => {
      const corr_matrix = data
      console.log('data received:', corr_matrix)
      Plotly.newPlot('corr_matrix', corr_matrix)
    })
  fetch(`http://localhost:5000/studies/${studyId}/rounds/${roundId}`)
    .then((response) => response.json())
    .then((data) => {
      const round_scatter = data
      console.log('data received:', round_scatter)
      Plotly.newPlot('round_scatter', round_scatter)
    })
})
</script>

<template>
  <v-card style="margin: 15px; padding-left: 15px; min-height: 87vh;">
    <h2>Round {{ roundId }}</h2>
    <div style="display: flex; justify-content: center; align-items: center; height: 700px">
      <div id="corr_matrix" style="width: 50%; height: 100%"></div>
      <div id="round_scatter" style="width: 50%; height: 100%"></div>
    </div>
    <InteractiveAnalysis :parentElement="'round'"/>
  </v-card>
</template>
