import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Main from '@/components/Main'
import SA from '@/components/SA'
import Table from '@/components/Table'
import Search from '@/components/Search.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/main',
      name: 'Main',
      component: Main
    },
    {
      path: '/static',
      name: 'static',
      component: SA
    },
    {
      path: '/table',
      name: 'table',
      component: Table
    },
    {
      path: '/search',
      name: 'search',
      component: Search
    }
  ]
})