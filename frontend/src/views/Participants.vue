<script setup>
import { onMounted, ref } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import router from '@/router'

const studyStore = useStudyStore()
let studyId = useRoute().params.id

let eucDistPlot = null
let pcaPlot = null

const highlightUser = {
  mode: 'markers',
  marker: {
    size: 40,
    color: 'rgba(255, 182, 193, .9)'
  }
}

const mouseOverUser = (userId) => {
  const pointIndex = eucDistPlot.data[0].customdata.findIndex((id) => id[0] === userId)
  eucDistPlot.data[0].selectedpoints = [pointIndex]

  // highlight only the selected user
  Plotly.restyle(
    'euclidean_distance',
    {
      mode: 'markers'
    },
    [0]
  )
}

const mouseLeaveUser = () => {
  eucDistPlot.data[0].selectedpoints = null
  Plotly.restyle(
    'euclidean_distance',
    {
      mode: 'markers'
    },
    [0]
  )
}

onMounted(() => {
  fetch(`http://localhost:5000/studies/${studyId}/average_euclidean_distance`)
    .then((response) => response.json())
    .then((data) => {
      const euclidean_distance = data
      Plotly.newPlot('euclidean_distance', euclidean_distance)
      eucDistPlot = document.getElementById('euclidean_distance')
      eucDistPlot.on('plotly_click', function (data) {
        const point = data.points[0]
        console.log(point)
        router.push({ path: `/study/${studyId}/participants/${point.customdata[0]}` })
      })
    })
  fetch(`http://localhost:5000/studies/${studyId}/users_pca`)
    .then((response) => response.json())
    .then((data) => {
      const pca = data
      Plotly.newPlot('pca', pca)
      pcaPlot = document.getElementById('pca')
      pcaPlot.on('plotly_click', function (data) {
        const point = data.points[0]
        console.log(point)
        router.push({ path: `/study/${studyId}/participants/${point.customdata[0]}` })
      })
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
        max-width: 250px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: start;
        padding-left: 10px;
        margin-right: 20px;
      "
    >
      <h2>Participants:</h2>
      <v-virtual-scroll :items="studyStore.participants" :item-height="40" width="100%">
        <template v-slot:default="{ item }">
          <v-list-item
            :key="item.id"
            :to="`/study/${studyId}/participants/${item.id}`"
            @mouseover="mouseOverUser(item.id)"
            @mouseleave="mouseLeaveUser"
          >
            {{ item.name }}
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
        width: 25%;
      "
    >
      <h2>User consistency between rounds</h2>
      <div id="euclidean_distance" style="max-width: 400px; height: 100%"></div>
    </div>
    <!-- 30 and 70% of flex -->
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: start; height: 100%; width: 50%">
      <h2>PCA Similariy Clustering</h2>
      <div id="pca" style="width: 100%; height: 100%"></div>
    </div>
    <!-- list users -->
  </v-card>
</template>
