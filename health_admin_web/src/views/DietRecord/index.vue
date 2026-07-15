<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="用户">
                    <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
                </el-form-item>
                <el-form-item label="餐次">
                    <el-select v-model="searchForm.mealType" placeholder="请选择餐次" clearable>
                        <el-option label="早餐" value="breakfast"></el-option>
                        <el-option label="午餐" value="lunch"></el-option>
                        <el-option label="晚餐" value="dinner"></el-option>
                        <el-option label="加餐" value="snack"></el-option>
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
                <el-table-column prop="meal_type" label="餐次" width="100">
                    <template #default="scope">
                        <el-tag>{{ getMealTypeText(scope.row.meal_type) }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="food_name" label="食物名称" min-width="200"></el-table-column>
                <el-table-column prop="calories" label="热量(千卡)" width="120"></el-table-column>
                <el-table-column prop="protein" label="蛋白质(g)" width="100"></el-table-column>
                <el-table-column prop="carbohydrate" label="碳水(g)" width="100"></el-table-column>
                <el-table-column prop="fat" label="脂肪(g)" width="100"></el-table-column>
                <el-table-column prop="record_datetime" label="记录时间" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.record_datetime) }}
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
        <el-dialog v-model="dialogVisible" title="饮食记录详情" width="500px">
            <el-descriptions :column="2" border>
                <el-descriptions-item label="用户名">{{ detailData.user_name }}</el-descriptions-item>
                <el-descriptions-item label="餐次">
                    <el-tag>{{ getMealTypeText(detailData.meal_type) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="食物名称" :span="2">{{ detailData.food_name }}</el-descriptions-item>
                <el-descriptions-item label="热量">{{ detailData.calories || '-' }} 千卡</el-descriptions-item>
                <el-descriptions-item label="蛋白质">{{ detailData.protein || '-' }} g</el-descriptions-item>
                <el-descriptions-item label="碳水化合物">{{ detailData.carbohydrate || '-' }} g</el-descriptions-item>
                <el-descriptions-item label="脂肪">{{ detailData.fat || '-' }} g</el-descriptions-item>
                <el-descriptions-item label="记录时间" :span="2">{{ formatDate(detailData.record_datetime) }}</el-descriptions-item>
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
    mealType: '',
    dateRange: []
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const detailData = reactive({})

const tableData = ref([])

const getMealTypeText = (type) => {
    const map = {
        breakfast: '早餐',
        lunch: '午餐',
        dinner: '晚餐',
        snack: '加餐'
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
    searchForm.mealType = ''
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
        
        await recordApi.deleteDiet(row.id)
        ElMessage.success('删除成功')
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || '删除失败')
        }
    }
}

const handleExport = () => {
    const exportData = tableData.value.map(item => ({
        'ID': item.id,
        '用户名': item.user_name,
        '餐次': getMealTypeText(item.meal_type),
        '食物名称': item.food_name,
        '热量(千卡)': item.calories,
        '蛋白质(g)': item.protein,
        '碳水(g)': item.carbohydrate,
        '脂肪(g)': item.fat,
        '记录时间': formatDate(item.record_datetime)
    }))

    const ws = XLSX.utils.json_to_sheet(exportData)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '饮食记录')
    XLSX.writeFile(wb, `饮食记录_${new Date().toISOString().slice(0, 10)}.xlsx`)
    
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
        
        if (searchForm.mealType) {
            params.meal_type = searchForm.mealType
        }
        
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
            params.start_date = parseDate(searchForm.dateRange[0])
            params.end_date = parseDate(searchForm.dateRange[1])
        }
        
        const res = await recordApi.getDietList(params)
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