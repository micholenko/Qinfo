<script setup>
import { ref, onMounted } from 'vue'
import { useStudyStore } from '@/stores/study'

import Plotly from 'plotly.js-dist'
import { parse } from 'vue/compiler-sfc'
import * as d3 from 'd3'



const store = useStudyStore()
const props = defineProps(['participantId'])

const attributeStringArr = ['round', 'participant', 'card', 'position']

const colors = [
  '#1f77b4',
  '#ff7f0e',
  '#2ca02c',
  '#d62728',
  '#9467bd',
  '#8c564b',
  '#e377c2',
  '#7f7f7f',
  '#bcbd22',
  '#17becf'
]

const round = ref(null)
const participant = ref(null)
if (props.participantId) {
  participant.value = parseInt(props.participantId)
}
const card = ref(null)
const position = ref(null)
const data = ref([])
const filters = [round, participant, card, position]
const filterCount = ref(0)
const dataPointExists = ref(false)
const showListData = ref([])
const switch3d = ref(false)
const switchAxis = ref(false)

const getSetFilters = () => {
  const setFilters = []
  for (let i = 0; i < attributeStringArr.length; i++) {
    if (filters[i].value !== null) {
      setFilters.push(attributeStringArr[i])
    }
  }
  return setFilters
}

// get inedxes of unset filters
const getUnsetFilters = () => {
  const unsetFilters = []
  for (let i = 0; i < filters.length; i++) {
    if (filters[i].value === null) {
      unsetFilters.push(i)
    }
  }
  return unsetFilters
}

const capitalizeFirst = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

const clearFilters = () => {
  round.value = null
  participant.value = null
  card.value = null
  position.value = null
  filterCount.value = 0
  updatePlot()
}

const countFilters = () => {
  console.log('position:', position.value)
  let count = 0
  if (round.value) count++
  if (participant.value) count++
  if (card.value) count++
  if (position.value !== null) count++
  filterCount.value = count
  return count
}

const switchAxisFunc = () => {
  switchAxis.value = !switchAxis.value
  updatePlot()
}

const switch3dFunc = () => {
  switch3d.value = !switch3d.value
  updatePlot()
}

const axesLabels = (filter) => {
  if (filter === 'round')
    return {
      tickvals: store.rounds,
      ticktext: store.rounds,
      range: [store.rounds[0] - 0.5, store.rounds[store.rounds.length - 1] + 0.5]
    }
  if (filter === 'card')
    return {
      tickvals: store.cards.cards.map((card) => card.id),
      // truncate x axis tick labels
      ticktext: store.cards.cards.map((card) => card.text)
    }
  if (filter === 'participant')
    return {
      tickvals: store.participants.map((participant) => participant.id),
      ticktext: store.participants.map((participant) => participant.name)
    }
  if (filter === 'position')
    return {
      tickvals: store.positions,
      range: [store.positions[0] - 0.5, store.positions[store.positions.length - 1] + 0.5]
    }
}

const scatter3d = (filteredData, selectedFilters) => {
  const axNames = attributeStringArr.filter((name) => !selectedFilters.includes(name))

  const trace = {
    x: filteredData.map((row) => row[axNames[0]]),
    y: filteredData.map((row) => row[axNames[1]]),
    z: filteredData.map((row) => row[axNames[2]]),
    mode: 'markers',
    type: 'scatter3d',
    marker: {
      size: 8
    }
  }
  const layout = {
    scene: {
      xaxis: { title: capitalizeFirst(axNames[0]), ...axesLabels(axNames[0]) },
      yaxis: { title: capitalizeFirst(axNames[1]), ...axesLabels(axNames[1]) },
      zaxis: { title: capitalizeFirst(axNames[2]), ...axesLabels(axNames[2]) },
      aspectmode: 'cube' // TODO: change, will not work for bigger data sets
    },
    margin: {
      t: 30, //top margin
      l: 0, //left margin
      r: 0, //right margin
      b: 0 //bottom margin
    }
  }
  return { traces: [trace], layout }
}

