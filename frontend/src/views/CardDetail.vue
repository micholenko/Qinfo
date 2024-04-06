<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Stats from '@/components/Stats.vue'
import Plotly from 'plotly.js-dist'
import InteractiveAnalysis from '@/components/InteractiveAnalysis.vue'

const studyStore = useStudyStore()
let studyId = useRoute().params.id
const cardId = useRoute().params.cardId
const cardName = studyStore.cards.cards.find((c) => c.id == cardId).text

onMounted(() => {
  fetch(`http://localhost:5000/studies/${studyId}/cards/${cardId}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      const cardBoxPlot = data['cardBoxPlot']
      const cardScatterPlot = data['cardScatterPlot']
      Plotly.newPlot('cardBoxPlot', cardBoxPlot)
      Plotly.newPlot('cardScatterPlot', cardScatterPlot)
    })
})
</script>

<template>
  <v-card style="margin: 15px; padding-left: 15px; min-height: 87vh;">
    <h2>{{ cardName }}</h2>
    <div style="display: flex; justify-content: center; align-items: center; height: 50%">
      <div id="cardBoxPlot" style="width: 50%; height: 50%"></div>
      <div id="cardScatterPlot" style="width: 50%; height: 50%"></div>
    </div>
    <InteractiveAnalysis :parentElement="'card'" />
  </v-card>
</template>
