<script setup>
import { onMounted } from 'vue'
import * as d3 from 'd3'
import { defineProps } from 'vue'

import { watch } from 'vue'
import { useStudyStore } from '@/stores/study'

const store = useStudyStore()
const col_values = store.positions

const props = defineProps(['distribution', 'qsort', 'highlight', 'id'])

console.log('in Qtable', props)

const drawQTable = () => {
  const maxWidth = document.getElementById(props.id).clientWidth // Get parent element's width
  const maxColumnHeight = Math.max(...props.distribution)
  const columnsCount = props.qsort.length

  const width = maxWidth < columnsCount * 200 ? maxWidth : columnsCount * 200
  const height = maxColumnHeight * (props.id === 'empty-qtable' ? 50 : 130)

  console.log('parentWidth', width)

  let svg = d3
    .select('#' + props.id)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  let xScale = d3.scaleBand().domain(d3.range(props.distribution.length)).range([0, width])
  let yScale = d3
    .scaleLinear()
    .domain([0, d3.max(props.distribution)])
    .range([0, height - 20])

  let columns = svg
    .selectAll('g')
    .data(props.distribution)
    .enter()
    .append('g')
    .attr('transform', (d, i) => `translate(${xScale(i)}, 0)`)
    .attr('fill', (d, i) => d3.interpolateRgbBasis(["lightcoral", "white", "lightgreen"])(i / props.distribution.length))
    .attr('stroke', 'black')
    .attr('stroke-width', 1)

  columns
    .selectAll('rect')
    .data((d) => d3.range(d))
    .enter()
    .append('rect')
    .attr('x', 0)
    .attr('y', (d, i) => height - yScale(i + 1) - 20)
    .attr('width', xScale.bandwidth())
    .attr('height', yScale(1))

  columns
    .selectAll('foreignObject')
    .data((d, columnIndex) => d3.range(d).map((_, rowIndex) => ({ columnIndex, rowIndex })))
    .enter()
    .append('foreignObject')
    .attr('x', 0)
    .attr('y', (d, i) => height - yScale(i) - yScale(1) -20)
    .attr('width', xScale.bandwidth())
    .attr('height', yScale(1))
    .append('xhtml:div')
    .style('width', xScale.bandwidth() + 'px')
    .style('height', yScale(1) + 'px')
    .style('padding', '5px')
    .style('display', 'flex')
    .style('justify-content', 'center')
    .style('align-items', 'center')
    .style('text-align', 'center')
    .style('font-size', function () {
      const cellWidth = xScale.bandwidth()
      const longestText = d3.max(props.qsort, function (column) {
        return d3.max(column, function (d) {
          return d.length
        })
      })
      const fontSize = (cellWidth / Math.max(longestText, 40)) * 5
      return fontSize + 'px'
    })
    .html((d) => props.qsort[d.columnIndex][d.rowIndex])

  const xAxis = svg.append('g').attr('transform', `translate(0, ${height - 20})`)

  xAxis
    .selectAll('text')
    .data(col_values)
    .enter()
    .append('text')
    .attr('x', (d, i) => xScale(i) + xScale.bandwidth() / 2)
    .attr('y', 17) // Adjust this value according to your preference for distance from the x-axis
    .attr('text-anchor', 'middle')
    .text((d) => d)

  // find column by x and row by y
  console.log('highlight', props.highlight)
  if (props.highlight !== null){
    // set opacity to 0.5 for all cells
    columns
    .selectAll('rect')
    .attr('opacity', 0.4)
    columns.
    selectAll('foreignObject')
    .attr('opacity', 0.4)
    if (props.highlight.type === 'card')
    {

      columns
      .filter((d, i) => i === props.highlight.position.x)
      .selectAll('rect')
      .filter((d, i) => i === props.highlight.position.y)
      .attr('opacity', 1)
      .attr('id', 'highlighted')
      columns
      .filter((d, i) => i === props.highlight.position.x)
      .selectAll('foreignObject')
      .filter((d, i) => i === props.highlight.position.y)
      .attr('opacity', 1)
      // add id

      }
    else if (props.highlight.type === 'column'){
      columns
      .filter((d, i) => i === props.highlight.position.x)
      .selectAll('rect')
      .attr('opacity', 1)
      .attr('id', 'highlighted')
      columns
      .filter((d, i) => i === props.highlight.position.x)
      .selectAll('foreignObject')
      .attr('opacity', 1)
    
    }
  }

  if (document.getElementById('highlighted'))
    document.getElementById('highlighted').scrollIntoView({behavior: 'smooth', block: 'center'})
  else
    document.getElementById(props.id).scrollIntoView({behavior: 'smooth', block: 'center'})
}
onMounted(drawQTable)
// watch(distribution, drawQTable)
watch(
  () => props.qsort,
  (newVal, oldVal) => {
    console.log('newVal', newVal)
    console.log('oldVal', oldVal)

    // remove svg but leave the div
    d3.select('#' + props.id).selectAll('svg').remove()
    drawQTable()
    // get height of the div
    const height = document.getElementById(props.id).clientHeight
    console.log('height', height)
    // set the height permanently
    d3.select('#' + props.id).style('height', height + 'px')
  }
)
</script>

<template>
  <div
    :id="props.id"
    style="display: flex; justify-content: center; align-items: center; width: 100%"
  ></div>
</template>
