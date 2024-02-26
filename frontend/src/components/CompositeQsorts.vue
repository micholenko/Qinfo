<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import { watch } from 'vue'

import Qtable from '@/components/Qtable.vue'

import { defineProps } from 'vue'
import { cardsWithText } from '@/helpers'

const props = defineProps(['qset', 'distribution'])

const data = ref(null)
const loading = ref(true)
const qSortWithText = ref([])
const selectedFactor = ref(0)

watch(
  () => selectedFactor,
  async () => {
    console.log('selectedFactor', selectedFactor.value)
    await updateQsort()
  }
)

const fetchData = async (round_id) => {
  const response = await fetch('http://localhost:5000/rounds/' + round_id + '/composite')
  const responseData = await response.json()
  data.value = responseData
}

const updateQsort = async () => {
  console.log('selectedFactor', selectedFactor.value)
  console.log('data', data.value)
  console.log(data.value[selectedFactor.value].cards)
  qSortWithText.value = await cardsWithText(data.value[selectedFactor.value].cards, props.qset)
}

onMounted(async () => {
  const round_id = 1
  await fetchData(round_id)
  await updateQsort()
  loading.value = false
})
</script>

<template>
  <v-container v-if="!loading">
    <div class="text-h6">
      Composite Qsorts are the average responses for each factor.  

    </div>
    <v-select
      label="Select factor"
      :items="[...Array(data.length).keys()]"
      v-model="selectedFactor"
      @update:model-value="updateQsort"
      style="width: 200px; margin: 10px 0 10px 0"
    >
      <template v-slot:selection="{ item }">
        Factor {{ item.value + 1 }}
      </template>
      <template v-slot:item="{ props, item }">
        <v-list-item v-bind="props" :title="`Factor ${item.value + 1}`"></v-list-item>
      </template>
    </v-select>
    <Qtable :distribution="props.distribution" :qsort="qSortWithText" id="composite-qsort" />
  </v-container>
</template>
