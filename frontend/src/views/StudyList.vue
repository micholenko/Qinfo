<script setup>

import axios from 'axios'
import { ref, onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useRouter } from 'vue-router'
import { useStudyStore } from '@/stores/study'

const apiResponse = ref([])
const plotlyChart = ref(null)

const studyStore = useStudyStore()
const router = useRouter()

const headers = [
  { title: 'Title', key: 'title' },
  { title: 'Question', key: 'question'},
  { title: 'Created', key: 'created_time' },
  { title: 'Submit Date', key: 'submit_time' },
  { title: 'Status', key: 'status' }
]

const sortBy = [
  {
    key: 'created',
    order: 'desc'
  }
]

const plotChart = () => {
  Plotly.newPlot(
    plotlyChart.value,
    [
      {
        x: [1, 2, 3, 4],
        y: [10, 11, 12, 13],
        type: 'scatter'
      }
    ],
    {
      margin: { t: 0 }
    }
  )
}

const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/studies')
    // Update the reactive variable with the API response
    apiResponse.value = response.data
    console.log('apiResponse:', apiResponse.value)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const onClick = (_, row) => {
  const id = row.item.id
  router.push(`/study/${id}`)
}

// change the color of the row when the mouse is over it
const mouseOver = (event) => {
  event.target.parentNode.classList.add('bg-blue-grey-lighten-4')
}

const mouseOut = (event) => {
  event.target.parentNode.classList.remove('bg-blue-grey-lighten-4')
}

onMounted(() => {
  studyStore.study.id = null
  fetchData()
  // plotChart()
})
</script>

<template>
  <v-container class="d-flex justify-center mt-16">
    <v-sheet elevation="4" class="rounded-lg w-75">
      <v-container>
        <h1>Studies</h1>
        <v-divider></v-divider>
        <v-data-table
          :headers="headers"
          :items="apiResponse"
          :sort-by="sortBy"
          item-key="title"
          class="elevation-1"
          @click:row="onClick"
          @mouseover:row="mouseOver"
          @mouseout:row="mouseOut"
        ></v-data-table>
      </v-container>
    </v-sheet>
    <!-- show plot -->
    <!-- <div ref="plotlyChart"></div> -->
  </v-container>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
