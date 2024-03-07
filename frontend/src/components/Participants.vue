<script setup>
import { ref, onMounted } from 'vue'
import { cardsWithText } from '@/helpers'
import Qtable from '@/components/Qtable.vue'
import CrossRoundStatistics from './CrossRoundStatistics.vue';

const props = defineProps(['qSet', 'distribution', 'rounds'])

const qSortWithText = ref([])
const selectedRound = ref(null)
const responses = ref(null)
const cards = ref(null)
const selectedResponse = ref(null)
const loading = ref(true)
const isInitialLoad = ref(true)

const fetchRound = async (round) => {
  let ret = await fetch(`http://localhost:5000/responses?round=${round}`)
  const data = await ret.json()
  responses.value = data
}

const updateRound = async (round) => {
  isInitialLoad.value = false
  await fetchRound(round)
  selectedResponse.value = responses.value[0]
  if (selectedResponse.value)
    await updateResponse(selectedResponse.value.id)
  else {
    qSortWithText.value = []
  }
}

const fetchResponse = async (response_id) => {
  let ret = await fetch(`http://localhost:5000/responses/${response_id}/cards`)
  const data = await ret.json()
  cards.value = data
}

const updateResponse = async (response_id) => {
  console.log('response_id', response_id)
  await fetchResponse(response_id)
  qSortWithText.value = cardsWithText(cards.value, props.qSet)
  console.log('qSortWithText', qSortWithText)
}

onMounted(async () => {
  await fetchRound(props.rounds[0])
  selectedRound.value = props.rounds[0]
  selectedResponse.value = responses.value[0]
  console.log('selectedResponse', selectedResponse.value)
  await updateResponse(selectedResponse.value.id)
  // sleep for 1 second
  loading.value = false
})
</script>

<template>
  <v-container v-if="!loading">
    <v-container v-if="rounds.length >  1">
      <CrossRoundStatistics/>
    </v-container> 

    <div class="text-h6">
      Select a round and a user to view their Q-Sort
    </div>
    <v-slide-group show-arrows>
      
      <v-slide-group-item
        v-for="(round, index) in props.rounds"
        :key="round"
        v-slot:default="{ isSelected, toggle }"
      >
        <v-btn class="ma-2" :color="isSelected || (isInitialLoad && index === 0) ? 'primary' : undefined" @click="updateRound(round); toggle()">
          Round {{ round }}
        </v-btn>
      </v-slide-group-item>
    </v-slide-group>

    <v-select
      v-model="selectedResponse"
      :items="responses"
      label="Select User"
      item-title="respondent_id"
      item-value="respondent_id"
      @update:model-value="updateResponse(selectedResponse)"
      density="compact"
      style="width: 200px; margin: 10px 0 10px 0"
    >
      <template v-slot:selection="{ item }"> User {{ item.value }} </template>
      <template v-slot:item="{ props, item }">
        <v-list-item v-bind="props" :title="`User ${item.value}`"></v-list-item>
      </template>
    </v-select>
    <v-container v-if="qSortWithText.length > 0">
      <Qtable :distribution="props.distribution" :qsort="qSortWithText" id="participants" />
    </v-container>
  </v-container>
</template>
