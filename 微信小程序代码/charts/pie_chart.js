// charts/pie_chart.js - 饼图配置（饮食分类）

const pieChartOption = {
    title: {
        text: '饮食营养分布',
        left: 'center',
        textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}g ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle'
    },
    series: [
        {
            name: '营养成分',
            type: 'pie',
            radius: '60%',
            data: [
                { value: 0, name: '蛋白质', itemStyle: { color: '#4CAF50' } },
                { value: 0, name: '脂肪', itemStyle: { color: '#FF9800' } },
                { value: 0, name: '碳水化合物', itemStyle: { color: '#2196F3' } }
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            label: {
                formatter: '{b}\n{d}%'
            }
        }
    ]
}

module.exports = {
    pieChartOption
}
