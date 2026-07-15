// 本地存储封装：Token和用户信息的持久化操作
var TOKEN_KEY = 'token'
var USER_INFO_KEY = 'userInfo'

var setToken = function(token) { wx.setStorageSync(TOKEN_KEY, token) }
var getToken = function() { return wx.getStorageSync(TOKEN_KEY) || '' }
var removeToken = function() { wx.removeStorageSync(TOKEN_KEY) }

var setUserInfo = function(userInfo) { wx.setStorageSync(USER_INFO_KEY, userInfo) }
var getUserInfo = function() { return wx.getStorageSync(USER_INFO_KEY) || null }
var removeUserInfo = function() { wx.removeStorageSync(USER_INFO_KEY) }

var clearLogin = function() { removeToken(); removeUserInfo() }

module.exports = {
    setToken: setToken,
    getToken: getToken,
    removeToken: removeToken,
    setUserInfo: setUserInfo,
    getUserInfo: getUserInfo,
    removeUserInfo: removeUserInfo,
    clearLogin: clearLogin
}