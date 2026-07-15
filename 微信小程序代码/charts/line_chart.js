// charts/line_chart.js - 折线图配置（体征趋势）

const lineChartOption = {
    title: {
        text: '体征数据趋势',
        left: 'center',
        textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
        }
    },
    tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
    },
    legend: {
        data: ['体重', '心率'],
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
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        name: '数值'
    },
    series: [
        {
            name: '体重',
            type: 'line',
            smooth: true,
            data: [],
            itemStyle: {
                color: '#4CAF50'
            }
        },
        {
            name: '心率',
            type: 'line',
            smooth: true,
            data: [],
            itemStyle: {
                color: '#FF9800'
            }
        }
    ]
}

module.exports = {
    lineChartOption
}
