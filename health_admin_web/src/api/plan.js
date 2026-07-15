import request from '@/utils/request'

export default {
 
    getList(params) {
        return request({
            url: '/plans/',
            method: 'get',
            params
        })
    },
    

    create(data) {
        return request({
            url: '/plans/',
            method: 'post',
            data
        })
    },
    
 
    getDetail(id) {
        return request({
            url: `/plans/${id}/`,
            method: 'get'
        })
    },
    

    update(id, data) {
        return request({
            url: `/plans/${id}/`,
            method: 'put',
            data
        })
    },
    

    delete(id) {
        return request({
            url: `/plans/${id}/`,
            method: 'delete'
        })
    }
}
