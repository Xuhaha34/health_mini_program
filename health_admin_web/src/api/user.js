// src/api/user.js - 用户管理接口
import request from '@/utils/request'

export default {
    // 获取用户列表
    getList(params) {
        return request({
            url: '/users/',
            method: 'get',
            params
        })
    },
    
    // 创建用户
    create(data) {
        return request({
            url: '/users/',
            method: 'post',
            data
        })
    },
    
    // 获取用户详情
    getDetail(id) {
        return request({
            url: `/users/${id}/`,
            method: 'get'
        })
    },
    
    // 更新用户信息
    update(id, data) {
        return request({
            url: `/users/${id}/`,
            method: 'put',
            data
        })
    },
    
    // 删除用户
    delete(id) {
        return request({
            url: `/users/${id}/`,
            method: 'delete'
        })
    },
    
    // 获取用户统计
    getStats() {
        return request({
            url: '/users/stats/',
            method: 'get'
        })
    }
}
