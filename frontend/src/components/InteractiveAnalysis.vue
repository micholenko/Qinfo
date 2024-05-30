<script setup>
import { ref } from 'vue'
import * as d3 from 'd3'
import { defineProps } from 'vue'
import { useStudyStore } from '@/stores/study'
import { useRoute } from 'vue-router'
import Plotly, { list } from 'plotly.js-dist'
import { onMounted } from 'vue'
import Qtable from './Qtable.vue'

// get second param from route
const route = useRoute()
const props = defineProps(['parentElement'])
const store = useStudyStore()

let qsort = []

const selectedRound = ref(props.parentElement === 'round' ? route.params.roundId : null)
const selectedParticipant = ref(
  props.parentElement === 'participant' ? route.params.participantId : null
)
const selectedCard = ref(props.parentElement === 'card' ? route.params.cardId : null)
const selectedPosition = ref(null)

const positions = store.positions

const drawQTable = ref(false)

const rows = ref(null)
const highlight = ref(null)
const listData = ref(null)

const getQSort = (filtered) => {
  qsort = []
  console.log('filtered', filtered)
  positions.forEach((item) => {
    let column = filtered.filter((row) => row.position === item)
    column = column.map((row) => store.cards.cards.find((card) => card.id === row.card).text)
    qsort.push(column)
  })

  return qsort
}

