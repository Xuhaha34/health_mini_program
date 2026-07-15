import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/modules/user'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login/index.vue'),
        meta: { title: '管理员登录' }
    },
    {
        path: '/',
        component: () => import('@/components/Layout/index.vue'),
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('@/views/Dashboard/index.vue'),
                meta: { title: '数据看板', icon: 'DataAnalysis' }
            },
            {
                path: 'users',
                name: 'UserManage',
                component: () => import('@/views/UserManage/index.vue'),
                meta: { title: '用户管理', icon: 'User' }
            },
            {
                path: 'body-records',
                name: 'BodyRecord',
                component: () => import('@/views/BodyRecord/index.vue'),
                meta: { title: '体征数据', icon: 'Monitor' }
            },
            {
                path: 'diet-records',
                name: 'DietRecord',
                component: () => import('@/views/DietRecord/index.vue'),
                meta: { title: '饮食记录', icon: 'Food' }
            },
            {
                path: 'sport-records',
                name: 'SportRecord',
                component: () => import('@/views/SportRecord/index.vue'),
                meta: { title: '运动记录', icon: 'Bicycle' }
            },
            {
                path: 'news',
                name: 'NewsManage',
                component: () => import('@/views/NewsManage/index.vue'),
                meta: { title: '资讯管理', icon: 'Document' }
            },
            {
                path: 'plans',
                name: 'HealthPlan',
                component: () => import('@/views/HealthPlan/index.vue'),
                meta: { title: '健康计划', icon: 'List' }
            },
            {
                path: 'system',
                name: 'SystemConfig',
                component: () => import('@/views/SystemConfig/index.vue'),
                meta: { title: '系统配置', icon: 'Setting' }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})


router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    const token = userStore.token
    
    if (to.path !== '/login' && !token) {
        next('/login')
    } else if (to.path === '/login' && token) {
        next('/')
    } else {
        next()
    }
})

export default router
