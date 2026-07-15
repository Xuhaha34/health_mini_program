// AI对话助手
const { post } = require('../../utils/request')

Page({
    data: {
        messages: [],
        input: '',
        isLoading: false,
        scrollTop: 0
    },

    onLoad: function() {
        this.setData({
            messages: [{
                id: 0, role: 'assistant',
                content: '您好！我是您的健康助手。您可以向我咨询饮食建议、运动方案、体征解读或健康科普。请随时提问。'
            }]
        })
    },

    onInput: function(e) {
        this.setData({ input: e.detail.value })
    },

    sendMessage: function() {
        const text = this.data.input.trim()
        if (!text || this.data.isLoading) return

        const userMsg = { id: Date.now(), role: 'user', content: text }
        const newMessages = this.data.messages.slice()
        newMessages.push(userMsg)
        this.setData({ messages: newMessages, input: '', isLoading: true })

        const that = this
        post('/ai/chat/', { message: text }).then(function(res) {
            const aiMsg = {
                id: Date.now() + 1,
                role: 'assistant',
                content: (res.data && res.data.response) ? res.data.response : '抱歉，我暂时无法回答。'
            }
            const msgs = that.data.messages.slice()
            msgs.push(aiMsg)
            that.setData({ messages: msgs, isLoading: false, scrollTop: 99999 })
        }).catch(function(err) {
            console.error(err)
            that.setData({ isLoading: false })
            wx.showToast({ title: 'AI服务暂不可用', icon: 'none' })
        })
    }
})