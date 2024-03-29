<script setup>
import { onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Stats from '@/components/Stats.vue'

const studyStore = useStudyStore()
let studyId = useRoute().params.id
const participantId = useRoute().params.participantId
const participantName = studyStore.participants.find((p) => p.id == participantId).name

console.log(studyStore)
// let participantName = studyStore.participants.find((p) => p.id === participantId).name

onMounted(() => {
  fetch(`http://localhost:5000/studies/${studyId}/user_details?user_id=${participantId}`)
    .then((response) => response.json())
    .then((data) => {
      const correlation_matrix = data
      Plotly.newPlot('corr_matrix', correlation_matrix)
    })
})
</script>

<template>
  <v-card style="height: 85vh; margin: 15px">
    <h2>{{participantName}}</h2>
    <div id="corr_matrix" style="width: 30%;"></div>
    <div>
      <Stats :participantId="participantId" />
    </div>
  </v-card>
</template>
