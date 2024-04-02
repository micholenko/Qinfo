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
      const card_detail = data
      Plotly.newPlot('card_detail', card_detail)
    })

  
})



</script>

<template>
  <v-card style="height: 85vh; margin: 15px">
    <h2>{{cardName}}</h2>
    <div id="card_detail" style="width: 100%; height: 50%"></div>
    <InteractiveAnalysis :parentElement="'card'"/> 
  </v-card>
</template>
