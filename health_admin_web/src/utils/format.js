// src/utils/format.js - 时间、数据格式化
import dayjs from 'dayjs'

/**
 * 格式化日期时间
 */
export const formatDateTime = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
    if (!date) return ''
    return dayjs(date).format(format)
}

/**
 * 格式化日期
 */
export const formatDate = (date) => {
    return formatDateTime(date, 'YYYY-MM-DD')
}

/**
 * 格式化时间
 */
export const formatTime = (date) => {
    return formatDateTime(date, 'HH:mm:ss')
}

/**
 * 友好时间显示
 */
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

/**
 * 格式化数字
 */
export const formatNumber = (num, decimals = 2) => {
    if (num === null || num === undefined || isNaN(num)) return '0'
    return Number(num).toFixed(decimals)
}

/**
 * 格式化体重
 */
export const formatWeight = (weight) => {
    return formatNumber(weight, 1) + ' kg'
}

/**
 * 格式化身高
 */
export const formatHeight = (height) => {
    return formatNumber(height, 1) + ' cm'
}

/**
 * 格式化卡路里
 */
export const formatCalories = (calories) => {
    return formatNumber(calories, 0) + ' kcal'
}

/**
 * 格式化距离
 */
export const formatDistance = (distance) => {
    return formatNumber(distance, 2) + ' km'
}
