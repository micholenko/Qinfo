<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <!-- app bar using the vuetify library -->
  <v-app>
    <v-layout>
      <v-app-bar rounded>
        <v-app-bar-title>Qinfo</v-app-bar-title>
        <v-spacer></v-spacer>
        <router-link to="/">Home</router-link>
      </v-app-bar>
      <v-main class='bg-blue-grey-lighten-5'>
        <router-view/>
      </v-main>
    </v-layout>

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
