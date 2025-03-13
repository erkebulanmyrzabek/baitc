import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import HackathonsView from '../views/HackathonsView.vue'
import ShopView from '../views/ShopView.vue'
import RatingView from '../views/RatingView.vue'
import HackathonDetailView from '../views/HackathonDetailView.vue'
import ProfileSettingsView from '../views/ProfileSettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/hackathons', 
      name: 'hackathons',
      component: HackathonsView,
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView,
    },
    {
      path: '/rating',
      name: 'rating',
      component: RatingView,
    },
    {
      path: '/hackathon/:id',
      name: 'hackathon-detail',
      component: HackathonDetailView,
    },
    {
      path: '/settings',
      name: 'settings',
      component: ProfileSettingsView
    },
    {
      path: '/hackathons/:id',
      name: 'HackathonDetail',
      component: () => import('@/views/HackathonDetailView.vue'),
      meta: {
        requiresAuth: false
      }
    }
  ]
})

export default router
