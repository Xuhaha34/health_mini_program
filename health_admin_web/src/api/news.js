// src/api/news.js - 资讯管理接口
import request from '@/utils/request'

export default {
    // 小程序端公开接口

    getCategories() {
        return request({
            url: '/news/categories/',
            method: 'get'
        })
    },
    

    getList(params) {
        return request({
            url: '/news/',
            method: 'get',
            params
        })
    },
    

    getDetail(id) {
        return request({
            url: `/news/${id}/`,
            method: 'get'
        })
    },
    


    getManageList(params) {
        return request({
            url: '/news/manage/',
            method: 'get',
            params
        })
    },
    
 
    create(data) {
        return request({
            url: '/news/manage/',
            method: 'post',
            data
        })
    },
    

    update(id, data) {
        return request({
            url: `/news/manage/${id}/`,
            method: 'put',
            data
        })
    },
    

    delete(id) {
        return request({
            url: `/news/manage/${id}/`,
            method: 'delete'
        })
    }
}