const getPlot = (setFilters) => {
  highlight.value = null
  listData.value = null
  if (setFilters.round !== null) {
    setFilters.round = parseInt(setFilters.round)
  }
  if (setFilters.participant !== null) {
    setFilters.participant = parseInt(setFilters.participant)
  }
  if (setFilters.card !== null) {
    setFilters.card = parseInt(setFilters.card)
  }
  if (setFilters.position !== null) {
    setFilters.position = parseInt(setFilters.position)
  }

  if (
    setFilters.round !== null &&
    setFilters.participant === null &&
    setFilters.card === null &&
    setFilters.position === null
  ) {
    console.log('round default')
  } else if (
    setFilters.round === null &&
    setFilters.participant !== null &&
    setFilters.card === null &&
    setFilters.position === null
  ) {
    console.log('participant default')
  } else if (
    setFilters.round === null &&
    setFilters.participant === null &&
    setFilters.card !== null &&
    setFilters.position === null
  ) {
    console.log('card default')
  } else if (
    setFilters.round === null &&
    setFilters.participant === null &&
    setFilters.card === null &&
    setFilters.position !== null
  ) {
    console.log('position default')
  } else if (
    setFilters.round !== null &&
    setFilters.participant !== null &&
    setFilters.card === null &&
    setFilters.position === null
  ) {
    const filtered = rows.value.filter(
      (item) =>
        item.round === parseInt(setFilters.round) &&
        item.participant === parseInt(setFilters.participant)
    )
    // create a list of list according to the distribution

    qsort = getQSort(filtered)
    console.log('qsort:', qsort)

    drawQTable.value = true
  } else if (
    setFilters.round !== null &&
    setFilters.participant === null &&
    setFilters.card !== null &&
    setFilters.position === null
  ) {
    console.log('round card')
    const filtered = rows.value.filter(
      (item) => item.round === setFilters.round && item.card === setFilters.card
    )

    // map participant id to name
    const mapped = filtered.map((item) => {
      return {
        ...item,
        participant: store.participants.find((participant) => participant.id === item.participant)
          .name
      }
    })
    // create scatter plot with one column
    mapped.sort((a, b) => a.position - b.position)
    const trace = {
      x: mapped.map((item) => item.participant),
      y: mapped.map((item) => item.position),
      mode: 'markers+lines',
      type: 'scatter'
    }
    const layout = {
      title: 'Round vs Participant',
      xaxis: {
        title: 'Participant'
      },
      yaxis: {
        title: 'Position'
      }
    }

    Plotly.newPlot('plotlyChart', [trace], layout)
    document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
  } else if (
    setFilters.round !== null &&
    setFilters.participant === null &&
    setFilters.card === null &&
    setFilters.position !== null
  ) {
    console.log('round position')
    const filtered = rows.value.filter(
      (item) => item.round === setFilters.round && item.position === setFilters.position
    )
    // map card id to text
    const mapped = filtered.map((item) => {
      return {
        ...item,
        card: store.cards.cards.find((card) => card.id === item.card).text,
        participant: store.participants.find((participant) => participant.id === item.participant)
          .name
      }
    })

    // create scatter plot
    const trace = {
      x: mapped.map((item) => item.participant),
      y: mapped.map((item) => item.card),
      mode: 'markers',
      type: 'scatter'
    }
    const layout = {
      title: 'Round vs Card',
      xaxis: {
        title: 'Participant'
      },
      yaxis: {
        title: 'Card'
      }
    }
    Plotly.newPlot('plotlyChart', [trace], layout)
    document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
  } else if (
    setFilters.round === null &&
    setFilters.participant !== null &&
    setFilters.card !== null &&
    setFilters.position === null
  ) {
    console.log('line with scatter')
    console.log('participant', setFilters.participant)
    console.log('card', setFilters.card)
    const filtered = rows.value.filter(
      (item) => item.participant === setFilters.participant && item.card === setFilters.card
    )
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
    document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
  } else if (
    setFilters.round === null &&
    setFilters.participant !== null &&
    setFilters.card === null &&
    setFilters.position !== null
  ) {
    console.log('participant position')
    const filtered = rows.value.filter(
      (item) => item.participant === setFilters.participant && item.position === setFilters.position
    )
    // create scatter plot
    console.log('filtered', filtered)
    // map card id to text
    const mapped = filtered.map((item) => {
      return {
        ...item,
        card: store.cards.cards.find((card) => card.id === item.card).text
      }
    })
    console.log('rows', rows.value)

    const uniqueCards = [...new Set(mapped.map((item) => item.card))]
    const traces = []
    uniqueCards.forEach((card) => {
      const trace = {
        x: mapped.filter((item) => item.card === card).map((item) => item.round),
        y: mapped.filter((item) => item.card === card).map((item) => item.card),
        mode: 'markers+lines',
        type: 'scatter',
        name: card
      }
      traces.push(trace)
    })

    // hide legend
    const layout = {
      title: 'Participant vs Position',
      xaxis: {
        title: 'Round'
      },
      yaxis: {
        title: 'Card'
      },
      showlegend: false
    }
    Plotly.newPlot('plotlyChart', traces, layout)
    // focus on plot
    document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
  } else if (
    setFilters.round === null &&
    setFilters.participant === null &&
    setFilters.card !== null &&
    setFilters.position !== null
  ) {
    console.log('card position')
    const filtered = rows.value.filter(
      (item) => item.card === setFilters.card && item.position === setFilters.position
    )
    if (filtered.length === 0) {
      console.log('no data')
    } else {
      // create scatter plot
      const trace = {
        x: filtered.map((item) => item.round),
        y: filtered.map((item) => item.participant),
        mode: 'markers',
        type: 'scatter'
      }
      const layout = {
        title: 'Card vs Participant',
        xaxis: {
          title: 'Round'
        },
        yaxis: {
          title: 'Participant'
        }
      }
      Plotly.newPlot('plotlyChart', [trace], layout)
      document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
    }
  } else if (
    setFilters.round !== null &&
    setFilters.participant !== null &&
    setFilters.card !== null &&
    setFilters.position === null
  ) {
    const filtered = rows.value.filter(
      (item) =>
        item.round === parseInt(setFilters.round) &&
        item.participant === parseInt(setFilters.participant)
    )
    qsort = getQSort(filtered)
    // find position of the card in the qsort

    const cardText = store.cards.cards.find((card) => card.id === setFilters.card).text
    const x = qsort.findIndex((column) => column.includes(cardText))
    const y = qsort[x].findIndex((card) => card === cardText)

    highlight.value = {
      type: 'card',
      position: {
        x: x,
        y: y
      }
    }
    console.log('highlight one card')

    drawQTable.value = true
  } else if (
    setFilters.round !== null &&
    setFilters.participant !== null &&
    setFilters.card === null &&
    setFilters.position !== null
  ) {
    const filtered = rows.value.filter(
      (item) =>
        item.round === parseInt(setFilters.round) &&
        item.participant === parseInt(setFilters.participant)
    )
    qsort = getQSort(filtered)
    // find position of the card in the qsort
    highlight.value = {
      type: 'column',
      position: {
        x: setFilters.position + Math.floor(store.distribution.length / 2)
      }
    }

    drawQTable.value = true
  } else if (
    setFilters.round !== null &&
    setFilters.participant === null &&
    setFilters.card !== null &&
    setFilters.position !== null
  ) {
    console.log('round card position')
    const filtered = rows.value.filter(
      (item) =>
        item.round === parseInt(setFilters.round) &&
        item.card === parseInt(setFilters.card) &&
        item.position === parseInt(setFilters.position)
    )
    if (filtered.length === 0) {
      listData.value = 'No data'
    } else {
      console.log('filtered', filtered)
      const mapped = filtered.map((item) => {
        return {
          ...item,
          participant: store.participants.find((participant) => participant.id === item.participant)
            .name,
          card: store.cards.cards.find((card) => card.id === item.card).text
        }
      })
      listData.value = mapped
    }
  } else if (
    setFilters.round === null &&
    setFilters.participant !== null &&
    setFilters.card !== null &&
    setFilters.position !== null
  ) {
    console.log('participant card position')
    const filtered = rows.value.filter(
      (item) =>
        item.participant === parseInt(setFilters.participant) &&
        item.card === parseInt(setFilters.card) &&
        item.position === parseInt(setFilters.position)
    )
    if (filtered.length === 0) {
      listData.value = 'No data'
    } else {
      console.log('filtered', filtered)
      const trace = {
        x: filtered.map((item) => item.round),
        y: filtered.map((item) => item.position),
        mode: 'markers+lines',
        type: 'scatter'
      }

      const layout = {
        title: 'Round vs Position',
        xaxis: {
          title: 'Round',
        },
        yaxis: {
          title: 'Position',
          range: [store.positions[0], store.positions[store.positions.length - 1]]
        }
      }
      Plotly.newPlot('plotlyChart', [trace], layout)
      document.getElementById('plotlyChart').scrollIntoView({ behavior: 'smooth' })
    }
  } else if (
    setFilters.round !== null &&
    setFilters.participant !== null &&
    setFilters.card !== null &&
    setFilters.position !== null
  ) {
    console.log('round participant card position')
    const filtered = rows.value.filter(
      (item) =>
        item.round === parseInt(setFilters.round) &&
        item.participant === parseInt(setFilters.participant) &&
        item.card === parseInt(setFilters.card) &&
        item.position === parseInt(setFilters.position)
    )
    if (filtered.length === 0) {
      listData.value = 'No data'
    } else {
      const qsortData = rows.value.filter(
        (item) =>
          item.round === parseInt(setFilters.round) &&
          item.participant === parseInt(setFilters.participant)
      )
      qsort = getQSort(qsortData)
      // find position of the card in the qsort
      const cardText = store.cards.cards.find((card) => card.id === setFilters.card).text
      const x = qsort.findIndex((column) => column.includes(cardText))
      const y = qsort[x].findIndex((card) => card === cardText)

      highlight.value = {
        type: 'card',
        position: {
          x: x,
          y: y
        }
      }
      console.log('highlight one card')

      drawQTable.value = true
      

    }
  } else {
    console.log('no filters')
  }

}

