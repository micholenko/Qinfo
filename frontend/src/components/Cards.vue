<script setup>
import { onMounted, ref } from 'vue'
import plotly from 'plotly.js-dist'



import { useStudyStore } from '@/stores/study';

const store = useStudyStore()
console.log('store:', store)


onMounted( async () => {
  let data = null
  try {
    const response = await fetch(`http://localhost:5000/studies/${store.study.id}/cards_stats`)
    data = await response.json()
    console.log('data:', data)
  } catch (error) {
    console.error(error)
  }

  plotly.newPlot('cards-box', data)

})
</script>

<template>
  <v-container>
    <!-- list all cards -->
    <div id="cards-box"></div>
    <v-list>
      <v-list-item
        v-for="(card, index) in store.cards.cards"
        :key="card.id"
      >
      <v-list-item-title>{{ index + 1 }}. {{ card.text }}</v-list-item-title>
      </v-list-item>
    </v-list>


  </v-container>
</template>
