<script setup>
import { onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import router from '@/router'
import { fillStudyStore } from '@/helpers'


const studyStore = useStudyStore()
let studyId = useRoute().params.id

let cardsScatterPlot = null

const mouseOverCard = (cardId) => {
  const pointIndex = cards.data.findIndex((card) => card.id === cardId)
  cards.data[pointIndex].selectedpoints = [pointIndex]

  // highlight only the selected user
  Plotly.restyle(
    'cards-scatter',
    {
      mode: 'markers'
    },
    [0]
  )
}

const mouseLeaveCard = () => {
  cards.data.forEach((card) => {
    card.selectedpoints = null
  })
  Plotly.restyle(
    'cards-scatter',
    {
      mode: 'markers'
    },
    [0]
  )
}

onMounted(() => {
  if (studyStore.study.id === null) {
    fillStudyStore(studyId)
  }
  fetch(`http://localhost:5000/studies/${studyId}/card_stats2`)
    .then((response) => response.json())
    .then((data) => {
      const cards = data
      console.log('cards:', cards)
      Plotly.newPlot('cards-scatter', cards)
      cardsScatterPlot = document.getElementById('cards-scatter')
      cardsScatterPlot.on('plotly_click', function (data) {
        const point = data.points[0]
        console.log(point)
        router.push({ path: `/study/${studyId}/cards/${point.customdata[0]}` })
      })
    })
  fetch(`http://localhost:5000/studies/${studyId}/cards_stats`)
    .then((response) => response.json())
    .then((data) => {
      const cards = data
      Plotly.newPlot('cards-box', cards)
    })
})
</script>

<template>
  <v-card
    style="display: flex; justify-content: left; align-items: center; height: 87vh; margin: 15px"
  >
    <div
      style="
        height: 100%;
        width: 20%;
        max-width: 400px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: start;
        padding-left: 10px;
        margin-right: 20px;
      "
    >
      <h2>Cards:</h2>
      <v-virtual-scroll :items="studyStore.cards.cards" :item-height="40" width="100%">
        <template v-slot:default="{ item }">
          <v-list-item
            :key="item.id"
            :to="`/study/${studyId}/cards/${item.id}`"
            @mouseover="mouseOverCard(item.id)"
            @mouseleave="mouseLeaveCard"
          >
            {{ item.text }}
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </div>
    <div
      style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: start;
        height: 100%;
        width: 80%;
      "
    >
      <h2>Mean and standard deviation of cards</h2>
      <div id="cards-scatter" style="width: 100%; height: 100%"></div>
    </div>
  </v-card>
  <!-- <div id="cards-box" style="width: 100%; height: 100%"></div> -->
</template>
