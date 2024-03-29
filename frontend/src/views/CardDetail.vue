<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Stats from '@/components/Stats.vue'
import Plotly from 'plotly.js-dist'

const studyStore = useStudyStore()
console.log(studyStore)
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
    <div id="card_detail" style="width: 100%; height: 100%"></div>
    <!-- <div id="corr_matrix" style="width: 30%;"></div>
    <div>
      <Stats :participantId="participantId" />
    </div> -->
  </v-card>
</template>
