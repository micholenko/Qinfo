<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Plotly from 'plotly.js-dist'


const studyStore = useStudyStore()
let studyId = useRoute().params.id

console.log(studyStore)

onMounted(() => {
  fetch(`http://localhost:5000/studies/${studyId}/rounds_stats`)
    .then((response) => response.json())
    .then((data) => {
      const rounds = data
      console.log('rounds:', rounds)
      Plotly.newPlot('rounds-scatter', rounds)
    })
})


</script>

<template>
  <v-card style="height: 85vh; margin: 15px; padding-left: 15px;">
    <div style="display: flex; justify-content: start; align-items: start; height">
      <div>
      
        <h2>Rounds:</h2>
        <v-virtual-scroll :items="studyStore.rounds" :item-height="40" width="100%">
          <template v-slot:default="{ item }">
            <v-list-item
            :key="item  "
            :to="`/study/${studyId}/rounds/${item}`"
            >
            Round {{ item}}
          </v-list-item>
        </template>
      </v-virtual-scroll>

    </div>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: start; height: 100%; width: 80%">
      <h2>Mean and standard deviation of rounds</h2>
      <div id="rounds-scatter" style="width: 100%; height: 100%"></div>
    </div>
  </div>
  </v-card>    
</template>
