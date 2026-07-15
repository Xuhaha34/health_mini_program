// src/api/record.js - 健康记录管理接口
import request from '@/utils/request'

export default {
    // ==================== 体征数据 ====================
    // 获取体征数据列表
    getBodyDataList(params) {
        return request({
            url: '/records/body-data/',
            method: 'get',
            params
        })
    },
    
    // 删除体征数据
    deleteBodyData(id) {
        return request({
            url: `/records/body-data/${id}/`,
            method: 'delete'
        })
    },
    
    // 获取体征统计
    getBodyDataStats(params) {
        return request({
            url: '/records/body-data/stats/',
            method: 'get',
            params
        })
    },
    
    // ==================== 饮食记录 ====================
    // 获取饮食记录列表
    getDietList(params) {
        return request({
            url: '/records/diet/',
            method: 'get',
            params
        })
    },
    
    // 删除饮食记录
    deleteDiet(id) {
        return request({
            url: `/records/diet/${id}/`,
            method: 'delete'
        })
    },
    
    // 获取饮食统计
    getDietStats(params) {
        return request({
            url: '/records/diet/stats/',
            method: 'get',
            params
        })
    },
    
    // ==================== 运动记录 ====================
    // 获取运动记录列表
    getSportList(params) {
        return request({
            url: '/records/sport/',
            method: 'get',
            params
        })
    },
    
    // 删除运动记录
    deleteSport(id) {
        return request({
            url: `/records/sport/${id}/`,
            method: 'delete'
        })
    },
    
    // 获取运动统计
    getSportStats(params) {
        return request({
            url: '/records/sport/stats/',
            method: 'get',
            params
        })
    },

    // 获取最近活动（Dashboard）
    getRecentActivities(params) {
        return request({
            url: '/records/recent-activities/',
            method: 'get',
            params
        })
    },

    // 获取综合统计（Dashboard）
    getOverallStatistics(params) {
        return request({
            url: '/records/statistics/',
            method: 'get',
            params
        })
    }
}