<script setup>
import { onMounted } from 'vue';
import { ref } from 'vue';
import Plotly from 'plotly.js-dist';

const studyData = ref(null);
// const plotlyChart = ref(null);

// const plotChart = () => {
//   const data = [
//     {
//       z: [
//         [1, 20, 30],
//         [20, 1, 60],
//         [30, 60, 1]
//       ],
//       type: 'heatmap'
//     }
//   ];
//   const layout = {
//     title: 'Heatmap'
//   };
//   const config = {
//     responsive: true
//   };
//   Plotly.newPlot(plotlyChart.value, data, layout, config);
// };

const fetchData = async () => {
  // const id = $route.params.id;
  // const response = await fetch(`http://127.0.0.1:5000/study/${id}`);
  // const data = await response.json();
  // studyData.value = data;
};

onMounted(() => {
  fetchData();
  // plotChart();
});
</script>

<template>
  <v-container class="d-flex justify-center mt-16">
    <v-sheet elevation="4" class="rounded-lg w-75">
      <v-container>
        <h1>Study {{ $route.params.id }}</h1>
        <v-divider></v-divider>
        <!-- plotly heatmap -->
        <v-container>
          <div ref="plotlyChart"></div>
        </v-container>  
      </v-container>
    </v-sheet>
  </v-container>
</template>
