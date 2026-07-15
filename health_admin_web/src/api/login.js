
import request from '@/utils/request'

export default {
    
    adminLogin(data) {
        return request({
            url: '/users/login/',
            method: 'post',
            data
        })
    },
    

    getUserInfo() {
        return request({
            url: '/users/info/',
            method: 'get'
        })
    }
}
