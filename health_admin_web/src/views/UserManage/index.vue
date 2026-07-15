<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="用户名">
                    <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="handleReset">重置</el-button>
                </el-form-item>
            </el-form>

            <!-- 操作按钮 -->
            <div class="toolbar">
                <el-button type="primary" @click="handleAdd">
                    <el-icon><Plus /></el-icon> 新增用户
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
                <el-table-column prop="username" label="用户名" width="120"></el-table-column>
                <el-table-column prop="phone" label="手机号" width="130"></el-table-column>
                <el-table-column prop="email" label="邮箱" width="180"></el-table-column>
                <el-table-column prop="gender" label="性别" width="80">
                    <template #default="scope">
                        {{ getGenderText(scope.row.gender) }}
                    </template>
                </el-table-column>
                <el-table-column prop="age" label="年龄" width="80"></el-table-column>
                <el-table-column prop="date_joined" label="注册时间" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.date_joined) }}
                    </template>
                </el-table-column>
                <el-table-column prop="is_active" label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                            {{ scope.row.is_active ? '正常' : '禁用' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" width="200">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
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
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="80px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="formData.username" :disabled="isEdit" />
                </el-form-item>
                <el-form-item label="密码" prop="password" v-if="!isEdit">
                    <el-input v-model="formData.password" type="password" show-password />
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="formData.phone" />
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="formData.email" />
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-select v-model="formData.gender" placeholder="请选择性别">
                        <el-option label="未知" :value="0"></el-option>
                        <el-option label="男" :value="1"></el-option>
                        <el-option label="女" :value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="年龄" prop="age">
                    <el-input-number v-model="formData.age" :min="1" :max="150" />
                </el-form-item>
                <el-form-item label="身高(cm)" prop="height">
                    <el-input-number v-model="formData.height" :precision="2" :step="0.1" />
                </el-form-item>
                <el-form-item label="体重(kg)" prop="weight">
                    <el-input-number v-model="formData.weight" :precision="2" :step="0.1" />
                </el-form-item>
                <el-form-item label="状态" prop="is_active">
                    <el-switch v-model="formData.is_active" active-text="正常" inactive-text="禁用" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import userApi from '@/api/user'

const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const formRef = ref(null)
const selectedRows = ref([])

const searchForm = reactive({
    username: '',
    phone: ''
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const formData = reactive({
    id: null,
    username: '',
    password: '',
    phone: '',
    email: '',
    gender: 0,
    age: null,
    height: null,
    weight: null,
    is_active: true
})

const rules = {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const tableData = ref([])

const getGenderText = (gender) => {
    const map = { 0: '未知', 1: '男', 2: '女' }
    return map[gender] || '未知'
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
    searchForm.phone = ''
    pagination.page = 1
    loadData()
}

const handleAdd = () => {
    dialogTitle.value = '新增用户'
    isEdit.value = false
    resetForm()
    dialogVisible.value = true
}

const handleEdit = (row) => {
    dialogTitle.value = '编辑用户'
    isEdit.value = true
    Object.assign(formData, row)
    formData.password = '' // 编辑时不显示密码
    dialogVisible.value = true
}

const handleDelete = async (row) => {
    try {
        await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        await userApi.delete(row.id)
        ElMessage.success('删除成功')
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || '删除失败')
        }
    }
}

const handleBatchDelete = async () => {
    try {
        await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 个用户吗？`, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        // 批量删除
        const promises = selectedRows.value.map(row => userApi.delete(row.id))
        await Promise.all(promises)
        
        ElMessage.success('批量删除成功')
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || '批量删除失败')
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
        if (isEdit.value) {
            // 编辑用户
            await userApi.update(formData.id, formData)
            ElMessage.success('更新成功')
        } else {
            // 新增用户
            await userApi.create(formData)
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
        username: '',
        password: '',
        phone: '',
        email: '',
        gender: 0,
        age: null,
        height: null,
        weight: null,
        is_active: true
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
            username: searchForm.username || '',
            phone: searchForm.phone || ''
        }
        const res = await userApi.getList(params)
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