<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import plotly from 'plotly.js-dist'
import { sampleCorrelation } from 'simple-statistics'

import { useStudyStore } from '@/stores/study'

const round = ref(null)
const participant = ref(null)
const data = ref(null)

const createPlots = async (data) => {
  plotly.newPlot('correlations_scatter', data.scatter)
  plotly.newPlot('correlations_histogram', data.histogram)
}

const store = useStudyStore()

const countFilters = () => {
  let count = 0
  if (round.value) count++
  if (participant.value) count++
  return count
}

const getCorrelationMatrixParticipants = (data) => {
  const participants = store.participants.map((p) => p.id)
  const matrix = []
  for (let i = participants.length - 1; i >= 0; i--) {
    const row = []
    for (let j = 0; j < participants.length; j++) {
      const p1 = participants[i]
      const p2 = participants[j]
      const p1Data = data
        .filter((d) => d.participant === p1)
        .sort((a, b) => a.card - b.card)
        .map((d) => d.position)
      const p2Data = data
        .filter((d) => d.participant === p2)
        .sort((a, b) => a.card - b.card)
        .map((d) => d.position)
      console.log('p2Data', p2Data)
      const correlation = sampleCorrelation(p1Data, p2Data)
      row.push(correlation)
    }
    matrix.push(row)
  }
  return matrix
}

const getCorrelationMatrixRounds = (data) => {
  const rounds = store.rounds
  console.log(rounds)
  const matrix = []
  for (let i = rounds.length - 1; i >= 0; i--) {
    const row = []
    for (let j = 0; j < rounds.length; j++) {
      const r1 = rounds[i]
      const r2 = rounds[j]
      const r1Data = data
        .filter((d) => d.round === r1)
        .sort((a, b) => a.card - b.card)
        .map((d) => d.position)
      const r2Data = data
        .filter((d) => d.round === r2)
        .sort((a, b) => a.card - b.card)
        .map((d) => d.position)
      const correlation = sampleCorrelation(r1Data, r2Data)
      row.push(correlation)
    }
    matrix.push(row)
  }
  return matrix
}

const heatmapParticipants = (correlationMatrix) => {
  const trace = {
    z: correlationMatrix,
    x: store.participants.map((p) => p.name),
    y: store.participants.map((p) => p.name),
    type: 'heatmap',
    colorscale: 'Viridis', // You can choose a different color scale
    // display values in the cells
    zmin: -1,
    zmax: 1,
    colorbar: {
      title: 'Correlation'
    }
  }

  // Set layout
  const layout = {
    xaxis: {
      title: 'Participants'
    },
    yaxis: {
      title: 'Participants'
    }
  }
  // add anotations
  const annotations = []
  for (let i = 0; i < store.participants.length; i++) {
    for (let j = 0; j < store.participants.length; j++) {
      const result = {
        xref: 'x1',
        yref: 'y1',
        x: i,
        y: j,
        text: correlationMatrix[j][i].toFixed(2),
        showarrow: false,
        font: {
          family: 'Arial',
          size: 12,
        }
      }
      annotations.push(result)
    }
  }
  layout.annotations = annotations

  return { trace, layout }
}

const heatmapRounds = (correlationMatrix) => {
  const trace = {
    z: correlationMatrix,
    x: store.rounds,
    y: store.rounds,
    type: 'heatmap',
    colorscale: 'Viridis', // You can choose a different color scale
    zmin: -1,
    zmax: 1,
    colorbar: {
      title: 'Correlation'
    },
  }

  // Set layout
  const layout = {
    xaxis: {
      title: 'Rounds',
      range: [0.5, store.rounds.length + 0.5  ],
      tickvals: store.rounds.map((r, i) => i + 1),
    },
    yaxis: {
      title: 'Rounds',
      range: [0.5, store.rounds.length + 0.5  ],
      tickvals: store.rounds.map((r, i) => i + 1),
    }
  }
  // add anotations
  const annotations = []
  for (let i = 0; i < store.rounds.length; i++) {
    for (let j = 0; j < store.rounds.length; j++) {
      const result = {
        xref: 'x1',
        yref: 'y1',
        x: i + 1,
        y: j + 1,
        text: correlationMatrix[j][i].toFixed(2),
        showarrow: false,
        font: {
          family: 'Arial',
          size: 12,
        }
      }
      annotations.push(result)
    }
  }
  layout.annotations = annotations

  return { trace, layout }
}

const updatePlot = () => {
  const count = countFilters()
  let trace = null
  let layout = null
  if (count === 0) {
    plotly.purge('corr_matrix')
  } else if (count === 2) {
    plotly.purge('corr_matrix')

  } else if (count === 1 && round.value) {
    const filteredData = data.value.filter((d) => d.round === round.value)
    const correlationMatrix = getCorrelationMatrixParticipants(filteredData)
    ;({ trace, layout } = heatmapParticipants(correlationMatrix))

    // Create plot
  } else if (count === 1 && participant.value) {
    const filteredData = data.value.filter((d) => d.participant === participant.value)
    console.log('filteredData', filteredData)
    const correlationMatrix = getCorrelationMatrixRounds(filteredData)

    ;({ trace, layout } = heatmapRounds(correlationMatrix))
  }
  plotly.newPlot('corr_matrix', [trace], layout)
}

onMounted(async () => {
  const id = store.study.id
  try {
    let response = await fetch(`http://localhost:5000/studies/${id}/user_correlations`)
    const graphData = await response.json()
    await createPlots(graphData)
    response = await fetch(`http://localhost:5000/studies/${store.study.id}/data`)
    data.value = await response.json()
    updatePlot()
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <!-- flex -->
  <v-container style="display: flex; flex-direction: row; align-items: center">
    <v-select
      v-model="round"
      :items="store.rounds"
      label="Round"
      variant="outlined"
      clearable
      v-on:update:model-value="updatePlot"
    ></v-select>
    <v-select
      v-model="participant"
      :items="store.participants"
      item-title="name"
      item-value="id"
      label="Participant"
      variant="outlined"
      clearable
      v-on:update:model-value="updatePlot"
    ></v-select>
  </v-container>
  <v-container>
    <div id="corr_matrix"></div>
  </v-container>
  <v-container>
    <div id="correlations_scatter"></div>
    <div id="correlations_histogram"></div>
  </v-container>
</template>
