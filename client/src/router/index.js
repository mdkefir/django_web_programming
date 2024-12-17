import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user';
import CarsView from '../views/CarsView.vue';
import BrandsView from '../views/BrandsView.vue';
import ServicesView from '../views/ServicesView.vue';
import OwnersView from '../views/OwnersView.vue';
import ServiceRecordsView from '../views/ServiceRecordsView.vue';
import LoginPage from '../views/LoginPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: "/",
      name: "CarsView",
      component: CarsView
    },
    {
      path: "/brands",
      name: "BrandsView",
      component: BrandsView
    },
    {
      path: "/services",
      name: "ServicesView",
      component: ServicesView
    },
    {
      path: "/owners",
      name: "OwnersView",
      component: OwnersView
    },
    {
      path: "/servicerecords",
      name: "ServiceRecordsView",
      component: ServiceRecordsView
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  
  if (!userStore.isAuthenticated && !to.meta.requiresAuth) {
    await userStore.checkAuth();
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router
