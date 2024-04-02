<script setup>
import { ref } from 'vue';
import * as d3 from 'd3';
import { defineProps } from 'vue';
import {useStudyStore} from '@/stores/study'
import {useRoute} from 'vue-router'
import Plotly from 'plotly.js-dist'
import { onMounted } from 'vue';
import Qtable from './Qtable.vue';

// get second param from route
const route = useRoute()
const props = defineProps(['parentElement']);
const store = useStudyStore()

let qsort = []


const selectedRound = ref( props.parentElement === 'round' ? route.params.roundId : null);
const selectedParticipant = ref( props.parentElement === 'participant' ? route.params.participantId : null);
const selectedCard = ref( props.parentElement === 'card' ? route.params.cardId : null);
const selectedPosition = ref(null);

const positions = store.positions

const drawQTable = ref(false)

const rows = ref(null)

const getPlot = (setFilters) => {
  if (setFilters.round !== null && setFilters.participant === null && setFilters.card === null && setFilters.position === null) {
    console.log('round default')
  }
  else if (setFilters.round === null && setFilters.participant !== null && setFilters.card === null && setFilters.position === null) {
    console.log('participant default')
  }
  else if (setFilters.round === null && setFilters.participant === null && setFilters.card !== null && setFilters.position === null) {
    console.log('card default')
  }
  else if (setFilters.round === null && setFilters.participant === null && setFilters.card === null && setFilters.position !== null) {
    console.log('position default')
  }
  else if (setFilters.round !== null && setFilters.participant !== null && setFilters.card === null && setFilters.position === null) {
    console.log('Qtable')
    console.log('rows', rows.value)
    const filtered = rows.value.filter((item) => item.round === parseInt(setFilters.round) && item.participant === parseInt(setFilters.participant))
    // create a list of list according to the distribution
    console.log('filtered:', filtered)
    console.log('positions:', positions)
    qsort = []
    positions.forEach((item) => {
      let column = filtered.filter((row) => row.position === item)
      column = column.map((row) => store.cards.cards.find((card) => card.id === row.card).text)
      qsort.push(column)
    })

    console.log('qsort:', qsort)
    

    drawQTable.value = true
  }
  else if (setFilters.round !== null && setFilters.participant === null && setFilters.card !== null && setFilters.position === null) {
    console.log('sorted scatter or simpler')
  }
  else if (setFilters.round !== null && setFilters.participant === null && setFilters.card === null && setFilters.position !== null) {
    console.log('dont know yet')
  }
  else if (setFilters.round === null && setFilters.participant !== null && setFilters.card !== null && setFilters.position === null) {
    console.log('line with scatter')
    const filtered = rows.value.filter((item) => item.participant === parseInt(setFilters.participant) && item.card === setFilters.card)
    // create scatter plot
    const trace = {
      x: filtered.map((item) => item.round),
      y: filtered.map((item) => item.position),
      mode: 'markers+lines',
      type: 'scatter'
    }
    const layout = {
      title: 'Participant vs Position',
      xaxis: {
        title: 'Round'
      },
      yaxis: {
        title: 'Position'
      }
    }
    Plotly.newPlot('plotlyChart', [trace], layout)    
  }
  else if (setFilters.round === null && setFilters.participant !== null && setFilters.card === null && setFilters.position !== null) {
    console.log('participant position')
  }
  else if (setFilters.round === null && setFilters.participant === null && setFilters.card !== null && setFilters.position !== null) {
    console.log('card position')
  }
  else if (setFilters.round !== null && setFilters.participant !== null && setFilters.card !== null && setFilters.position === null) {
    console.log('round participant card')
  }
  else if (setFilters.round !== null && setFilters.participant !== null && setFilters.card === null && setFilters.position !== null) {
    console.log('round participant position')
  }
  else if (setFilters.round !== null && setFilters.participant === null && setFilters.card !== null && setFilters.position !== null) {
    console.log('round card position')
  }
  else if (setFilters.round === null && setFilters.participant !== null && setFilters.card !== null && setFilters.position !== null) {
    console.log('participant card position')
  }
  else if (setFilters.round !== null && setFilters.participant !== null && setFilters.card !== null && setFilters.position !== null) {
    console.log('round participant card position')
  }
  else {
    console.log('no filters')
  }
}




