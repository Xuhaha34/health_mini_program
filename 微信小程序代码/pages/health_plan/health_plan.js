// 健康计划管理：创建和查看健康计划
const { get, post } = require('../../utils/request')
const { getToday } = require('../../utils/format')

Page({
    data: {
        plans: [],
        showForm: false,
        planTypes: [
            { value: 'weight_loss', label: '减重' },
            { value: 'muscle_gain', label: '增肌' },
            { value: 'health_maintenance', label: '健康维护' },
            { value: 'blood_pressure', label: '血压控制' },
            { value: 'blood_sugar', label: '血糖控制' }
        ],
        form: {
            title: '',
            description: '',
            plan_type: 'weight_loss',
            start_date: getToday(),
            end_date: getToday(),
            target_weight: '',
            target_blood_pressure_systolic: '',
            target_blood_pressure_diastolic: '',
            target_blood_sugar: '',
            daily_calories: '',
            exercise_minutes: '',
            water_intake: '',
            sleep_hours: ''
        }
    },

    onShow: function() { this.loadPlans() },

    loadPlans: function() {
        const that = this
        get('/plans/', { page_size: 20 }).then(function(res) {
            if (res.data) that.setData({ plans: res.data.results || [] })
        }).catch(function(err) { console.error(err) })
    },

    showAddForm: function() {
        this.setData({
            showForm: true,
            form: {
                title: '', description: '', plan_type: 'weight_loss',
                start_date: getToday(), end_date: getToday(),
                target_weight: '', target_blood_pressure_systolic: '',
                target_blood_pressure_diastolic: '', target_blood_sugar: '',
                daily_calories: '', exercise_minutes: '',
                water_intake: '', sleep_hours: ''
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

    selectPlanType: function(e) {
        this.setData({ 'form.plan_type': e.currentTarget.dataset.type })
    },

    onStartDateChange: function(e) {
        this.setData({ 'form.start_date': e.detail.value })
    },

    onEndDateChange: function(e) {
        this.setData({ 'form.end_date': e.detail.value })
    },

    savePlan: function() {
        const that = this
        post('/plans/', this.data.form).then(function(res) {
            wx.showToast({ title: '创建成功', icon: 'success' })
            that.setData({ showForm: false })
            that.loadPlans()
        }).catch(function(err) { console.error(err) })
    },

    hideForm: function() { this.setData({ showForm: false }) }
})