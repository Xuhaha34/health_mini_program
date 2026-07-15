// 登录/注册页面
const app = getApp()
const { post } = require('../../utils/request')
const { setToken, setUserInfo } = require('../../utils/storage')

Page({
    data: {
        mode: 'login',
        form: {
            username: '',
            password: '',
            email: '',
            confirm_password: ''
        }
    },

    switchMode: function(e) {
        const mode = e.currentTarget.dataset.mode
        this.setData({
            mode: mode || (this.data.mode === 'login' ? 'register' : 'login'),
            'form.username': '',
            'form.password': '',
            'form.email': '',
            'form.confirm_password': ''
        })
    },

    onInput: function(e) {
        const field = e.currentTarget.dataset.field
        const key = 'form.' + field
        const data = {}
        data[key] = e.detail.value
        this.setData(data)
    },

    onSubmit: function() {
        this.data.mode === 'login' ? this.handleLogin() : this.handleRegister()
    },

    handleLogin: function() {
        const that = this
        const username = this.data.form.username
        const password = this.data.form.password
        if (!username || !password) {
            wx.showToast({ title: '请输入用户名和密码', icon: 'none' })
            return
        }
        post('/users/login/', { username: username, password: password }).then(function(res) {
            setToken(res.data.access_token)
            app.globalData.token = res.data.access_token
            setUserInfo(res.data.user)
            app.globalData.userInfo = res.data.user
            wx.showToast({ title: '登录成功', icon: 'success' })
            wx.switchTab({ url: '/pages/index/index' })
        }).catch(function(err) {
            console.error('登录失败', err)
        })
    },

    handleRegister: function() {
        const that = this
        const form = this.data.form
        if (!form.username || !form.password) {
            wx.showToast({ title: '请填写必填项', icon: 'none' })
            return
        }
        if (form.password !== form.confirm_password) {
            wx.showToast({ title: '两次密码不一致', icon: 'none' })
            return
        }
        post('/users/register/', {
            username: form.username,
            password: form.password,
            password_confirm: form.confirm_password,
            email: form.email
        }).then(function(res) {
            wx.showToast({ title: '注册成功，请登录', icon: 'success' })
            that.setData({
                mode: 'login',
                'form.password': '',
                'form.confirm_password': ''
            })
        }).catch(function(err) {
            console.error('注册失败', err)
        })
    }
})