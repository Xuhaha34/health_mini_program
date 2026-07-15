// src/api/statistics.js - 数据统计接口
import request from '@/utils/request'

export default {
    // 获取平台总览数据
    getOverview() {
        return request({
            url: '/statistics/overview/',
            method: 'get'
        })
    },
    
    // 获取用户增长趋势
    getUserTrend(params) {
        return request({
            url: '/statistics/user-trend/',
            method: 'get',
            params
        })
    },
    
    // 获取健康数据分布
    getHealthDistribution(params) {
        return request({
            url: '/statistics/health-distribution/',
            method: 'get',
            params
        })
    },
    
    // 获取活跃度统计
    getActivityStats(params) {
        return request({
            url: '/statistics/activity/',
            method: 'get',
            params
        })
    }
}