const scatter3dPerRound = (filteredData) => {
  const uniqueRounds = [...new Set(filteredData.map((row) => row.round))]
  console.log('uniqueRounds:', uniqueRounds)

  const traces = []

  uniqueRounds.forEach((round, index) => {
    const filteredData = data.value.filter((row) => row.round === round)
    const trace = {
      x: filteredData.map((row) => row.card),
      y: filteredData.map((row) => row.participant),
      z: filteredData.map((row) => row.position),
      mode: 'markers',
      type: 'scatter3d',
      name: `Round ${round}`,
      marker: {
        color: colors[round % colors.length]
      }
    }

    traces.push(trace)
  })
  const layout = {
    scene: {
      xaxis: {
        title: 'Card',
        tickvals: store.cards.cards.map((card) => card.id),
        ticktext: store.cards.cards.map((card) => card.text)
      },
      yaxis: {
        title: 'Participant',
        tickvals: store.participants.map((participant) => participant.id),
        ticktext: store.participants.map((participant) => participant.name)
      },
      zaxis: { title: 'Position', tickvals: store.positions }
    },
    margin: {
      t: 30, //top margin
      l: 0, //left margin
      r: 0, //right margin
      b: 0 //bottom margin
    }
  }
  return { traces, layout }
}

// const boxplot = ()

const scatter2d = (inputData, selectedFilters) => {
  const attributesWithoutRound = attributeStringArr.filter((name) => name !== 'round')
  const axNames = attributesWithoutRound.filter((name) => !selectedFilters.includes(name))
  // const uniqueRounds = [...new Set(inputData.map((row) => row.round))]
  const traces = []

  const xAttr = switchAxis.value ? axNames[1] : axNames[0]
  const yAttr = switchAxis.value ? axNames[0] : axNames[1]

  const uniqueRounds = [...new Set(inputData.map((row) => row.round))]

  // Create a trace for each round
  uniqueRounds.forEach((round, index) => {
    const filteredData = inputData.filter((row) => row.round === round)
    const trace = {
      x: filteredData.map((row) => row[xAttr] + Math.random() * 0.2 - 0.1), // jitter
      y: filteredData.map((row) => row[yAttr]),
      unjitteredX: filteredData.map((row) => row[xAttr]),
      // mode: 'markers+lines',
      mode: 'lines+markers',
      opacity: 0.7,
      type: 'scatter',
      name: `Round ${round}`,
      marker: {
        size: 12,
        color: colors[round % colors.length],
        colorscale: 'Viridis'
      }
    }
    trace.hoverinfo = 'text'
    // TODO: make better
    trace.text = filteredData.map((row, i) => `x: ${trace.unjitteredX[i]}, y: ${row[yAttr]}`)
    // truncate x axis tick labels
    traces.push(trace)
  })

  const layout = {
    xaxis: { title: capitalizeFirst(xAttr), ...axesLabels(xAttr), tickangle: 90},
    yaxis: { title: capitalizeFirst(yAttr), ...axesLabels(yAttr) },
    margin: {
      t: 30, //top margin
      l: 50, //left margin
      r: 30, //right margin
      b: 50 //bottom margin
    }
  }

  return { traces, layout }
}

const scatter2d2filters = (inputData, selectedFilters) => {
  const axNames = attributeStringArr.filter((name) => !selectedFilters.includes(name))

  const xAttr = switchAxis.value ? axNames[1] : axNames[0]
  const yAttr = switchAxis.value ? axNames[0] : axNames[1]

  const trace = {
    x: inputData.map((row) => row[xAttr]),
    y: inputData.map((row) => row[yAttr]),
    unjitteredX: inputData.map((row) => row[xAttr]),
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 12
    }
  }
  const layout = {
    xaxis: { title: capitalizeFirst(xAttr), ...axesLabels(xAttr) },
    yaxis: { title: capitalizeFirst(yAttr), ...axesLabels(yAttr) },
    margin: {
      t: 30, //top margin
      l: 50, //left margin
      r: 30, //right margin
      b: 50 //bottom margin
    }
  }
  return { traces: [trace], layout }
}

