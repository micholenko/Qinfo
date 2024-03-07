<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'

const headers = [
  {title: 'User', key:'0'},
  {title: 'Factor 1', key:'1'},
  {title: 'Factor 2', key:'2'},
  {title: 'Factor 3', key:'3'},
  {title: 'Factor 4', key:'4'},
  {title: 'Factor 5', key:'5'},
  {title: 'Factor 6', key:'6'},
  {title: 'Factor 7', key:'7'},
  {title: 'Factor 8', key:'8'},
]

const table = ref([])
const loading = ref(true)

const fetchData = async (round_id) => {
  let ret = await fetch(`http://localhost:5000/rounds/${round_id}/rotated_factors`)
  const data = await ret.json()
  // append user to each row
  data.forEach((row, i) => {
    row.unshift(i)
  })
  table.value = data
}

onMounted(async () => {
  const round_id = 1
  await fetchData(round_id)
  loading.value = false
})

</script>

<template>
  <v-container v-if="!loading">
    <!-- text vuetify component -->
    <div class="text-h6">
      Rotated factors with Varimax
    </div>
    
    <v-data-table
    :headers="headers"
    :items="table"
    :items-per-page="20"
    class="elevation-1"
    />
  </v-container>
</template>