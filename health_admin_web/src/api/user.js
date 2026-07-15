// src/api/user.js - 用户管理接口
import request from '@/utils/request'

export default {
   
    getList(params) {
        return request({
            url: '/users/',
            method: 'get',
            params
        })
    },
    

    create(data) {
        return request({
            url: '/users/',
            method: 'post',
            data
        })
    },
    
   
    getDetail(id) {
        return request({
            url: `/users/${id}/`,
            method: 'get'
        })
    },
    
  
    update(id, data) {
        return request({
            url: `/users/${id}/`,
            method: 'put',
            data
        })
    },
    
  
    delete(id) {
        return request({
            url: `/users/${id}/`,
            method: 'delete'
        })
    },
    
 
    getStats() {
        return request({
            url: '/users/stats/',
            method: 'get'
        })
    }
}
