<template>
    <div class="dashboard-container">
        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stats-row">
            <el-col :span="6">
                <el-card shadow="hover" class="stat-card" @click="router.push('/users')">
                    <div class="stat-content">
                        <el-icon :size="40" color="#409EFF"><User /></el-icon>
                        <div class="stat-info">
                            <div class="stat-value">{{ stats.totalUsers }}</div>
                            <div class="stat-label">总用户数</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card shadow="hover" class="stat-card" @click="router.push('/body-records')">
                    <div class="stat-content">
                        <el-icon :size="40" color="#67C23A"><Monitor /></el-icon>
                        <div class="stat-info">
                            <div class="stat-value">{{ stats.bodyRecords }}</div>
                            <div class="stat-label">体征数据</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card shadow="hover" class="stat-card" @click="router.push('/diet-records')">
                    <div class="stat-content">
                        <el-icon :size="40" color="#E6A23C"><Food /></el-icon>
                        <div class="stat-info">
                            <div class="stat-value">{{ stats.dietRecords }}</div>
                            <div class="stat-label">饮食记录</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card shadow="hover" class="stat-card" @click="router.push('/sport-records')">
                    <div class="stat-content">
                        <el-icon :size="40" color="#F56C6C"><Bicycle /></el-icon>
                        <div class="stat-info">
                            <div class="stat-value">{{ stats.sportRecords }}</div>
                            <div class="stat-label">运动记录</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 图表区域 -->
        <el-row :gutter="20" class="chart-row">
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <div class="card-header">
                            <span>用户增长趋势</span>
                        </div>
                    </template>
                    <div ref="userChartRef" style="height: 300px;"></div>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card>
                    <template #header>
                        <div class="card-header">
                            <span>健康数据类型分布</span>
                        </div>
                    </template>
                    <div ref="typeChartRef" style="height: 300px;"></div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 最近活动 -->
        <el-card class="activity-card">
            <template #header>
                <div class="card-header">
                    <span>最近活动</span>
                    <el-button type="primary" size="small" @click="router.push('/body-records')">查看更多</el-button>
                </div>
            </template>
            <el-table :data="recentActivities" stripe v-loading="activityLoading">
                <el-table-column prop="time" label="时间" width="180"></el-table-column>
                <el-table-column prop="user" label="用户" width="120"></el-table-column>
                <el-table-column prop="type" label="类型" width="120">
                    <template #default="scope">
                        <el-tag :type="getTypeColor(scope.row.type)">{{ scope.row.type }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="content" label="内容"></el-table-column>
                <el-table-column label="操作" width="100">
                    <template #default="scope">
                        <el-button type="primary" link size="small" @click="router.push(scope.row.route)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { User, Monitor, Food, Bicycle } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import userApi from '@/api/user'
import recordApi from '@/api/record'

const router = useRouter()

const stats = ref({
    totalUsers: 0,
    bodyRecords: 0,
    dietRecords: 0,
    sportRecords: 0
})

const recentActivities = ref([])
const activityLoading = ref(false)

const userChartRef = ref(null)
const typeChartRef = ref(null)
let userChartInstance = null
let typeChartInstance = null

const getTypeColor = (type) => {
    const colors = {
        '体征数据': 'success',
        '饮食记录': 'warning',
        '运动记录': 'danger',
        '健康计划': 'primary'
    }
    return colors[type] || 'info'
}

const handleResize = () => {
    userChartInstance?.resize()
    typeChartInstance?.resize()
}

const initCharts = (userData, typeData) => {
    if (userChartRef.value) {
        userChartInstance = echarts.init(userChartRef.value)
        const maxCount = Math.max(...userData.counts, 1)
        userChartInstance.setOption({
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line',
                    lineStyle: { color: '#409EFF', width: 1 }
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                top: '10%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: userData.dates,
                boundaryGap: false,
                axisLine: { lineStyle: { color: '#909399' } },
                axisLabel: { color: '#606266' }
            },
            yAxis: {
                type: 'value',
                minInterval: 1,
                min: 0,
                max: Math.max(maxCount + 2, 5),
                axisLine: { lineStyle: { color: '#909399' } },
                axisLabel: { color: '#606266' },
                splitLine: { lineStyle: { color: '#EBEEF5' } }
            },
            series: [{
                name: '新增用户',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                data: userData.counts,
                itemStyle: {
                    color: '#409EFF',
                    borderColor: '#fff',
                    borderWidth: 2
                },
                lineStyle: {
                    color: '#409EFF',
                    width: 3
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(64, 158, 255, 0.35)' },
                        { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
                    ])
                }
            }]
        })
    }

    if (typeChartRef.value) {
        typeChartInstance = echarts.init(typeChartRef.value)
        typeChartInstance.setOption({
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'horizontal',
                bottom: '5%',
                left: 'center',
                textStyle: { color: '#606266' }
            },
            series: [{
                name: '数据类型',
                type: 'pie',
                radius: ['45%', '70%'],
                center: ['50%', '45%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold',
                        formatter: '{b}\n{c}'
                    }
                },
                labelLine: { show: false },
                data: typeData
            }]
        })
    }
}

onMounted(async () => {
    try {
        const [userStats, bodyRes, dietRes, sportRes] = await Promise.all([
            userApi.getStats(),
            recordApi.getBodyDataList({ page_size: 1 }),
            recordApi.getDietList({ page_size: 1 }),
            recordApi.getSportList({ page_size: 1 })
        ])

        stats.value = {
            totalUsers: userStats.data?.total_users || 0,
            bodyRecords: bodyRes.data?.count || 0,
            dietRecords: dietRes.data?.count || 0,
            sportRecords: sportRes.data?.count || 0
        }

        // 用户增长趋势（真实数据）
        const daily = userStats.data?.daily_registrations || []
        const userData = {
            dates: daily.map(d => d.date),
            counts: daily.map(d => d.count)
        }

        // 类型分布（真实数据）
        const typeData = [
            { value: stats.value.bodyRecords, name: '体征数据', itemStyle: { color: '#67C23A' } },
            { value: stats.value.dietRecords, name: '饮食记录', itemStyle: { color: '#E6A23C' } },
            { value: stats.value.sportRecords, name: '运动记录', itemStyle: { color: '#F56C6C' } },
            { value: stats.value.totalUsers, name: '用户', itemStyle: { color: '#409EFF' } }
        ]

        await nextTick()
        initCharts(userData, typeData)

        // 加载最近活动
        activityLoading.value = true
        const res = await recordApi.getRecentActivities({ limit: 10 })
        if (res.data && Array.isArray(res.data)) {
            recentActivities.value = res.data
        }
        activityLoading.value = false

        // 监听窗口大小变化
        window.addEventListener('resize', handleResize)
    } catch (error) {
        console.error('加载统计数据失败:', error)
    }
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
    userChartInstance?.dispose()
    typeChartInstance?.dispose()
})
</script>

<style scoped>
.dashboard-container {
    padding: 0;
}

.stats-row {
    margin-bottom: 20px;
}

.stat-card {
    cursor: pointer;
    transition: all 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
    display: flex;
    align-items: center;
    gap: 20px;
}

.stat-info {
    flex: 1;
}

.stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #303133;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 14px;
    color: #909399;
}

.chart-row {
    margin-bottom: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.activity-card {
    margin-top: 20px;
}
</style>