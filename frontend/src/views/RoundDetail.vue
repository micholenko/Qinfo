<script setup>
import { onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'

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
})
</script>

<template>
  <v-card style="height: 85vh; margin: 15px">
    <h2>Round {{ roundId }}</h2>
    <div id="corr_matrix" style="width: 100%; height: 100%"></div>
  </v-card>
</template>
