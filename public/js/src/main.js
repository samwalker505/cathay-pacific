import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import App from './App.vue'
import Test from './components/test/Test.vue'
import Trip from './components/trip/Trip.vue'
import Thailand from './components/trip/templates/Thailand.vue'
import Japan from './components/trip/templates/Japan.vue'

Vue.use(VueRouter);
Vue.use(VueResource);

const routes = [
  { path: '/test', component: Test },
  { path: '/trips/:trip_id/JP', component: Japan},
  { path: '/trips/:trip_id/Tokyo/NRT', redirect: '/trips/:trip_id/JP'},
  { path: '/trips/:trip_id/TH', component: Thailand},
  { path: '/trips/:trip_id/Bangkok', redirect: '/trips/:trip_id/TH'},
  { path: '/trips/:trip_id',  component: Trip }
]

const router = new VueRouter({
  mode: 'history',
  routes // short for routes: routes
})

const app = new Vue({
  router
}).$mount('#app')
