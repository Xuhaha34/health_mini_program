import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/modules/user'

// 创建axios实例
const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
service.interceptors.request.use(
    config => {
        const userStore = useUserStore()
        if (userStore.token) {
            config.headers['Authorization'] = `Bearer ${userStore.token}`
        }
        return config
    },
    error => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        const res = response.data

        if (res.code >= 200 && res.code < 300) {
            return res
        } else {
            if (res.code === 401) {
                const userStore = useUserStore()
                userStore.logout()
                window.location.href = '/login'
                return Promise.reject(new Error('未授权'))
            }
            ElMessage.error(res.message || '请求失败')
            return Promise.reject(new Error(res.message || '请求失败'))
        }
    },
    error => {
        console.error('响应错误:', error)

        if (error.response && error.response.status === 401) {
            const userStore = useUserStore()
            userStore.logout()
            window.location.href = '/login'
            return Promise.reject(error)
        }

        let message = '网络错误'
        if (error.response) {
            switch (error.response.status) {
                case 400:
                    message = '请求参数错误'
                    break
                case 403:
                    message = '拒绝访问'
                    break
                case 404:
                    message = '请求资源不存在'
                    break
                case 500:
                    message = '服务器内部错误'
                    break
                default:
                    message = `连接错误${error.response.status}`
            }
        } else {
            message = '网络连接异常'
        }

        ElMessage.error(message)
        return Promise.reject(error)
    }
)

export default service