// 资讯详情页
const { get } = require('../../utils/request')

Page({
    data: { article: null },

    onLoad: function(options) {
        if (options.id) this.loadArticle(options.id)
    },

    loadArticle: function(id) {
        const that = this
        get('/news/articles/' + id + '/').then(function(res) {
            if (res.data) {
                that.setData({ article: res.data })
                wx.setNavigationBarTitle({ title: res.data.title || '资讯详情' })
            }
        }).catch(function(err) { console.error(err) })
    }
})