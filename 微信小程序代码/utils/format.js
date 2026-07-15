// 格式化工具：日期时间、数字、健康数据格式化
const formatDateTime = function(date, format) {
    if (!date) return ''
    const d = new Date(date)
    if (isNaN(d.getTime())) return ''
    const fmt = format || 'YYYY-MM-DD HH:mm:ss'

    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hours = String(d.getHours()).padStart(2, '0')
    const minutes = String(d.getMinutes()).padStart(2, '0')
    const seconds = String(d.getSeconds()).padStart(2, '0')

    return fmt
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds)
}

const formatDate = function(date) { return formatDateTime(date, 'YYYY-MM-DD') }
const formatTime = function(date) { return formatDateTime(date, 'HH:mm:ss') }

const friendlyTime = function(date) {
    if (!date) return ''
    const now = new Date()
    const target = new Date(date)
    const diff = now - target
    const minute = 60 * 1000
    const hour = 60 * minute
    const day = 24 * hour

    if (diff < minute) return '刚刚'
    if (diff < hour) return Math.floor(diff / minute) + '分钟前'
    if (diff < day) return Math.floor(diff / hour) + '小时前'
    if (diff < 7 * day) return Math.floor(diff / day) + '天前'
    return formatDate(date)
}

const formatNumber = function(num, decimals) {
    if (num === null || num === undefined || isNaN(num)) return '0'
    return Number(num).toFixed(decimals || 2)
}

const formatWeight = function(weight) { return formatNumber(weight, 1) + ' kg' }
const formatHeight = function(height) { return formatNumber(height, 1) + ' cm' }
const formatCalories = function(calories) { return formatNumber(calories, 0) + ' kcal' }
const formatDistance = function(distance) { return formatNumber(distance, 2) + ' km' }

const getToday = function() {
    const d = new Date()
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
}

const getDaysAgo = function(days) {
    const d = new Date()
    d.setDate(d.getDate() - days)
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
}

module.exports = {
    formatDateTime: formatDateTime,
    formatDate: formatDate,
    formatTime: formatTime,
    friendlyTime: friendlyTime,
    formatNumber: formatNumber,
    formatWeight: formatWeight,
    formatHeight: formatHeight,
    formatCalories: formatCalories,
    formatDistance: formatDistance,
    getToday: getToday,
    getDaysAgo: getDaysAgo
}