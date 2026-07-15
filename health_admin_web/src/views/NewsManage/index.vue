<template>
    <div class="page-container">
        <el-card>
            <!-- 搜索栏 -->
            <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="标题">
                    <el-input v-model="searchForm.title" placeholder="请输入标题" clearable />
                </el-form-item>
                <el-form-item label="分类">
                    <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
                        <el-option label="健康资讯" value="health"></el-option>
                        <el-option label="运动健身" value="sports"></el-option>
                        <el-option label="饮食营养" value="diet"></el-option>
                        <el-option label="心理健康" value="mental"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="searchForm.is_published" placeholder="请选择状态" clearable>
                        <el-option label="已发布" :value="true"></el-option>
                        <el-option label="草稿" :value="false"></el-option>
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
                    <el-icon><Plus /></el-icon> 新增资讯
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
                <el-table-column prop="title" label="标题" min-width="250"></el-table-column>
                <el-table-column prop="category" label="分类" width="120">
                    <template #default="scope">
                        <el-tag>{{ getCategoryText(scope.row.category) }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="author" label="作者" width="120"></el-table-column>
                <el-table-column prop="view_count" label="阅读量" width="100"></el-table-column>
                <el-table-column prop="is_published" label="状态" width="100">
                    <template #default="scope">
                        <el-tag :type="scope.row.is_published ? 'success' : 'info'">
                            {{ scope.row.is_published ? '已发布' : '草稿' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="publish_time" label="发布时间" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.publish_time) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" width="200">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button size="small" :type="scope.row.is_published ? 'warning' : 'success'" @click="handleToggleStatus(scope.row)">
                            {{ scope.row.is_published ? '下架' : '发布' }}
                        </el-button>
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
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="80px">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="formData.title" placeholder="请输入标题" />
                </el-form-item>
                <el-form-item label="分类" prop="category">
                    <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
                        <el-option label="健康资讯" value="health"></el-option>
                        <el-option label="运动健身" value="sports"></el-option>
                        <el-option label="饮食营养" value="diet"></el-option>
                        <el-option label="心理健康" value="mental"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="封面图" prop="cover_image">
                    <el-upload
                        action="#"
                        list-type="picture-card"
                        :auto-upload="false"
                        :limit="1"
                    >
                        <el-icon><Plus /></el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item label="摘要" prop="summary">
                    <el-input v-model="formData.summary" type="textarea" :rows="3" placeholder="请输入摘要" />
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <el-input v-model="formData.content" type="textarea" :rows="10" placeholder="请输入内容" />
                </el-form-item>
                <el-form-item label="作者" prop="author">
                    <el-input v-model="formData.author" placeholder="请输入作者" />
                </el-form-item>
                <el-form-item label="状态" prop="is_published">
                    <el-radio-group v-model="formData.is_published">
                        <el-radio :label="false">草稿</el-radio>
                        <el-radio :label="true">发布</el-radio>
                    </el-radio-group>
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
import newsApi from '@/api/news'

const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const formRef = ref(null)
const selectedRows = ref([])

const searchForm = reactive({
    title: '',
    category: '',
    status: ''
})

const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
})

const formData = reactive({
    id: null,
    title: '',
    category: '',
    cover_image: '',
    summary: '',
    content: '',
    author: '',
    is_published: false
})

const rules = {
    title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
    category: [{ required: true, message: '请选择分类', trigger: 'change' }],
    content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const tableData = ref([])

const getCategoryText = (category) => {
    const map = {
        health: '健康资讯',
        sports: '运动健身',
        diet: '饮食营养',
        mental: '心理健康'
    }
    return map[category] || category
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
    searchForm.title = ''
    searchForm.category = ''
    searchForm.status = ''
    pagination.page = 1
    loadData()
}

const handleAdd = () => {
    dialogTitle.value = '新增资讯'
    isEdit.value = false
    resetForm()
    dialogVisible.value = true
}

const handleEdit = (row) => {
    dialogTitle.value = '编辑资讯'
    isEdit.value = true
    Object.assign(formData, row)
    formData.is_published = row.is_published || false
    dialogVisible.value = true
}

const handleDelete = async (row) => {
    try {
        await ElMessageBox.confirm('确定要删除该资讯吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        await newsApi.delete(row.id)
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
        await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条资讯吗？`, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        // 批量删除
        const promises = selectedRows.value.map(row => newsApi.delete(row.id))
        await Promise.all(promises)
        
        ElMessage.success('批量删除成功')
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || '批量删除失败')
        }
    }
}

const handleToggleStatus = async (row) => {
    const action = row.is_published ? '下架' : '发布'
    try {
        await ElMessageBox.confirm(`确定要${action}该资讯吗？`, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        // 更新状态
        const updateData = { ...row, is_published: !row.is_published }
        await newsApi.update(row.id, updateData)
        
        ElMessage.success(`${action}成功`)
        loadData()
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error(error.message || `${action}失败`)
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
            // 编辑资讯
            await newsApi.update(formData.id, formData)
            ElMessage.success('更新成功')
        } else {
            // 新增资讯
            await newsApi.create(formData)
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
        title: '',
        category: '',
        cover_image: '',
        summary: '',
        content: '',
        author: '',
        is_published: false
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
            title: searchForm.title || '',
            category: searchForm.category || '',
            is_published: searchForm.is_published !== '' ? searchForm.is_published : undefined
        }
        const res = await newsApi.getManageList(params)
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