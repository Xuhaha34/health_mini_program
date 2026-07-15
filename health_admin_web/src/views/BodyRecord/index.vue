<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="用户">
                    <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
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
                <el-table-column prop="height" label="身高(cm)" width="100">
                    <template #default="scope">
                        {{ toFixed2(scope.row.height) }}
                    </template>
                </el-table-column>
                <el-table-column prop="weight" label="体重(kg)" width="100">
                    <template #default="scope">
                        {{ toFixed2(scope.row.weight) }}
                    </template>
                </el-table-column>
                <el-table-column prop="bmi" label="BMI" width="100">
                    <template #default="scope">
                        <span :class="getBmiClass(scope.row.bmi)">
                            {{ toFixed2(scope.row.bmi) }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="blood_pressure" label="血压" width="120"></el-table-column>
                <el-table-column prop="heart_rate" label="心率" width="100"></el-table-column>
                <el-table-column prop="record_date" label="记录时间" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.record_date) }}
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
        <el-dialog v-model="dialogVisible" title="体征数据详情" width="500px">
            <el-descriptions :column="2" border>
                <el-descriptions-item label="用户名">{{ detailData.user_name }}</el-descriptions-item>
                <el-descriptions-item label="记录时间">{{ formatDate(detailData.record_date) }}</el-descriptions-item>
                <el-descriptions-item label="身高">{{ detailData.height ? toFixed2(detailData.height) + ' cm' : '-' }}</el-descriptions-item>
                <el-descriptions-item label="体重">{{ detailData.weight ? toFixed2(detailData.weight) + ' kg' : '-' }}</el-descriptions-item>
                <el-descriptions-item label="BMI">
                    <el-tag :type="getBmiTagType(detailData.bmi)">{{ detailData.bmi ? toFixed2(detailData.bmi) : '-' }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="血压">{{ detailData.blood_pressure || '-' }}</el-descriptions-item>
                <el-descriptions-item label="心率">{{ detailData.heart_rate || '-' }}</el-descriptions-item>
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
    dateRange: []
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const detailData = reactive({})

const tableData = ref([])

const toFixed2 = (val) => {
    if (val === null || val === undefined || val === '') return '-'
    const n = Number(val)
    return isNaN(n) ? '-' : n.toFixed(2)
}

const getBmiClass = (bmi) => {
    if (!bmi) return ''
    if (bmi < 18.5) return 'text-warning'
    if (bmi >= 24) return 'text-danger'
    return 'text-success'
}

const getBmiTagType = (bmi) => {
    if (!bmi) return 'info'
    if (bmi < 18.5) return 'warning'
    if (bmi >= 24) return 'danger'
    return 'success'
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
        
        await recordApi.deleteBodyData(row.id)
        ElMessage.success('删除成功')
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || '删除失败')
        }
    }
}

const handleExport = () => {
    // 导出数据到Excel
    const exportData = tableData.value.map(item => ({
        'ID': item.id,
        '用户名': item.user_name,
        '身高(cm)': item.height,
        '体重(kg)': item.weight,
        'BMI': item.bmi,
        '血压': item.blood_pressure,
        '心率': item.heart_rate,
        '记录时间': item.record_date
    }))

    const ws = XLSX.utils.json_to_sheet(exportData)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '体征数据')
    XLSX.writeFile(wb, `体征数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
    
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
            username: searchForm.username || ''
        }
        
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
            params.start_date = parseDate(searchForm.dateRange[0])
            params.end_date = parseDate(searchForm.dateRange[1])
        }
        
        const res = await recordApi.getBodyDataList(params)
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

.text-success {
    color: #67C23A;
    font-weight: bold;
}

.text-warning {
    color: #E6A23C;
    font-weight: bold;
}

.text-danger {
    color: #F56C6C;
    font-weight: bold;
}
</style>