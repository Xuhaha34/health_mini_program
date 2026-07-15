// src/api/record.js - 健康记录管理接口
import request from '@/utils/request'

export default {
    //体征数据 
  
    getBodyDataList(params) {
        return request({
            url: '/records/body-data/',
            method: 'get',
            params
        })
    },
    

    deleteBodyData(id) {
        return request({
            url: `/records/body-data/${id}/`,
            method: 'delete'
        })
    },
    

    getBodyDataStats(params) {
        return request({
            url: '/records/body-data/stats/',
            method: 'get',
            params
        })
    },
    
    // 饮食记录
  
    getDietList(params) {
        return request({
            url: '/records/diet/',
            method: 'get',
            params
        })
    },

    deleteDiet(id) {
        return request({
            url: `/records/diet/${id}/`,
            method: 'delete'
        })
    },
    

    getDietStats(params) {
        return request({
            url: '/records/diet/stats/',
            method: 'get',
            params
        })
    },
    
    // 运动记录 

    getSportList(params) {
        return request({
            url: '/records/sport/',
            method: 'get',
            params
        })
    },
    

    deleteSport(id) {
        return request({
            url: `/records/sport/${id}/`,
            method: 'delete'
        })
    },
    
 
    getSportStats(params) {
        return request({
            url: '/records/sport/stats/',
            method: 'get',
            params
        })
    },

   
    getRecentActivities(params) {
        return request({
            url: '/records/recent-activities/',
            method: 'get',
            params
        })
    },

   
    getOverallStatistics(params) {
        return request({
            url: '/records/statistics/',
            method: 'get',
            params
        })
    }
}
