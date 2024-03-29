import { createRouter, createWebHistory } from 'vue-router'
import StudyList from '../views/StudyList.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: StudyList
    },
    {
      path: '/study/:id',
      name: 'studyDetail',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/StudyDetail.vue')
    },
    {
      path: '/study/:id/participants',
      name: 'participants',
      component: () => import('../views/Participants.vue')
    },
    {
      path : '/study/:id/participants/:participantId',
      name: 'participantDetail',
      component: () => import('../views/ParticipantDetail.vue')
    },

    {
      path: '/study/:id/cards',
      name: 'cards',
      component: () => import('../views/Cards.vue')
    },
    {
      path: '/study/:id/cards/:cardId',
      name: 'cardDetail',
      component: () => import('../views/CardDetail.vue')
    },
    {
      path: '/study/:id/rounds',
      name: 'rounds',
      component: () => import('../views/Rounds.vue')
    },
    {
      path: '/study/:id/rounds/:roundId',
      name: 'roundDetail',
      component: () => import('../views/RoundDetail.vue')
    },
    {
      path: '/study/:id/factors',
      name: 'factors',
      component: () => import('../views/Factors.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    }
  ]
})

export default router
