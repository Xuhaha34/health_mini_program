// 首页：展示用户健康数据概览、快捷入口、最近体征记录
const { get } = require('../../utils/request')
const { getToday, getDaysAgo } = require('../../utils/format')

Page({
    data: {
        userInfo: {},
        todayStats: {
            calories_in: 0,
            calories_out: 0,
            exercise_minutes: 0,
            weight: '--',
            blood_pressure: '--',
            heart_rate: '--'
        },
        recentBodyData: []
    },

    onShow: function() {
        this.loadData()
    },

    loadData: function() {
        const app = getApp()
        if (!app.globalData.token) {
            wx.redirectTo({ url: '/pages/login/login' })
            return
        }
        this.setData({ userInfo: app.globalData.userInfo || {} })
        this.loadStats()
    },

    loadStats: function() {
        const that = this
        get('/records/statistics/', { days: 7 }).then(function(res) {
            if (res.data) {
                const s = res.data
                const weightVal = s.body && s.body.avg_weight ? Number(s.body.avg_weight).toFixed(1) : '--'
                const bpVal = s.body && s.body.avg_systolic ? String(s.body.avg_systolic) + '/' + String(s.body.avg_diastolic) : '--'
                const hrVal = s.body && s.body.avg_heart_rate ? s.body.avg_heart_rate : '--'
                that.setData({
                    todayStats: {
                        calories_in: (s.diet && s.diet.total_calories) || 0,
                        calories_out: (s.sport && s.sport.total_calories) || 0,
                        exercise_minutes: (s.sport && s.sport.total_minutes) || 0,
                        weight: weightVal,
                        blood_pressure: bpVal,
                        heart_rate: hrVal
                    }
                })
            }
        }).catch(function(err) {
            console.error('数据加载失败', err)
        })

        const that2 = this
        get('/records/body-data/', {
            page: 1, page_size: 3,
            start_date: getDaysAgo(7),
            end_date: getToday()
        }).then(function(res) {
            if (res.data) {
                const list = res.data.results || res.data || []
                that2.setData({ recentBodyData: Array.isArray(list) ? list : [] })
            }
        }).catch(function(err) {
            console.error('最近记录加载失败', err)
        })
    },

    onQuickEntry: function(e) {
        const url = e.currentTarget.dataset.url
        wx.navigateTo({ url: url })
    },

    goToBodyData: function() {
        wx.navigateTo({ url: '/pages/body_data/body_data' })
    }
})