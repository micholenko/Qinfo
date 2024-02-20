<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import Plotly from 'plotly.js-dist'
import Qtable from '@/components/Qtable.vue'
import CorrelationMatrix from '@/components/CorrelationMatrix.vue'
import Factors from '@/components/Factors.vue'

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
const qSet = ref(null)
const cardsFinal = ref(null)
const plotlyChart = ref(null)

const plotChart = () => {
  const data = [
    {
      z: [
        [1, 20, 30],
        [20, 1, 60],
        [30, 60, 1]
      ],
      type: 'heatmap'
    }
  ]
  const layout = {
    title: 'Heatmap'
  }
  const config = {
    responsive: true
  }
  Plotly.newPlot(plotlyChart.value, data, layout, config)
}

const fetchRound = async (round) => {
  let ret = await fetch(`http://localhost:5000/responses?round=${round}`)
  const data = await ret.json()
  responses.value = data
  console.log('responses:', responses.value)
}

const fetchResponse = async (response_id) => {
  let ret = await fetch(`http://localhost:5000/responses/${response_id}/cards`)
  const data = await ret.json()
  cards.value = data
}

const fetchQset = async (qsetId) => {
  let ret = await fetch(`http://localhost:5000/qsets/${qsetId}`)
  const data = await ret.json()
  console.log(data)
  qSet.value = data
}

const updateResponse = async (response_id) => {
  await fetchResponse(response_id)
  fillQTable()
}

const fetchData = async () => {
  let ret = await fetch(`http://localhost:5000/studies/${studyId}`)
  const data = await ret.json()
  studyData.value = data
  selectedRound.value = data.rounds.ids[0]
  distribution.value = data.distribution

  // add param to request
  await fetchQset(data.q_set_id)
  await fetchRound(selectedRound.value)
  await fetchResponse(responses.value[0].id)
  fillQTable()
  loading.value = false
}

const fillQTable = () => {
  for (let card of cards.value) {
    card['text'] = qSet.value.cards.find((c) => c.id === card.id)['text']
  }
  cardsFinal.value = cards.value 
  console.log('cardsFinal:', cardsFinal.value) 
}

onMounted(() => {
  fetchData()
  // plotChart();
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
              <v-tabs v-model="tab" bg-color="secondary">
                <!-- studyData.rounds is a number -->
                <v-tab
                  v-for="round in studyData.rounds.count"
                  :key="round"
                  @click="selectedRound = round"
                >
                  Round {{ round }}
                </v-tab>
              </v-tabs>
              <v-window v-model="tab">
                <v-window-item value="one">
                  <v-menu>
                    <template v-slot:activator="{ props }">
                      <v-btn color="primary" v-bind="props">
                        {{ selectedUser ? selectedUser : 'Select User' }}
                      </v-btn>
                    </template>
                    <v-list>
                      <v-list-item
                        v-for="response in responses"
                        :key="response.respondent_id"
                        @click="updateResponse(response.id)"
                      >
                        <v-list-item-title>{{ response.user }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                  <v-container>
                    <Qtable :distribution="distribution" :cardsFinal="cardsFinal" />
                  </v-container>
                </v-window-item>

                <v-window-item value="two"> Two </v-window-item>

                <v-window-item value="three"> Three </v-window-item>
              </v-window>
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
              </v-container>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-container>
    </v-sheet>
  </v-container>
</template>
