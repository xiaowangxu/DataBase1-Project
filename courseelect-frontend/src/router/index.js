import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginIn from '../views/LoginIn.vue'

Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		name: 'Home',
		component: LoginIn
	},
	{
		path: '/teachertable',
		name: 'TeacherTable',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/TeacherTable.vue')
	},
	{
		path: '/studenttable',
		name: 'StudentTable',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/StudentTable.vue')
	},
	{
		path: '/studenthub',
		name: 'StudentHub',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/StudentHub.vue')
	},
	{
		path: '/teacherhub',
		name: 'TeacherHub',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/TeacherHub.vue')
	},
	{
		path: '/application',
		name: 'ApplicationTable',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/ApplicationTable.vue')
	},
	{
		path: '/controlhub',
		name: 'ControlHub',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/ControlHub.vue')
	},
	{
		path: '/coursetable',
		name: 'CourseTable',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import(/* webpackChunkName: "about" */ '../views/CourseTable.vue')
	}
]

const router = new VueRouter({
	routes
})

export default router
