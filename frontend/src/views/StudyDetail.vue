<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import Plotly from 'plotly.js-dist'
import Qtable from '@/components/Qtable.vue'
import CorrelationMatrix from '@/components/CorrelationMatrix.vue'
import Factors from '@/components/Factors.vue'
import CompositeQsorts from '@/components/CompositeQsorts.vue'
import Participants from '@/components/Participants.vue'

import { useRoute } from 'vue-router'


const studyData = ref({ rounds: { count: 0 } })
const tab = ref(null)
const selectedUser = ref(null)
const selectedRound = ref(null)
const responses = ref(null)
const selectedResponse = ref(null)
const cards = ref(null)
const distribution = ref([])
const loading = ref(true)
const route = useRoute()
const studyId = route.params.id
const qSetObject = ref(null)
const cardsFinal = ref(null)
const plotlyChart = ref(null)


const fetchQset = async (qsetId) => {
  let ret = await fetch(`http://localhost:5000/qsets/${qsetId}`)
  const data = await ret.json()
  console.log(data)
  qSetObject.value = data
}


const fetchData = async () => {
  let ret = await fetch(`http://localhost:5000/studies/${studyId}`)
  const data = await ret.json()
  studyData.value = data
  console.log('studyData:', studyData.value)
  selectedRound.value = data.rounds.ids[0]
  distribution.value = data.distribution

  // add param to request
  await fetchQset(data.q_set_id)
  loading.value = false
}



onMounted(() => {
  fetchData()
})
</script>

<template>
  <v-container class="d-flex justify-center mt-16">
    <v-sheet elevation="4" class="rounded-lg w-75">
      <!-- render if not loading -->
      <v-container v-if="!loading">
        <h1>{{ studyData.title }}</h1>
        <h2>Q: {{ studyData.question }}</h2>
        <p>
          {{ studyData.description }}
        </p>
        <v-divider></v-divider>

        <v-expansion-panels multiple>
          <v-expansion-panel>
            <v-expansion-panel-title> Participants </v-expansion-panel-title>
            <v-expansion-panel-text>
              <Participants :qSet="qSetObject.cards" :distribution="distribution" :rounds="studyData.rounds.ids"/>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title> Correlation matrix </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container>
                <CorrelationMatrix />
              </v-container>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title> Factors </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container>
                <Factors />
              </v-container>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title> Composite QSorts </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container>
                <CompositeQsorts :qset="qSetObject.cards" :distribution="distribution"/>

              </v-container>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-container>
    </v-sheet>
  </v-container>
</template>
