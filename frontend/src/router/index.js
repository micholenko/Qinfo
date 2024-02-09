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
  ]
})

export default router
