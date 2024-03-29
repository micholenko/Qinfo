<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStudyStore } from '@/stores/study'

const studyStore = useStudyStore()
let studyId = useRoute().params.id

console.log(studyStore)

</script>

<template>
  <v-card style="height: 85vh; margin: 15px">
    <div style="display: flex; justify-content: center; align-items: start; height">
      <h2>Rounds</h2>
      <v-virtual-scroll :items="studyStore.rounds" :item-height="40" width="100%">
        <template v-slot:default="{ item }">
        <v-list-item
          :key="item  "
          :to="`/study/${studyId}/rounds/${item}`"
          >
          Round {{ item}}
        </v-list-item>
      </template>
    </v-virtual-scroll>
  </div>
  </v-card>    
</template>
