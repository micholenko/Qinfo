<!-- create a login page with vue3 composition api -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const email = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  const response = await fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email.value,
      password: password.value
    })
  })
  const data = await response.json()
  if (response.status === 200) {
    // localStorage.setItem('token', data.token)
    userStore.user.name = data.name
    userStore.user.email = data.email
    router.push('/')
  }
}
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" offset-sm="3">
        <v-card>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-text-field v-model="email" label="Email"></v-text-field>
            <v-text-field v-model="password" label="Password" type="password"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="login">Login</v-btn>
          </v-card-actions>
         </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  