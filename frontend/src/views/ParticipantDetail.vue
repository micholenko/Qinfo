<script setup>
import { onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Stats from '@/components/Stats.vue'
import InteractiveAnalysis from '@/components/InteractiveAnalysis.vue'

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
  fetch(`http://localhost:5000/studies/${studyId}/user_card_stats?user_id=${participantId}`)
    .then((response) => response.json())
    .then((data) => {
      const user_cards = data
      Plotly.newPlot('user_cards', user_cards)
    })

})
</script>

<template>
  <v-card style="margin: 15px; padding-left: 15px; min-height: 87vh;">
    <h2>{{participantName}}</h2>
    <div style="display: flex; justify-content: center; height: 30%">
      <div id="corr_matrix" style="width: 100%; height: 100%"></div>
      <div id="user_cards" style="width: 100%; height: 100%"></div>
    </div>

    <div>
      <InteractiveAnalysis :parentElement="'participant'"/>
    </div>
  </v-card>
</template>
