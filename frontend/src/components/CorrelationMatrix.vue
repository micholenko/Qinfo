<script setup>
import plotly from 'plotly.js-dist'

import { onMounted } from 'vue';

const users = [
  { title: '', key: 'blank', align: 'center', sortable: false },
  { title: 'User1', key: 'user1', align: 'center', sortable: false},
  { title: 'User2', key: 'user2', align: 'center', sortable: false },
  { title: 'User3', key: 'user3', align: 'center', sortable: false },
  { title: 'User4', key: 'user4', align: 'center', sortable: false },
  { title: 'User5', key: 'user5', align: 'center', sortable: false },
  { title: 'User6', key: 'user6', align: 'center', sortable: false },
  { title: 'User7', key: 'user7', align: 'center', sortable: false },
  { title: 'User8', key: 'user8', align: 'center', sortable: false },
  { title: 'User9', key: 'user9', align: 'center', sortable: false },
  { title: 'User10', key: 'user10', align: 'center', sortable: false },
  { title: 'User11', key: 'user11', align: 'center', sortable: false },
  { title: 'User12', key: 'user12', align: 'center', sortable: false },
  { title: 'User13', key: 'user13', align: 'center', sortable: false },
  { title: 'User14', key: 'user14', align: 'center', sortable: false },
  { title: 'User15', key: 'user15', align: 'center', sortable: false },
  { title: 'User16', key: 'user16', align: 'center', sortable: false },
  { title: 'User17', key: 'user17', align: 'center', sortable: false },
  { title: 'User18', key: 'user18', align: 'center', sortable: false },
  // generate until 40
  { title: 'User19', key: 'user19', align: 'center', sortable: false },
  { title: 'User20', key: 'user20', align: 'center', sortable: false },
  { title: 'User21', key: 'user21', align: 'center', sortable: false },
  { title: 'User22', key: 'user22', align: 'center', sortable: false },
  { title: 'User23', key: 'user23', align: 'center', sortable: false },
  { title: 'User24', key: 'user24', align: 'center', sortable: false },
  { title: 'User25', key: 'user25', align: 'center', sortable: false },
  { title: 'User26', key: 'user26', align: 'center', sortable: false },
  { title: 'User27', key: 'user27', align: 'center', sortable: false },
  { title: 'User28', key: 'user28', align: 'center', sortable: false },
  { title: 'User29', key: 'user29', align: 'center', sortable: false },
  { title: 'User30', key: 'user30', align: 'center', sortable: false },
  { title: 'User31', key: 'user31', align: 'center', sortable: false },
  { title: 'User32', key: 'user32', align: 'center', sortable: false },
  { title: 'User33', key: 'user33', align: 'center', sortable: false },
  { title: 'User34', key: 'user34', align: 'center', sortable: false },
  { title: 'User35', key: 'user35', align: 'center', sortable: false },
  { title: 'User36', key: 'user36', align: 'center', sortable: false },
  { title: 'User37', key: 'user37', align: 'center', sortable: false },
  { title: 'User38', key: 'user38', align: 'center', sortable: false },
  { title: 'User39', key: 'user39', align: 'center', sortable: false },
  { title: 'User40', key: 'user40', align: 'center', sortable: false }
]
const values = [
  { blank: 'User1', user1: 1, user2: 0.5 },
  { blank: 'User2', user1: 0.5, user2: 1 },
  { blank: 'User3', user1: 0.5, user2: 0.5 },
  { blank: 'User4', user1: 0.5, user2: 0.5 },
  { blank: 'User5', user1: 0.5, user2: 0.5 },
  { blank: 'User6', user1: 0.5, user2: 0.5 },
  { blank: 'User7', user1: 0.5, user2: 0.5 },
  { blank: 'User8', user1: 0.5, user2: 0.5 },
  { blank: 'User9', user1: 0.5, user2: 0.5 },
  { blank: 'User10', user1: 0.5, user2: 0.5 },
  { blank: 'User11', user1: 0.5, user2: 0.5 },
  { blank: 'User12', user1: 0.5, user2: 0.5 },
  { blank: 'User13', user1: 0.5, user2: 0.5 },
  { blank: 'User14', user1: 0.5, user2: 0.5 },
  { blank: 'User15', user1: 0.5, user2: 0.5 },
  { blank: 'User16', user1: 0.5, user2: 0.5 },
  { blank: 'User17', user1: 0.5, user2: 0.5 },
  { blank: 'User18', user1: 0.5, user2: 0.5 },
  { blank: 'User19', user1: 0.5, user2: 0.5 },
  { blank: 'User20', user1: 0.5, user2: 0.5 },
  { blank: 'User21', user1: 0.5, user2: 0.5 },
  { blank: 'User22', user1: 0.5, user2: 0.5 },
  { blank: 'User23', user1: 0.5, user2: 0.5 },
  { blank: 'User24', user1: 0.5, user2: 0.5 },
  { blank: 'User25', user1: 0.5, user2: 0.5 },
  { blank: 'User26', user1: 0.5, user2: 0.5 },
  { blank: 'User27', user1: 0.5, user2: 0.5 },
  { blank: 'User28', user1: 0.5, user2: 0.5 },
  { blank: 'User29', user1: 0.5, user2: 0.5 },
  { blank: 'User30', user1: 0.5, user2: 0.5 },
  { blank: 'User31', user1: 0.5, user2: 0.5 },
  { blank: 'User32', user1: 0.5, user2: 0.5 },
  { blank: 'User33', user1: 0.5, user2: 0.5 },
  { blank: 'User34', user1: 0.5, user2: 0.5 },
  { blank: 'User35', user1: 0.5, user2: 0.5 },
  { blank: 'User36', user1: 0.5, user2: 0.5 },
  { blank: 'User37', user1: 0.5, user2: 0.5 },
  { blank: 'User38', user1: 0.5, user2: 0.5 },
  { blank: 'User39', user1: 0.5, user2: 0.5 },
  { blank: 'User40', user1: 0.5, user2: 0.5 }
]

const fetchMatrix = async (round_id) => {
  const response = await fetch('http://localhost:5000/rounds/' + round_id + '/matrix')
  const data = await response.json()
  return data
}

onMounted(async () => {
  const round_id = 1
  const matrix = await fetchMatrix(round_id)
  plotly.newPlot('matrix', matrix)
})

</script>

<template>
  <!-- make columns narrow -->
  <!-- <v-data-table
    :headers="users"
    :items="values"
    :hide-default-footer="true"
    class="elevation-1"
    disable-sort
    items-per-page="40"
    fixed-header="true"
    :height="500"
    density="dense"
  >
    <template #bottom></template>
  </v-data-table> -->
  <div class="text-h6">
    Correlation Matrix shows the correlation between answers of participants.
  </div>
  <div id="matrix"></div>
</template>

<!-- https://github.com/zhitnyakov/vuetify-fixed-columns/blob/master/src/components/TableWithFixedColumn.vue -->
<style>
table > tbody > tr > td:nth-child(1),
table > thead > tr > th:nth-child(1) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 0;
  /* z-index: 9998; */
  background: white;
}


table > tbody > tr > td {
    border: 1px solid #e0e0e0;
}

</style>
