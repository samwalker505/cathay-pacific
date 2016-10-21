import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import Test from './components/test/Test.vue'

Vue.use(VueRouter);

const routes = [
  { path: '/test', component: Test },
  { path: '*', component: App }
]

const router = new VueRouter({
  mode: 'history',
  routes // short for routes: routes
})

const app = new Vue({
  router
}).$mount('#app')
