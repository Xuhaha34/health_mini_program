// 网络请求封装：统一处理Token、错误提示、状态码
const app = getApp()

const request = function(options) {
    return new Promise(function(resolve, reject) {
        const token = wx.getStorageSync('token')
        const header = {
            'Content-Type': 'application/json'
        }
        if (options.header) {
            for (var k in options.header) header[k] = options.header[k]
        }
        if (token) header['Authorization'] = 'Bearer ' + token

        wx.request({
            url: app.globalData.baseUrl + options.url,
            method: options.method || 'GET',
            data: options.data || {},
            header: header,
            timeout: 30000,
            success: function(res) {
                if (res.statusCode === 401) {
                    app.clearLogin()
                    wx.reLaunch({ url: '/pages/login/login' })
                    reject(new Error('登录已过期'))
                    return
                }
                if (res.data && res.data.code >= 200 && res.data.code < 300) {
                    resolve(res.data)
                } else {
                    wx.showToast({ title: (res.data && res.data.message) || '请求失败', icon: 'none' })
                    reject(res.data)
                }
            },
            fail: function(err) {
                wx.showToast({ title: '网络连接失败', icon: 'none' })
                reject(err)
            }
        })
    })
}

const get = function(url, data) { return request({ url: url, method: 'GET', data: data || {} }) }
const post = function(url, data) { return request({ url: url, method: 'POST', data: data || {} }) }
const put = function(url, data) { return request({ url: url, method: 'PUT', data: data || {} }) }
const del = function(url, data) { return request({ url: url, method: 'DELETE', data: data || {} }) }

module.exports = { request: request, get: get, post: post, put: put, del: del }