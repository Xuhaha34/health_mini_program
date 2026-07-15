// 个人中心：用户信息、统计数据、功能入口
const app = getApp()
const { get } = require('../../utils/request')
const { removeToken, removeUserInfo } = require('../../utils/storage')

Page({
    data: {
        userInfo: {},
        avatarChar: '用',
        displayName: '健康达人',
        stats: {
            records: 0,
            days: 0,
            plans: 0
        }
    },

    onShow: function() {
        const userInfo = app.globalData.userInfo
        if (userInfo) {
            const name = userInfo.nickname || userInfo.username || '健康达人'
            const char = name.charAt(0)
            this.setData({ userInfo: userInfo, avatarChar: char, displayName: name })
        }
        this.loadStats()
    },

    loadStats: function() {
        const that = this
        get('/records/statistics/', { days: 30 }).then(function(res) {
            if (res.data) {
                const s = res.data
                that.setData({
                    stats: {
                        records: (s.body && s.body.total_records) || 0,
                        days: s.total_days || 0,
                        plans: s.plans_count || 0
                    }
                })
            }
        }).catch(function(err) {
            console.error('加载统计数据失败', err)
        })
    },

    editProfile: function() {
        wx.navigateTo({ url: '/pages/profile_edit/profile_edit' })
    },

    clearCache: function() {
        wx.showModal({
            title: '清除缓存',
            content: '确定要清除所有缓存数据吗？',
            success: function(res) {
                if (res.confirm) {
                    wx.clearStorageSync()
                    wx.showToast({ title: '已清除', icon: 'success' })
                }
            }
        })
    },

    onAbout: function() {
        wx.showModal({
            title: '关于我们',
            content: '个人健康管理系统 v1.0\n科学管理健康数据，记录成长每一步。',
            showCancel: false
        })
    },

    logout: function() {
        wx.showModal({
            title: '退出登录',
            content: '确定要退出登录吗？',
            success: function(res) {
                if (res.confirm) {
                    app.clearLogin()
                    removeToken()
                    removeUserInfo()
                    wx.reLaunch({ url: '/pages/login/login' })
                }
            }
        })
    }
})