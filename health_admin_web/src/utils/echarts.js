// utils/echarts.js - ECharts 全局挂载
import * as echarts from 'echarts'

// 默认主题配置
const defaultTheme = {
    color: ['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0'],
    title: {
        textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        textStyle: {
            fontSize: 14
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    }
}

export function initChart(dom, options) {
    const chart = echarts.init(dom)
    chart.setOption({ ...defaultTheme, ...options })
    return chart
}

export default function setupEcharts() {
    // 全局挂载，组件内通过 window.$echarts 使用
    window.$echarts = echarts
    window.initChart = initChart
}
