<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'

const factors = ref([])
const eigen = ref([])
const headers = [
  {title: 'user', key:'0'},
  {title: 'Factor 1', key:'1'},
  {title: 'Factor 2', key:'2'},
  {title: 'Factor 3', key:'3'},
  {title: 'Factor 4', key:'4'},
  {title: 'Factor 5', key:'5'},

]

const fetchFactors = async (round_id) => {
  const response = await fetch('http://localhost:5000/rounds/' + round_id + '/factors')
  const data = await response.json()
  factors.value = data.loadings
  eigen.value = data.eigen
}

onMounted(() => {
  const round_id = 1
  fetchFactors(round_id)
})


</script>

<template>
    <v-data-table
      :headers="headers"
      :items="factors"
      :items-per-page="20"
      class="elevation-1"
    />
    <v-data-table
      :headers="headers"
      :items="eigen"
      :items-per-page="20"
      class="elevation-1"
    />
</template>