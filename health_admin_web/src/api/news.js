// src/api/news.js - 资讯管理接口
import request from '@/utils/request'

export default {
    // ==================== 小程序端公开接口 ====================
    // 获取资讯分类列表
    getCategories() {
        return request({
            url: '/news/categories/',
            method: 'get'
        })
    },
    
    // 获取资讯列表（已发布）
    getList(params) {
        return request({
            url: '/news/',
            method: 'get',
            params
        })
    },
    
    // 获取资讯详情
    getDetail(id) {
        return request({
            url: `/news/${id}/`,
            method: 'get'
        })
    },
    
    // ==================== 管理后台接口 ====================
    // 获取所有资讯（含草稿）
    getManageList(params) {
        return request({
            url: '/news/manage/',
            method: 'get',
            params
        })
    },
    
    // 创建资讯
    create(data) {
        return request({
            url: '/news/manage/',
            method: 'post',
            data
        })
    },
    
    // 更新资讯
    update(id, data) {
        return request({
            url: `/news/manage/${id}/`,
            method: 'put',
            data
        })
    },
    
    // 删除资讯
    delete(id) {
        return request({
            url: `/news/manage/${id}/`,
            method: 'delete'
        })
    }
}