const updatePlot = () => {
  drawQTable.value = false
  Plotly.purge('plotlyChart')

  const filterCount = [selectedRound.value, selectedParticipant.value, selectedCard.value, selectedPosition.value].filter((item) => item !== null).length
  const setFilters = {
    round: selectedRound.value,
    participant: selectedParticipant.value,
    card: selectedCard.value,
    position: selectedPosition.value
  }
  getPlot(setFilters)
}

const clearFilters = () => {
  // all except one in props
  if (props.parentElement === 'round') {
    selectedParticipant.value = null
    selectedCard.value = null
    selectedPosition.value = null
  }
  else if (props.parentElement === 'participant') {
    selectedRound.value = null
    selectedCard.value = null
    selectedPosition.value = null
  }
  else if (props.parentElement === 'card') {
    selectedRound.value = null
    selectedParticipant.value = null
    selectedPosition.value = null
  }
  else {
    selectedRound.value = null
    selectedParticipant.value = null
    selectedCard.value = null
  }
}


onMounted(() => {
  const studyId = useRoute().params.id
  fetch(`http://localhost:5000/studies/${studyId}/data`)
    .then((response) => response.json())
    .then((data) => {
      rows.value = data

    })
})
</script>


<template>
    <div style="display: flex; justify-content: center; align-items: center; width: 50%">
      <v-select v-if="props.parentElement !== 'round'"
        v-model="selectedRound"
        :items="store.rounds"
        label="Round"
        variant="outlined"
        clearable
        v-on:update:model-value="updatePlot"
      >
      </v-select>
      <!-- conbobox -->
      <v-select
        v-if="props.parentElement !== 'participant'"
        v-model="selectedParticipant"
        :items="store.participants"
        item-title="name"
        item-value="id"
        label="Participant"
        variant="outlined"
        clearable
        v-on:update:model-value="updatePlot"
      >
      </v-select>
      <!-- combobox -->
      <v-select
        v-if="props.parentElement !== 'card'"
        v-model="selectedCard"
        :items="store.cards.cards"
        item-title="text"
        item-value="id"
        label="Card"
        variant="outlined"
        clearable
        v-on:update:model-value="updatePlot"
      ></v-select>
      <v-select
        v-model="selectedPosition"
        :items="store.positions"
        label="Position"
        variant="outlined"
        clearable
        v-on:update:model-value="updatePlot"
      >
      </v-select>
      <!-- <v-switch v-on:click="switch3dFunc" color="primary" label="3d" hide-details></v-switch> -->
      <v-btn v-on:click="switchAxisFunc">Switch Axis</v-btn>
  
      <!-- clear all filters -->
      <v-btn v-on:click="clearFilters">Clear Filters</v-btn>
    </div>
    <!-- plotly -->
    <!-- <div v-if="filterCount === 3">
      <div v-if="dataPointExists">
        <v-table>
          <thead>
            <tr>
              <th>Round</th>
              <th>Participant</th>
              <th>Card</th>
              <th>Position</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in showListData" :key="item.id">
              <td>{{ item.round }}</td>
              <td>{{ item.participant }}</td>
              <td>{{ store.cards.cards.find((card) => card.id === item.card).text }}</td>
              <td>{{ item.position }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>
      <div v-else>
        <v-icon>mdi-close</v-icon>
        no, this data point does not exist
      </div>
    </div>
    <div v-else-if="filterCount === 4">
      <div v-if="dataPointExists">
        <v-icon>mdi-check</v-icon>
        This data point exists
      </div>
      <div v-else>
        <v-icon>mdi-close</v-icon>
        This data point does not exist
      </div>
    </div> -->
    <!-- style hidden based on filter count -->
    <!-- div center horizontally -->
    <!-- render ComponentToRender -->


    
    <div id="plotlyChart"></div>

    <div v-if = "drawQTable">
      <Qtable :distribution="store.distribution" 
      :qsort="qsort" id="q-table" />
    </div>
  </template>