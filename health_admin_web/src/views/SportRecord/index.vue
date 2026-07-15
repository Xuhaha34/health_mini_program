<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="用户">
                    <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
                </el-form-item>
                <el-form-item label="运动类型">
                    <el-select v-model="searchForm.sportType" placeholder="请选择运动类型" clearable>
                        <el-option label="跑步" value="running"></el-option>
                        <el-option label="游泳" value="swimming"></el-option>
                        <el-option label="骑行" value="cycling"></el-option>
                        <el-option label="健身" value="fitness"></el-option>
                        <el-option label="篮球" value="basketball"></el-option>
                        <el-option label="其他" value="other"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="日期范围">
                    <el-date-picker
                        v-model="searchForm.dateRange"
                        type="daterange"
                        range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="handleReset">重置</el-button>
                    <el-button type="success" @click="handleExport">导出Excel</el-button>
                </el-form-item>
            </el-form>

            <!-- 数据表格 -->
            <el-table :data="tableData" stripe border v-loading="loading">
                <el-table-column prop="id" label="ID" width="80"></el-table-column>
                <el-table-column prop="user_name" label="用户名" width="120"></el-table-column>
                <el-table-column prop="sport_type" label="运动类型" width="120">
                    <template #default="scope">
                        <el-tag>{{ getSportTypeText(scope.row.sport_type) }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="duration" label="时长(分钟)" width="120"></el-table-column>
                <el-table-column prop="distance" label="距离(km)" width="120">
                    <template #default="scope">
                        {{ toFixed2(scope.row.distance) }}
                    </template>
                </el-table-column>
                <el-table-column prop="calories" label="消耗热量(千卡)" width="140"></el-table-column>
                <el-table-column prop="sport_date" label="记录时间" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.sport_date) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" width="150">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="handleView(scope.row)">查看</el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.pageSize"
                :total="pagination.total"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handlePageChange"
                style="margin-top: 20px; justify-content: flex-end;"
            />
        </el-card>

        <!-- 详情对话框 -->
        <el-dialog v-model="dialogVisible" title="运动记录详情" width="500px">
            <el-descriptions :column="2" border>
                <el-descriptions-item label="用户名">{{ detailData.user_name }}</el-descriptions-item>
                <el-descriptions-item label="运动类型">
                    <el-tag>{{ getSportTypeText(detailData.sport_type) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="时长">{{ detailData.duration || '-' }} 分钟</el-descriptions-item>
                <el-descriptions-item label="距离">{{ detailData.distance ? toFixed2(detailData.distance) + ' km' : '-' }}</el-descriptions-item>
                <el-descriptions-item label="消耗热量">{{ detailData.calories || '-' }} 千卡</el-descriptions-item>
                <el-descriptions-item label="平均心率">{{ detailData.heart_rate || '-' }} 次/分</el-descriptions-item>
                <el-descriptions-item label="记录时间" :span="2">{{ formatDate(detailData.sport_date) }}</el-descriptions-item>
                <el-descriptions-item label="备注" :span="2">{{ detailData.remark || '无' }}</el-descriptions-item>
            </el-descriptions>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx'
import recordApi from '@/api/record'

const loading = ref(false)
const dialogVisible = ref(false)

const searchForm = reactive({
    username: '',
    sportType: '',
    dateRange: []
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const detailData = reactive({})

// 真实数据
const tableData = ref([])

const toFixed2 = (val) => {
    if (val === null || val === undefined || val === '') return '-'
    const n = Number(val)
    return isNaN(n) ? '-' : n.toFixed(2)
}

const getSportTypeText = (type) => {
    const map = {
        running: '跑步',
        swimming: '游泳',
        cycling: '骑行',
        fitness: '健身',
        basketball: '篮球',
        other: '其他'
    }
    return map[type] || type
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return dateStr.replace('T', ' ').substring(0, 19)
}

const handleSearch = () => {
    pagination.page = 1
    loadData()
}

const handleReset = () => {
    searchForm.username = ''
    searchForm.sportType = ''
    searchForm.dateRange = []
    pagination.page = 1
    loadData()
}

const handleView = (row) => {
    Object.assign(detailData, row)
    dialogVisible.value = true
}

const handleDelete = async (row) => {
    try {
        await ElMessageBox.confirm('确定要删除该记录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        await recordApi.deleteSport(row.id)
        ElMessage.success('删除成功')
        loadData()
    } catch (err) {
        if (err !== 'cancel') {
            ElMessage.error(err.message || '删除失败')
        }
    }
}

const handleExport = () => {
    if (!tableData.value.length) {
        ElMessage.warning('没有数据可导出')
        return
    }
    
    const exportData = tableData.value.map(item => ({
        'ID': item.id,
        '用户名': item.user_name || '-',
        '运动类型': getSportTypeText(item.sport_type),
        '时长(分钟)': item.duration,
        '距离(km)': item.distance,
        '消耗热量(千卡)': item.calories,
        '平均心率': item.heart_rate,
        '记录时间': formatDate(item.sport_date)
    }))

    const ws = XLSX.utils.json_to_sheet(exportData)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '运动记录')
    XLSX.writeFile(wb, `运动记录_${new Date().toISOString().slice(0, 10)}.xlsx`)
    
    ElMessage.success('导出成功')
}

const handleSizeChange = (val) => {
    pagination.pageSize = val
    loadData()
}

const handlePageChange = (val) => {
    pagination.page = val
    loadData()
}

const parseDate = (d) => {
    if (!d) return ''
    if (d instanceof Date) return d.toISOString().split('T')[0]
    if (typeof d === 'string') return d.split('T')[0]
    return String(d)
}

const loadData = async () => {
    loading.value = true
    tableData.value = []
    pagination.total = 0
    try {
        const params = {
            page: pagination.page,
            page_size: pagination.pageSize,
            username: searchForm.username || '',
            sport_type: searchForm.sportType || ''
        }
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
            params.start_date = parseDate(searchForm.dateRange[0])
            params.end_date = parseDate(searchForm.dateRange[1])
        }
        
        const res = await recordApi.getSportList(params)
        if (res.data && res.data.results) {
            tableData.value = res.data.results
            pagination.total = res.data.count || 0
        } else if (Array.isArray(res.data)) {
            tableData.value = res.data
            pagination.total = res.data.length
        }
    } catch (error) {
        ElMessage.error(error.message || '加载数据失败')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadData()
})
</script>

<style scoped>
.page-container {
    padding: 0;
}

.search-form {
    margin-bottom: 20px;
}
</style>