const updatePlot = () => {
  const count = countFilters()
  console.log('count:', count)

  // Create a color scale for the legend
  let traces = [],
    layout = {}
  if (count === 0) {
    ;({ traces, layout } = scatter3dPerRound(data.value))
  } else if (count === 1) {
    console.log('one filter')
    if (round.value !== null) {
      // filter data by round
      const filteredData = data.value.filter((row) => row.round === round.value)
      ;({ traces, layout } = scatter3dPerRound(filteredData))
    }

    if (participant.value !== null) {
      console.log('participant:', participant.value)
      console.log('data:', data.value)
      const filteredData = data.value.filter((row) => row.participant === participant.value)
      console.log('filteredData:', filteredData)
      filteredData.sort((a, b) => a.card - b.card)

      if (switch3d.value) {
        ;({ traces, layout } = scatter3d(filteredData, ['participant']))
      } else {
        ;({ traces, layout } = scatter2d(filteredData, ['participant']))
      }
    }
    if (card.value !== null) {
      // filter data by card
      const filteredData = data.value.filter((row) => row.card === card.value)
      if (switch3d.value) {
        ;({ traces, layout } = scatter3d(filteredData, ['card']))
      } else {
        ;({ traces, layout } = scatter2d(filteredData, ['card']))
      }
    }
    if (position.value !== null) {
      // filter data by position
      const filteredData = data.value.filter((row) => row.position === position.value)
      if (switch3d.value) {
        ;({ traces, layout } = scatter3d(filteredData, ['position']))
      } else {
        ;({ traces, layout } = scatter2d(filteredData, ['position']))
      }
    }
  } else if (count === 2) {
    // get the two filters
    const filters = [round.value, participant.value, card.value, position.value]
    const filteredData = data.value.filter((row) => {
      let match = true
      for (let i = 0; i < filters.length; i++) {
        if (filters[i] !== null && row[Object.keys(row)[i]] !== filters[i]) {
          match = false
        }
      }
      return match
    })

    ;({ traces, layout } = scatter2d2filters(filteredData, getSetFilters()))
  }
  Plotly.react('plotlyChart', traces, layout)

  // add on hover event, display text of data point in a box
  var tooltip = d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 1).style('position', 'absolute')
                .style('padding', '10px').style('border', '1px solid #ccc').style('border-radius', '5px').style('color', 'black')

  // Select x ticks and bind mouseover event
  d3.selectAll('.xtick')
    .on('mouseover', function (event, d) {
      let target =  this.getBoundingClientRect();
      console.log('event:', event)
      tooltip.transition().duration(200).style('opacity', 0.9)
      tooltip
        .html(d.text )
        .style('left', target.left + window.scrollX + 'px')
        .style('top', target.top + window.scrollY + 28 + 'px')
    })

  d3.selectAll('.xaxislayer-above')
    .on('mouseout', function (d) {
      console.log('mouseout')
      tooltip.transition().duration(500).style('opacity', 0)
    })
  // change text
  console.log('d3.selectAll:', d3.selectAll('.xtick'))
  if (count === 3) {
    const filters = [round.value, participant.value, card.value, position.value]
    const filteredData = data.value.filter((row) => {
      let match = true
      for (let i = 0; i < filters.length; i++) {
        if (filters[i] !== null && row[Object.keys(row)[i]] !== filters[i]) {
          match = false
        }
      }
      return match
    })
    console.log('filteredData:', filteredData)
    // get indexes of unset filters
    const unsetFilters = getUnsetFilters()
    if (filteredData.length > 0) {
      dataPointExists.value = true
      showListData.value = filteredData
    } else {
      dataPointExists.value = false
    }
  } else if (count === 4) {
    // figure out if data contains row that matches all filters
    const setFilters = getSetFilters()
    console.log('setFilters:', setFilters)
    const filteredData = data.value.filter((row) => {
      let match = true
      for (let i = 0; i < setFilters.length; i++) {
        if (row[attributeStringArr[i]] !== setFilters[i].value) {
          match = false
        }
      }
      return match
    })
    if (filteredData.length > 0) {
      dataPointExists.value = true
    } else {
      dataPointExists.value = false
    }
  }
}
const fetchData = async (studyId) => {
  const response = await fetch(`http://localhost:5000/studies/${studyId}/data`)
  data.value = await response.json()
}

onMounted(async () => {
  await fetchData(store.study.id)
  Plotly.newPlot('plotlyChart', [], {})
  updatePlot()
})
</script>

<template>
  <div style="display: flex; justify-content: center; align-items: center">
    <v-select
      v-model="round"
      :items="store.rounds"
      label="Round"
      variant="outlined"
      clearable
      v-on:update:model-value="updatePlot"
    >
    </v-select>
    <!-- conbobox -->
    <v-select
      v-if="props.participantId === undefined"
      v-model="participant"
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
      v-model="card"
      :items="store.cards.cards"
      item-title="text"
      item-value="id"
      label="Card"
      variant="outlined"
      clearable
      v-on:update:model-value="updatePlot"
    ></v-select>
    <v-select
      v-model="position"
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
  <div v-if="filterCount === 3">
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
  </div>
  <!-- style hidden based on filter count -->
  <!-- div center horizontally -->
  <div
    id="plotlyChart"
    :style="{ display: filterCount >= 3 ? 'none' : 'block', width: '100%' }"
  ></div>
</template>

<style>
.xtick {
  pointer-events: all;
}
</style>
