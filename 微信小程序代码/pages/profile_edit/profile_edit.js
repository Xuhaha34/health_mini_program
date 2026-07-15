// 个人资料编辑：修改用户信息
const app = getApp()
const { get, put } = require('../../utils/request')
const { setUserInfo } = require('../../utils/storage')

Page({
    data: {
        form: {
            username: '',
            phone: '',
            age: '',
            gender: '',
            height: '',
            weight: ''
        }
    },

    onLoad: function() {
        this.loadUserInfo()
    },

    loadUserInfo: function() {
        const that = this
        get('/users/info/').then(function(res) {
            if (res.data) {
                const u = res.data
                that.setData({
                    form: {
                        username: u.username || '',
                        phone: u.phone || '',
                        age: u.age || '',
                        gender: u.gender || '',
                        height: u.height || '',
                        weight: u.weight || ''
                    }
                })
            }
        }).catch(function(err) {
            console.error(err)
        })
    },

    onInput: function(e) {
        const field = e.currentTarget.dataset.field
        const key = 'form.' + field
        const data = {}
        data[key] = e.detail.value
        this.setData(data)
    },

    saveProfile: function() {
        const that = this
        const form = {
            username: this.data.form.username,
            phone: this.data.form.phone,
            age: this.data.form.age,
            gender: this.data.form.gender,
            height: this.data.form.height,
            weight: this.data.form.weight
        }
        if (!form.username) {
            wx.showToast({ title: '用户名不能为空', icon: 'none' })
            return
        }
        put('/users/info/', form).then(function(res) {
            app.globalData.userInfo = form
            setUserInfo(form)
            wx.showToast({ title: '保存成功', icon: 'success' })
            setTimeout(function() { wx.navigateBack() }, 1500)
        }).catch(function(err) {
            console.error('保存失败', err)
        })
    }
})