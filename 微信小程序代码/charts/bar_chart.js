// charts/bar_chart.js - 柱状图配置（运动统计）

const barChartOption = {
    title: {
        text: '运动统计',
        left: 'center',
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
        data: ['时长(分钟)', '消耗(kcal)'],
        bottom: 0
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        data: []
    },
    yAxis: {
        type: 'value',
        name: '数值'
    },
    series: [
        {
            name: '时长(分钟)',
            type: 'bar',
            data: [],
            itemStyle: {
                color: '#4CAF50'
            }
        },
        {
            name: '消耗(kcal)',
            type: 'bar',
            data: [],
            itemStyle: {
                color: '#FF9800'
            }
        }
    ]
}

module.exports = {
    barChartOption
}
