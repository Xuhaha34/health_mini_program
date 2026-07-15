import request from '@/utils/request'

export default {
    // 获取健康计划列表
    getList(params) {
        return request({
            url: '/plans/',
            method: 'get',
            params
        })
    },
    
    // 创建健康计划
    create(data) {
        return request({
            url: '/plans/',
            method: 'post',
            data
        })
    },
    
    // 获取健康计划详情
    getDetail(id) {
        return request({
            url: `/plans/${id}/`,
            method: 'get'
        })
    },
    
    // 更新健康计划
    update(id, data) {
        return request({
            url: `/plans/${id}/`,
            method: 'put',
            data
        })
    },
    
    // 删除健康计划
    delete(id) {
        return request({
            url: `/plans/${id}/`,
            method: 'delete'
        })
    }
}