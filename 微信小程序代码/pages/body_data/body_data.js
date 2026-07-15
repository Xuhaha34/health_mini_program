// 体征记录管理：新增、编辑、删除体征数据
const { get, post, put, del } = require('../../utils/request')
const { getToday } = require('../../utils/format')

Page({
    data: {
        records: [],
        showForm: false,
        editId: null,
        form: {
            record_date: getToday(),
            weight: '', height: '',
            blood_pressure_systolic: '', blood_pressure_diastolic: '',
            heart_rate: '', blood_sugar: '', temperature: '', remark: ''
        }
    },

    onShow: function() { this.loadRecords() },

    loadRecords: function() {
        const that = this
        get('/records/body-data/', { page_size: 20 }).then(function(res) {
            if (res.data) that.setData({ records: res.data.results || [] })
        }).catch(function(err) { console.error(err) })
    },

    showAddForm: function() {
        this.setData({
            showForm: true, editId: null,
            form: {
                record_date: getToday(), weight: '', height: '',
                blood_pressure_systolic: '', blood_pressure_diastolic: '',
                heart_rate: '', blood_sugar: '', temperature: '', remark: ''
            }
        })
    },

    editRecord: function(e) {
        const item = e.currentTarget.dataset.item
        this.setData({
            showForm: true, editId: item.id,
            form: {
                record_date: item.record_date,
                weight: item.weight || '',
                height: item.height || '',
                blood_pressure_systolic: item.blood_pressure_systolic || '',
                blood_pressure_diastolic: item.blood_pressure_diastolic || '',
                heart_rate: item.heart_rate || '',
                blood_sugar: item.blood_sugar || '',
                temperature: item.temperature || '',
                remark: item.remark || ''
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

    onDateChange: function(e) {
        this.setData({ 'form.record_date': e.detail.value })
    },

    saveRecord: function() {
        const that = this
        const form = this.data.form
        const editId = this.data.editId
        const req = editId ? put('/records/body-data/' + editId + '/', form) : post('/records/body-data/', form)
        req.then(function(res) {
            wx.showToast({ title: '保存成功', icon: 'success' })
            that.setData({ showForm: false })
            that.loadRecords()
        }).catch(function(err) { console.error(err) })
    },

    deleteRecord: function(e) {
        const that = this
        const id = e.currentTarget.dataset.id
        wx.showModal({
            title: '确认删除',
            content: '确定要删除这条记录吗？',
            success: function(res) {
                if (res.confirm) {
                    del('/records/body-data/' + id + '/').then(function(res2) {
                        wx.showToast({ title: '已删除', icon: 'success' })
                        that.loadRecords()
                    }).catch(function(err) { console.error(err) })
                }
            }
        })
    },

    hideForm: function() { this.setData({ showForm: false }) }
})