<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'

let studyId = useRoute().params.id

const studyStore = useStudyStore()

const studyData = ref(null)
const loading = ref(true)


const fetchUsers = async (studyId) => {
  const response = await fetch(`http://localhost:5000/users?studyId=${studyId}`)
  const data = await response.json()
  studyStore.participants = data
  console.log('studyStore.participants:', studyStore.participants)
}

const fetchQset = async (qsetId) => {
  let ret = await fetch(`http://localhost:5000/qsets/${qsetId}`)
  const data = await ret.json()
  console.log(data)
  studyStore.cards = data
}


const fetchData = async () => {
  let ret = await fetch(`http://localhost:5000/studies/${studyId}`)
  const data = await ret.json()
  studyData.value = data

  await fetchUsers(studyId)
  await fetchQset(data.qset_id)
  studyStore.distribution = data.distribution
  studyStore.positions = data.col_values
  studyStore.rounds = data.rounds.ids
  loading.value = false
}

onMounted(() => {
  fetchData()
  studyStore.study.id = studyId
})
</script>

<template>

  <v-card
    style="height: 87vh; margin: 15px"
  >
  <div v-if="loading" style="display: flex; justify-content: center; align-items: center; height: 100%">
    <v-progress-circular  indeterminate color="primary"
    ></v-progress-circular>
  </div>
  <div v-else
  style="display: flex; justify-content: left; align-items: center; "
  >
    <h1>Study: {{ studyData.title }}</h1>
  </div>
  
    <!-- <h1>Study: {{ studyData.title }}</h1> -->
  </v-card>
</template>
