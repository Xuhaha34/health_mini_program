import { defineStore } from 'pinia'
import loginApi from '@/api/login'

export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('admin_token') || '',
        userInfo: JSON.parse(localStorage.getItem('admin_userInfo') || '{}'),
        permissions: []
    }),
    getters: {
        isLoggedIn: (state) => !!state.token,
        username: (state) => state.userInfo.username || '管理员'
    },
    actions: {
        // 登录
        async login(loginForm) {
            try {
                const res = await loginApi.adminLogin(loginForm)
                if (res.code === 200) {
                    // 后端返回 access_token，前端使用 token
                    this.setToken(res.data.access_token)
                    // 后端返回 user，前端使用 userInfo
                    this.setUserInfo(res.data.user)
                    return res
                } else {
                    throw new Error(res.message || '登录失败')
                }
            } catch (error) {
                throw error
            }
        },
        setToken(token) {
            this.token = token
            localStorage.setItem('admin_token', token)
        },
        setUserInfo(info) {
            this.userInfo = info
            localStorage.setItem('admin_userInfo', JSON.stringify(info))
        },
        setPermissions(permissions) {
            this.permissions = permissions
        },
        logout() {
            this.token = ''
            this.userInfo = {}
            this.permissions = []
            localStorage.removeItem('admin_token')
            localStorage.removeItem('admin_userInfo')
        }
    }
})
