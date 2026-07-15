<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="计划名称">
                    <el-input v-model="searchForm.planName" placeholder="请输入计划名称" clearable />
                </el-form-item>
                <el-form-item label="计划类型">
                    <el-select v-model="searchForm.planType" placeholder="请选择计划类型" clearable>
                        <el-option label="减重计划" value="weight_loss"></el-option>
                        <el-option label="增肌计划" value="muscle_gain"></el-option>
                        <el-option label="健康维护" value="health_maintenance"></el-option>
                        <el-option label="运动训练" value="training"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
                        <el-option label="进行中" value="active"></el-option>
                        <el-option label="已完成" value="completed"></el-option>
                        <el-option label="已暂停" value="paused"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="handleReset">重置</el-button>
                </el-form-item>
            </el-form>

            <!-- 操作按钮 -->
            <div class="toolbar">
                <el-button type="primary" @click="handleAdd">
                    <el-icon><Plus /></el-icon> 新增计划
                </el-button>
                <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
                    <el-icon><Delete /></el-icon> 批量删除
                </el-button>
            </div>

            <!-- 数据表格 -->
            <el-table 
                :data="tableData" 
                stripe 
                border
                @selection-change="handleSelectionChange"
                v-loading="loading">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="id" label="ID" width="80"></el-table-column>
                <el-table-column prop="user_name" label="用户" width="120"></el-table-column>
                <el-table-column prop="plan_name" label="计划名称" min-width="200"></el-table-column>
                <el-table-column prop="plan_type" label="计划类型" width="120">
                    <template #default="scope">
                        <el-tag>{{ getPlanTypeText(scope.row.plan_type) }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="start_date" label="开始日期" width="120"></el-table-column>
                <el-table-column prop="end_date" label="结束日期" width="120"></el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="getStatusType(scope.row.status)">
                            {{ getStatusText(scope.row.status) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="progress" label="进度" width="150">
                    <template #default="scope">
                        <el-progress :percentage="scope.row.progress" :status="getProgressStatus(scope.row.progress)" />
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" width="200">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button size="small" type="success" @click="handleView(scope.row)">详情</el-button>
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

        <!-- 编辑对话框 -->
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
                <el-form-item label="用户" prop="user_name">
                    <el-input v-model="formData.user_name" placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="计划名称" prop="plan_name">
                    <el-input v-model="formData.plan_name" placeholder="请输入计划名称" />
                </el-form-item>
                <el-form-item label="计划类型" prop="plan_type">
                    <el-select v-model="formData.plan_type" placeholder="请选择计划类型" style="width: 100%">
                        <el-option label="减重计划" value="weight_loss"></el-option>
                        <el-option label="增肌计划" value="muscle_gain"></el-option>
                        <el-option label="健康维护" value="health_maintenance"></el-option>
                        <el-option label="运动训练" value="training"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="目标描述" prop="goal">
                    <el-input v-model="formData.goal" type="textarea" :rows="3" placeholder="请输入目标描述" />
                </el-form-item>
                <el-form-item label="开始日期" prop="start_date">
                    <el-date-picker v-model="formData.start_date" type="date" placeholder="选择开始日期" style="width: 100%" />
                </el-form-item>
                <el-form-item label="结束日期" prop="end_date">
                    <el-date-picker v-model="formData.end_date" type="date" placeholder="选择结束日期" style="width: 100%" />
                </el-form-item>
                <el-form-item label="状态" prop="status">
                    <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
                        <el-option label="进行中" value="active"></el-option>
                        <el-option label="已完成" value="completed"></el-option>
                        <el-option label="已暂停" value="paused"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="进度(%)" prop="progress">
                    <el-input-number v-model="formData.progress" :min="0" :max="100" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确定</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 详情对话框 -->
        <el-dialog v-model="detailDialogVisible" title="计划详情" width="600px">
            <el-descriptions :column="2" border>
                <el-descriptions-item label="用户">{{ detailData.user_name }}</el-descriptions-item>
                <el-descriptions-item label="计划名称">{{ detailData.plan_name }}</el-descriptions-item>
                <el-descriptions-item label="计划类型">
                    <el-tag>{{ getPlanTypeText(detailData.plan_type) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="状态">
                    <el-tag :type="getStatusType(detailData.status)">{{ getStatusText(detailData.status) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="开始日期">{{ detailData.start_date }}</el-descriptions-item>
                <el-descriptions-item label="结束日期">{{ detailData.end_date }}</el-descriptions-item>
                <el-descriptions-item label="进度" :span="2">
                    <el-progress :percentage="detailData.progress" :status="getProgressStatus(detailData.progress)" />
                </el-descriptions-item>
                <el-descriptions-item label="目标描述" :span="2">{{ detailData.goal || '无' }}</el-descriptions-item>
            </el-descriptions>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import planApi from '@/api/plan'

const loading = ref(false)
const dialogVisible = ref(false)
const detailDialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const formRef = ref(null)
const selectedRows = ref([])

const searchForm = reactive({
    planName: '',
    planType: '',
    status: ''
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const formData = reactive({
    id: null,
    user_name: '',
    plan_name: '',
    plan_type: '',
    goal: '',
    start_date: '',
    end_date: '',
    status: 'active',
    progress: 0
})

const detailData = reactive({})

const rules = {
    user_name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    plan_name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
    plan_type: [{ required: true, message: '请选择计划类型', trigger: 'change' }],
    start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
    end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
}

// 真实数据
const tableData = ref([])

const getPlanTypeText = (type) => {
    const map = {
        diet: '减重计划',
        sport: '增肌计划',
        body: '健康维护',
        comprehensive: '运动训练',
        weight_loss: '减重计划',
        muscle_gain: '增肌计划',
        health_maintenance: '健康维护',
        training: '运动训练'
    }
    return map[type] || type
}

const getStatusText = (status) => {
    const map = {
        0: '进行中',
        1: '已完成',
        2: '已暂停',
        'active': '进行中',
        'completed': '已完成',
        'paused': '已暂停'
    }
    return map[status] || status
}

const getStatusType = (status) => {
    const map = {
        0: 'success',
        1: 'info',
        2: 'warning',
        'active': 'success',
        'completed': 'info',
        'paused': 'warning'
    }
    return map[status] || 'info'
}

const getProgressStatus = (progress) => {
    if (progress >= 100) return 'success'
    if (progress >= 70) return 'warning'
    return undefined
}

const handleSearch = () => {
    pagination.page = 1
    loadData()
}

const handleReset = () => {
    searchForm.planName = ''
    searchForm.planType = ''
    searchForm.status = ''
    pagination.page = 1
    loadData()
}

const handleAdd = () => {
    dialogTitle.value = '新增计划'
    isEdit.value = false
    resetForm()
    dialogVisible.value = true
}

const handleEdit = (row) => {
    dialogTitle.value = '编辑计划'
    isEdit.value = true
    Object.assign(formData, row)
    dialogVisible.value = true
}

const handleView = (row) => {
    Object.assign(detailData, row)
    detailDialogVisible.value = true
}

const handleDelete = async (row) => {
    try {
        await ElMessageBox.confirm('确定要删除该计划吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        await planApi.delete(row.id)
        ElMessage.success('删除成功')
        loadData()
    } catch (err) {
        if (err !== 'cancel') {
            ElMessage.error(err.message || '删除失败')
        }
    }
}

const handleBatchDelete = async () => {
    if (!selectedRows.value.length) {
        ElMessage.warning('请选择要删除的计划')
        return
    }
    
    try {
        await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 个计划吗？`, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        // 逐个删除
        for (const row of selectedRows.value) {
            await planApi.delete(row.id)
        }
        
        ElMessage.success('批量删除成功')
        loadData()
    } catch (err) {
        if (err !== 'cancel') {
            ElMessage.error(err.message || '批量删除失败')
        }
    }
}

const handleSelectionChange = (selection) => {
    selectedRows.value = selection
}

const handleSubmit = async () => {
    const valid = await formRef.value.validate()
    if (!valid) return

    try {
        // 格式化日期
        const submitData = {
            ...formData,
            user_id: formData.user?.id || null,
            start_date: formData.start_date instanceof Date ? formData.start_date.toISOString().split('T')[0] : formData.start_date,
            end_date: formData.end_date instanceof Date ? formData.end_date.toISOString().split('T')[0] : formData.end_date
        }
        
        if (isEdit.value) {
            await planApi.update(formData.id, submitData)
            ElMessage.success('更新成功')
        } else {
            await planApi.create(submitData)
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadData()
    } catch (error) {
        ElMessage.error(error.message || '操作失败')
    }
}

const handleSizeChange = (val) => {
    pagination.pageSize = val
    loadData()
}

const handlePageChange = (val) => {
    pagination.page = val
    loadData()
}

const resetForm = () => {
    Object.assign(formData, {
        id: null,
        user_name: '',
        plan_name: '',
        plan_type: '',
        goal: '',
        start_date: '',
        end_date: '',
        status: 'active',
        progress: 0
    })
    if (formRef.value) {
        formRef.value.clearValidate()
    }
}

const loadData = async () => {
    loading.value = true
    tableData.value = []
    pagination.total = 0
    try {
        const params = {
            page: pagination.page,
            page_size: pagination.pageSize,
            plan_name: searchForm.planName || '',
            plan_type: searchForm.planType || '',
            status: searchForm.status || ''
        }
        
        const res = await planApi.getList(params)
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

.toolbar {
    margin-bottom: 20px;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>