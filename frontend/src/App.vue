<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user'
import { useStudyStore } from './stores/study'
import { onMounted, ref } from 'vue'

const tab = ref(null)

const userStore = useUserStore()
const studyStore = useStudyStore()
// console.log('userStore:', userStore)
</script>

<template>
  <!-- app bar using the vuetify library -->
  <v-app>
    <v-toolbar height="50">
      <v-toolbar-title>
        <router-link style="text-decoration: none; color: black" to="/">
          Qinfo analysis
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div>
        <div v-if="userStore.user.name" style="display: flex; align-items: center">
          <p>{{ userStore.user.name }}</p>
          <v-btn text to="/login">Logout</v-btn>
        </div>
        <div v-else>
          <v-btn text to="/login">Login</v-btn>
          <v-btn text to="/register">Register</v-btn>
        </div>
      </div>
    </v-toolbar>
    <v-divider></v-divider>
    <v-toolbar height="40" v-if="studyStore.study.id">
      <v-tabs v-model="tab" background-color="transparent" color="black">
        <v-tab :to="`/study/${studyStore.study.id}/`">Home</v-tab>
        <v-tab :to="`/study/${studyStore.study.id}/participants`">Participants</v-tab>
        <v-tab :to="`/study/${studyStore.study.id}/cards`">Cards</v-tab>
        <v-tab :to="`/study/${studyStore.study.id}/rounds`">Rounds</v-tab>
        <v-tab :to="`/study/${studyStore.study.id}/factors`">Factors</v-tab>
      </v-tabs>
    </v-toolbar>
    <v-main>
      <router-view />
    </v-main>

    <!-- make a list component centered in the page -->
    <!-- <v-container>
      <v-card>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-card>
                Menu
              </v-card>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>

            </v-list-item-content>
          </v-list-item>
        </v-list>
        
      </v-card>
    </v-container> -->
  </v-app>

  <!-- <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header> -->

  <!-- <h1>API Response</h1>
  <pre>{{ apiResponse }}</pre>

  <div>
    <div ref="plotlyChart"></div>
  </div> -->
  <!-- <RouterView /> -->
</template>

<style scoped>
/*header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}*/
</style>
