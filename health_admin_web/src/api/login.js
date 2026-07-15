// src/api/login.js - 管理员登录接口
import request from '@/utils/request'

export default {
    // 管理员登录
    adminLogin(data) {
        return request({
            url: '/users/login/',
            method: 'post',
            data
        })
    },
    
    // 获取用户信息
    getUserInfo() {
        return request({
            url: '/users/info/',
            method: 'get'
        })
    }
}
