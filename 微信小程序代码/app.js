// 小程序全局入口
App({
    onLaunch: function() {
        const token = wx.getStorageSync('token')
        if (token) {
            this.globalData.token = token
            this.checkLogin()
        }
    },

    globalData: {
        token: '',
        userInfo: null,
        baseUrl: 'http://127.0.0.1:8000/api'
    },

    checkLogin: function() {
        const that = this
        wx.request({
            url: this.globalData.baseUrl + '/users/info/',
            header: { 'Authorization': 'Bearer ' + this.globalData.token },
            success: function(res) {
                if (res.data && res.data.code === 200) {
                    that.globalData.userInfo = res.data.data
                } else {
                    that.clearLogin()
                }
            },
            fail: function() {
                that.clearLogin()
            }
        })
    },

    clearLogin: function() {
        this.globalData.token = ''
        this.globalData.userInfo = null
        wx.removeStorageSync('token')
        wx.removeStorageSync('userInfo')
    }
})