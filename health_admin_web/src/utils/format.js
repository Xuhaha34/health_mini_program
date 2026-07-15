// src/utils/format.js - 时间、数据格式化
import dayjs from 'dayjs'


export const formatDateTime = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
    if (!date) return ''
    return dayjs(date).format(format)
}


export const formatDate = (date) => {
    return formatDateTime(date, 'YYYY-MM-DD')
}


export const formatTime = (date) => {
    return formatDateTime(date, 'HH:mm:ss')
}


export const friendlyTime = (date) => {
    if (!date) return ''
    
    const now = dayjs()
    const target = dayjs(date)
    const diff = now.diff(target, 'second')
    
    if (diff < 60) {
        return '刚刚'
    } else if (diff < 3600) {
        return Math.floor(diff / 60) + '分钟前'
    } else if (diff < 86400) {
        return Math.floor(diff / 3600) + '小时前'
    } else if (diff < 604800) {
        return Math.floor(diff / 86400) + '天前'
    } else {
        return formatDate(date)
    }
}


export const formatNumber = (num, decimals = 2) => {
    if (num === null || num === undefined || isNaN(num)) return '0'
    return Number(num).toFixed(decimals)
}


export const formatWeight = (weight) => {
    return formatNumber(weight, 1) + ' kg'
}


export const formatHeight = (height) => {
    return formatNumber(height, 1) + ' cm'
}


export const formatCalories = (calories) => {
    return formatNumber(calories, 0) + ' kcal'
}


export const formatDistance = (distance) => {
    return formatNumber(distance, 2) + ' km'
}
