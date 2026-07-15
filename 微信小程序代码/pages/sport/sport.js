// 运动记录管理：记录运动信息
const { get, post, del } = require('../../utils/request')
const { getToday } = require('../../utils/format')

Page({
    data: {
        records: [],
        showForm: false,
        sportTypes: [
            { value: 'running', label: '跑步' },
            { value: 'walking', label: '散步' },
            { value: 'cycling', label: '骑行' },
            { value: 'swimming', label: '游泳' },
            { value: 'gym', label: '健身' },
            { value: 'yoga', label: '瑜伽' },
            { value: 'basketball', label: '篮球' },
            { value: 'badminton', label: '羽毛球' }
        ],
        form: {
            sport_date: getToday(),
            sport_type: 'running',
            duration: '',
            calories: '',
            distance: '',
            steps: '',
            heart_rate: '',
            remark: ''
        }
    },

    onShow: function() { this.loadRecords() },

    loadRecords: function() {
        const that = this
        get('/records/sport/', { page_size: 20 }).then(function(res) {
            if (res.data) that.setData({ records: res.data.results || [] })
        }).catch(function(err) { console.error(err) })
    },

    showAddForm: function() {
        this.setData({
            showForm: true,
            form: {
                sport_date: getToday(),
                sport_type: 'running',
                duration: '', calories: '', distance: '',
                steps: '', heart_rate: '', remark: ''
            }
        })
    },

    onFormInput: function(e) {
        const field = e.currentTarget.dataset.field
        const key = 'form.' + field
        const data = {}
        data[key] = e.detail.value
        this.setData(data)
    },

    selectSportType: function(e) {
        this.setData({ 'form.sport_type': e.currentTarget.dataset.type })
    },

    onDateChange: function(e) {
        this.setData({ 'form.sport_date': e.detail.value })
    },

    saveRecord: function() {
        const that = this
        post('/records/sport/', this.data.form).then(function(res) {
            wx.showToast({ title: '记录成功', icon: 'success' })
            that.setData({ showForm: false })
            that.loadRecords()
        }).catch(function(err) { console.error(err) })
    },

    deleteRecord: function(e) {
        const that = this
        const id = e.currentTarget.dataset.id
        wx.showModal({
            title: '确认删除', content: '确定要删除吗？',
            success: function(res) {
                if (res.confirm) {
                    del('/records/sport/' + id + '/').then(function(res2) {
                        that.loadRecords()
                    }).catch(function(err) { console.error(err) })
                }
            }
        })
    },

    hideForm: function() { this.setData({ showForm: false }) }
})