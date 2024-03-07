
<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import plotly from 'plotly.js-dist'

import { useStudyStore } from '@/stores/study'


const createPlots = async (data) => {
  plotly.newPlot('correlations_scatter', data.scatter)
  plotly.newPlot('correlations_histogram', data.histogram)
}

const store = useStudyStore()
console.log('store:', store.users)


onMounted(async () => {
  const id = store.study.id
  try {
    const response = await fetch(`http://localhost:5000/studies/${id}/user_correlations`)
    const data = await response.json()
    await createPlots(data)
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <v-container v-if="!loading">
    <div id="correlations_scatter"></div>
    <div id="correlations_histogram"></div>
  </v-container>
</template>