const updatePlot = () => {
  // TODO: if qtable should be removed
  drawQTable.value = false
  Plotly.purge('plotlyChart')
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
  } else if (props.parentElement === 'participant') {
    selectedRound.value = null
    selectedCard.value = null
    selectedPosition.value = null
  } else if (props.parentElement === 'card') {
    selectedRound.value = null
    selectedParticipant.value = null
    selectedPosition.value = null
  } else {
    selectedRound.value = null
    selectedParticipant.value = null
    selectedCard.value = null
  }
  updatePlot()
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
  <div style="display: flex; justify-content: center; align-items: start; width: 50%">
    <v-select
      v-if="props.parentElement !== 'round'"
      v-model="selectedRound"
      :items="store.rounds.rounds"
      item-title="name"
      item-value="id"
      label="Round"
      variant="outlined"
      density="comfortable"
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
      density="comfortable"
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
      density="comfortable"
      clearable
      v-on:update:model-value="updatePlot"
    ></v-select>
    <v-select
      v-model="selectedPosition"
      :items="store.positions"
      label="Position"
      variant="outlined"
      density="comfortable"
      clearable
      v-on:update:model-value="updatePlot"
    >
    </v-select>
    <!-- <v-switch v-on:click="switch3dFunc" color="primary" label="3d" hide-details></v-switch> -->
    <!-- <v-btn v-on:click="switchAxisFunc">Switch Axis</v-btn> -->

    <!-- clear all filters -->

    <v-btn size="large"
     style="margin-left: 20px"
    v-on:click="clearFilters">Clear Filters</v-btn>
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

  <div v-if="drawQTable">
    <Qtable :distribution="store.distribution" :qsort="qsort" :highlight="highlight" id="q-table" />
  </div>
  <div v-if="listData === 'No data'">
    <v-icon>mdi-close</v-icon>
    No data
  </div>
  <div v-else-if="listData">
    <v-data-table
      :headers="[
        {
          title: 'Round',
          value: 'round'
        },
        {
          title: 'Participant',
          value: 'participant'
        },
        {
          title: 'Card',
          value: 'card'
        },
        {
          title: 'Position',
          value: 'position'
        }
      ]"
      :items="listData"
      :items-per-page="100"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>