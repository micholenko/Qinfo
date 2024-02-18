<script setup>
import { onMounted } from 'vue';
import * as d3 from 'd3';
import { defineProps } from 'vue';
import {watch} from 'vue';
import { ref } from 'vue';
import { W } from 'plotly.js-dist';

const props = defineProps(['distribution', 'cardsFinal']);
const distribution = ref(props.distribution)

let cardIndex = 0;
const getCardText = () => {
  const text = props.cardsFinal[cardIndex].text;
  console.log('cardIndex', cardIndex, text)
  cardIndex++;
  return text;
}


// Assume qTable is a 2D array representing your Q-table
const height = 500;
// stretch the width to fit parent container
const width = 800;

const drawQTable = () => {
  let svg = d3.select("#q-table").append("svg")
  .attr("width", width)
    .attr("height", height);
    
    
    let xScale = d3.scaleBand().domain(d3.range(distribution.value.length)).range([0, width]);
    let yScale = d3.scaleLinear().domain([0, d3.max(distribution.value)]).range([0, height]);
    

    let columns = svg.selectAll('g')
    .data(distribution.value)
    .enter()
    .append('g')
    .attr('transform', (d, i) => `translate(${xScale(i)}, 0)`)
    .attr("fill", (d, i) => d3.interpolateBlues(i / distribution.value.length))
    .attr("stroke", "black")
    .attr("stroke-width", 1)

    columns.selectAll('rect')
    .data(d => d3.range(d))
    .enter()
    .append('rect')
    .attr('x', 0)
    .attr('y', (d, i) => height - yScale(i + 1))
    .attr('width', xScale.bandwidth())
    .attr('height', yScale(1))

    columns.selectAll('text')
    .data(d => d3.range(d))
    .enter()
    .append('text')
    .attr('x', xScale.bandwidth() / 2)
    .attr('y', (d, i) => height - yScale(i) - yScale(1) / 2)
    .attr('text-anchor', 'middle')
    .attr('alignment-baseline', 'middle')
    .text((d, i) => getCardText());
  };
onMounted(drawQTable)
// watch(distribution, drawQTable)
watch(()=>props.cardsFinal, (newVal, oldVal) => {
  console.log('cardsFinal changed', newVal, oldVal)
  cardIndex = 0;
  d3.select("#q-table").selectAll('svg').remove()
  drawQTable()

})
</script>

<template>
  <div id="q-table"></div>
</template>

<script>
  
</script>
