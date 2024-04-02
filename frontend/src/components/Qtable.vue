<script setup>
import { onMounted } from 'vue';
import * as d3 from 'd3';
import { defineProps } from 'vue';
import {watch} from 'vue';

const props = defineProps(['distribution', 'qsort', 'id']);

console.log('in Qtable', props)


// Assume qTable is a 2D array representing your Q-table
const height = 500;
// stretch the width to fit parent container
const width = 800;

const drawQTable = () => {
  let svg = d3.select("#" + props.id).append("svg")
    .attr("width", width)
    .attr("height", height);
    
  let xScale = d3.scaleBand().domain(d3.range(props.distribution.length)).range([0, width]);
  let yScale = d3.scaleLinear().domain([0, d3.max(props.distribution)]).range([0, height]);
    
  let columns = svg.selectAll('g')
    .data(props.distribution)
    .enter()
    .append('g')
    .attr('transform', (d, i) => `translate(${xScale(i)}, 0)`)
    .attr("fill", (d, i) => d3.interpolateBlues(i / props.distribution.length))
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  columns.selectAll('rect')
    .data(d => d3.range(d))
    .enter()
    .append('rect')
    .attr('x', 0)
    .attr('y', (d, i) => height - yScale(i + 1))
    .attr('width', xScale.bandwidth())
    .attr('height', yScale(1));

  columns.selectAll('foreignObject')
    .data((d, columnIndex) => d3.range(d).map((_, rowIndex) => ({ columnIndex, rowIndex })))
    .enter()
    .append('foreignObject')
    .attr('x', 0)
    .attr('y', (d, i) => height - yScale(i) - yScale(1))
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
    .style('font-size', function() {
      const cellWidth = xScale.bandwidth();
      const longestText = d3.max(props.qsort, function(column) {
        return d3.max(column, function(d) {
          return d.length;
        });
      });
      const fontSize = cellWidth / Math.max(longestText, 40) * 5;
      return fontSize + 'px';
    })
    .html(d => props.qsort[d.columnIndex][d.rowIndex]);
};
onMounted(drawQTable)
// watch(distribution, drawQTable)
watch(()=>props.qsort, (newVal, oldVal) => {
  console.log('newVal', newVal)
  console.log('oldVal', oldVal)

  d3.select("#" + props.id).selectAll('svg').remove()
  drawQTable()
})
</script>

<template>
  <div :id="props.id"></div>
</template>
