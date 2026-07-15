// 资讯列表：分类筛选、搜索、分页加载
const { get } = require('../../utils/request')

Page({
    data: {
        articles: [],
        categories: [],
        currentCategory: '',
        keyword: '',
        page: 1,
        hasMore: true
    },

    onShow: function() {
        this.loadCategories()
        this.loadArticles(true)
    },

    loadCategories: function() {
        const that = this
        get('/news/categories/').then(function(res) {
            if (res.data) that.setData({ categories: res.data })
        }).catch(function(err) { console.error(err) })
    },

    loadArticles: function(reset) {
        const that = this
        const page = reset ? 1 : this.data.page + 1
        const params = { page: page, page_size: 10 }
        if (this.data.currentCategory) params.category = this.data.currentCategory
        if (this.data.keyword) params.keyword = this.data.keyword

        get('/news/articles/', params).then(function(res) {
            if (res.data && res.data.results) {
                const articles = reset ? res.data.results : that.data.articles.concat(res.data.results)
                that.setData({
                    articles: articles,
                    page: page,
                    hasMore: page < res.data.total_pages
                })
            }
        }).catch(function(err) { console.error(err) })
    },

    onSearchInput: function(e) { this.setData({ keyword: e.detail.value }) },
    onSearch: function() { this.loadArticles(true) },

    onCategoryTap: function(e) {
        const id = e.currentTarget.dataset.id
        this.setData({ currentCategory: id === this.data.currentCategory ? '' : id })
        this.loadArticles(true)
    },

    onArticleTap: function(e) {
        const id = e.currentTarget.dataset.id
        wx.navigateTo({ url: '/pages/news_detail/news_detail?id=' + id })
    },

    onReachBottom: function() {
        if (this.data.hasMore) this.loadArticles()
    }
})