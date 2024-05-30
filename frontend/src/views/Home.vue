<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'
import Qtable from '@/components/Qtable.vue'
import { fillStudyStore } from '@/helpers'

let studyId = useRoute().params.id

const studyStore = useStudyStore()

const studyData = ref(null)
const loading = ref(true)

const createEmptyQsort = (distribution) => {
  console.log('distribution:', distribution)
  let qsort = []
  for (let i = 0; i < distribution.length; i++) {
    qsort.push([])
  }
  return qsort
}

onMounted(async () => {
  await fillStudyStore(studyId)
  studyStore.study.id = studyId
  console.log('studyStore:', studyStore)
  loading.value = false
})
</script>

<template>
  <v-card style="height: 87vh; margin: 15px; padding-left: 15px; padding-right: 15px">
    <div
      v-if="loading"
      style="display: flex; justify-content: center; align-items: center; height: 100%"
    >
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <div
      v-else
      style="
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: start;
        height: 100%;
      "
    >
      <h1>{{ studyStore.title }}</h1>
      <h2>Question: {{ studyStore.question }}</h2>
      <h2>Created: {{ new Date(studyStore.created_time).toLocaleDateString() }}</h2>
      <p>{{ studyStore.description }}</p>
      <v-container style="margin: 0; max-width: 100%; padding-left: 0; padding-right: 0">
      <v-divider></v-divider>
    </v-container>
      <div>
        <h2>Rounds: {{ studyStore.rounds.rounds.length }}</h2>
        <div style="display: flex; gap: 20px">
          <div
            v-for="round in studyStore.rounds.rounds"
            :key="round.id"
            style="display: flex; flex-direction: column"
          >
            <h3>{{ round.name }}</h3>
            <!-- show only date no time -->
            <h4>Start: {{ new Date(round.start_time).toLocaleDateString() }}</h4>
            <h4>End: {{ new Date(round.end_time).toLocaleDateString() }}</h4>
          </div>
        </div>
      </div>
      <v-container style="margin: 0; max-width: 100%; padding-left: 0; padding-right: 0">
      <v-divider></v-divider>
    </v-container>
      <div
        style="display: flex; height: 100%; width: 100%; overflow: hidden; padding: 10px; gap: 20px"
      >
        <div style="display: flex; flex-direction: column; width: 25%">
          <h2>Cards: {{ studyStore.cards.cards.length }}</h2>
          <v-virtual-scroll :items="studyStore.cards.cards" :item-height="40">
            <template v-slot:default="{ item }">
              <v-list-item :key="item.id">
                {{ item.text }}
              </v-list-item>
            </template>
          </v-virtual-scroll>
        </div>
        <div style="display: flex; flex-direction: column; width: 20%">
          <h2>Participants: {{ studyStore.participants.length }}</h2>
          <v-virtual-scroll :items="studyStore.participants" :item-height="50">
            <template v-slot:default="{ item }">
              <v-list-item :key="item.id">
                {{ item.name }}
              </v-list-item>
            </template>
          </v-virtual-scroll>
        </div>
        <div
          style="
            display: flex;
            flex-direction: column;
            width: 55%;
            padding-left: 20px;
            height: 100%;
          "
        >
          <h2>Distribution</h2>
          <div style="display: flex; flex-direction: column; justify-content: center; height: 100%">
            <Qtable
              :distribution="studyStore.distribution"
              :qsort="createEmptyQsort(studyStore.distribution)"
              :highlight="null"
              id="empty-qtable"
            />
          </div>
        </div>
      </div>
      <!-- </div> -->
    </div>
  </v-card>
</template>
