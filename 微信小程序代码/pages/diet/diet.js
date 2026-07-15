// 饮食记录管理：记录每日饮食信息
const { get, post, del } = require('../../utils/request')
const { getToday } = require('../../utils/format')

Page({
    data: {
        records: [],
        showForm: false,
        mealTypes: [
            { value: 'breakfast', label: '早餐' },
            { value: 'lunch', label: '午餐' },
            { value: 'dinner', label: '晚餐' },
            { value: 'snack', label: '加餐' }
        ],
        form: {
            meal_type: 'lunch',
            food_name: '',
            portion_size: '',
            calories: '',
            protein: '',
            fat: '',
            carbohydrate: '',
            record_datetime: '',
            remark: ''
        }
    },

    onShow: function() { this.loadRecords() },

    loadRecords: function() {
        const that = this
        get('/records/diet/', { page_size: 20 }).then(function(res) {
            if (res.data) that.setData({ records: res.data.results || [] })
        }).catch(function(err) { console.error(err) })
    },

    showAddForm: function() {
        const now = new Date()
        const dt = getToday() + ' ' + String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0')
        this.setData({
            showForm: true,
            form: {
                meal_type: 'lunch',
                food_name: '', portion_size: '', calories: '',
                protein: '', fat: '', carbohydrate: '',
                record_datetime: dt, remark: ''
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

    selectMealType: function(e) {
        const type = e.currentTarget.dataset.type
        this.setData({ 'form.meal_type': type })
    },

    saveRecord: function() {
        const that = this
        post('/records/diet/', this.data.form).then(function(res) {
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
                    del('/records/diet/' + id + '/').then(function(res2) {
                        that.loadRecords()
                    }).catch(function(err) { console.error(err) })
                }
            }
        })
    },

    hideForm: function() { this.setData({ showForm: false }) }
})