<template>
    <div class="page-container">
        <el-tabs v-model="activeTab" type="border-card">
            <!-- 系统设置 -->
            <el-tab-pane label="系统设置" name="system">
                <el-form :model="systemConfig" label-width="120px" style="max-width: 600px;">
                    <el-divider content-position="left">基础配置</el-divider>
                    <el-form-item label="系统名称">
                        <el-input v-model="systemConfig.systemName" />
                    </el-form-item>
                    <el-form-item label="系统版本">
                        <el-input v-model="systemConfig.version" disabled />
                    </el-form-item>
                    <el-form-item label="维护模式">
                        <el-switch v-model="systemConfig.maintenanceMode" active-text="开启" inactive-text="关闭" />
                    </el-form-item>
                    
                    <el-divider content-position="left">用户配置</el-divider>
                    <el-form-item label="允许注册">
                        <el-switch v-model="systemConfig.allowRegister" active-text="允许" inactive-text="禁止" />
                    </el-form-item>
                    <el-form-item label="默认头像">
                        <el-upload
                            action="#"
                            list-type="picture"
                            :auto-upload="false"
                            :limit="1"
                        >
                            <el-button type="primary">上传头像</el-button>
                        </el-upload>
                    </el-form-item>
                    
                    <el-divider content-position="left">数据配置</el-divider>
                    <el-form-item label="数据备份周期">
                        <el-select v-model="systemConfig.backupCycle" placeholder="请选择">
                            <el-option label="每天" value="daily"></el-option>
                            <el-option label="每周" value="weekly"></el-option>
                            <el-option label="每月" value="monthly"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="数据保留天数">
                        <el-input-number v-model="systemConfig.dataRetention" :min="7" :max="3650" />
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" @click="saveSystemConfig">保存配置</el-button>
                        <el-button @click="resetSystemConfig">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

            <!-- AI配置 -->
            <el-tab-pane label="AI配置" name="ai">
                <el-form :model="aiConfig" label-width="120px" style="max-width: 600px;">
                    <el-divider content-position="left">AI服务配置</el-divider>
                    <el-form-item label="启用AI功能">
                        <el-switch v-model="aiConfig.enabled" active-text="启用" inactive-text="禁用" />
                    </el-form-item>
                    <el-form-item label="API密钥">
                        <el-input v-model="aiConfig.apiKey" type="password" show-password placeholder="请输入API密钥" />
                    </el-form-item>
                    <el-form-item label="API地址">
                        <el-input v-model="aiConfig.apiUrl" placeholder="请输入API地址" />
                    </el-form-item>
                    <el-form-item label="模型选择">
                        <el-select v-model="aiConfig.model" placeholder="请选择模型">
                            <el-option label="GLM-4-Flash（智谱）" value="glm-4-flash"></el-option>
                            <el-option label="GLM-4（智谱）" value="glm-4"></el-option>
                            <el-option label="GPT-4" value="gpt-4"></el-option>
                            <el-option label="GPT-3.5" value="gpt-3.5"></el-option>
                            <el-option label="Claude" value="claude"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="最大Token数">
                        <el-input-number v-model="aiConfig.maxTokens" :min="100" :max="4000" />
                    </el-form-item>
                    <el-form-item label="响应超时(秒)">
                        <el-input-number v-model="aiConfig.timeout" :min="10" :max="120" />
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" @click="saveAiConfig">保存配置</el-button>
                        <el-button @click="testAiConnection">测试连接</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

            <!-- 邮件配置 -->
            <el-tab-pane label="邮件配置" name="email">
                <el-form :model="emailConfig" label-width="120px" style="max-width: 600px;">
                    <el-divider content-position="left">SMTP配置</el-divider>
                    <el-form-item label="启用邮件服务">
                        <el-switch v-model="emailConfig.enabled" active-text="启用" inactive-text="禁用" />
                    </el-form-item>
                    <el-form-item label="SMTP服务器">
                        <el-input v-model="emailConfig.smtpHost" placeholder="例如：smtp.example.com" />
                    </el-form-item>
                    <el-form-item label="SMTP端口">
                        <el-input-number v-model="emailConfig.smtpPort" :min="1" :max="65535" />
                    </el-form-item>
                    <el-form-item label="发件人邮箱">
                        <el-input v-model="emailConfig.fromEmail" placeholder="例如：noreply@example.com" />
                    </el-form-item>
                    <el-form-item label="发件人名称">
                        <el-input v-model="emailConfig.fromName" placeholder="例如：健康管理系统" />
                    </el-form-item>
                    <el-form-item label="用户名">
                        <el-input v-model="emailConfig.username" />
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input v-model="emailConfig.password" type="password" show-password />
                    </el-form-item>
                    <el-form-item label="使用SSL">
                        <el-switch v-model="emailConfig.useSsl" active-text="是" inactive-text="否" />
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" @click="saveEmailConfig">保存配置</el-button>
                        <el-button @click="testEmailConnection">发送测试邮件</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

            <!-- 操作日志 -->
            <el-tab-pane label="操作日志" name="logs">
                <el-table :data="logData" stripe border max-height="500">
                    <el-table-column prop="id" label="ID" width="80"></el-table-column>
                    <el-table-column prop="operator" label="操作人" width="120"></el-table-column>
                    <el-table-column prop="action" label="操作类型" width="150"></el-table-column>
                    <el-table-column prop="module" label="模块" width="120"></el-table-column>
                    <el-table-column prop="description" label="描述" min-width="200"></el-table-column>
                    <el-table-column prop="ip_address" label="IP地址" width="150"></el-table-column>
                    <el-table-column prop="created_at" label="操作时间" width="180">
                        <template #default="scope">
                            {{ formatDate(scope.row.created_at) }}
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    v-model:current-page="logPagination.page"
                    v-model:page-size="logPagination.pageSize"
                    :total="logPagination.total"
                    layout="total, prev, pager, next"
                    style="margin-top: 20px; justify-content: flex-end;"
                />
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('system')

const systemConfig = reactive({
    systemName: '健康管理系统',
    version: 'v1.0.0',
    maintenanceMode: false,
    allowRegister: true,
    backupCycle: 'weekly',
    dataRetention: 365
})

const aiConfig = reactive({
    enabled: true,
    apiKey: '4fca78aa25d2466fa8ffeb023b6f2902.6zuh2ua4Qz2tKUkR',
    apiUrl: 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    model: 'glm-4-flash',
    maxTokens: 1000,
    timeout: 30
})

const emailConfig = reactive({
    enabled: false,
    smtpHost: '',
    smtpPort: 587,
    fromEmail: '',
    fromName: '健康管理系统',
    username: '',
    password: '',
    useSsl: true
})

const logPagination = reactive({
    page: 1,
    pageSize: 20,
    total: 0
})

// 模拟日志数据
const logData = ref([
    { id: 1, operator: 'admin', action: '登录', module: '系统', description: '管理员登录系统', ip_address: '192.168.1.100', created_at: '2026-06-15 10:30:00' },
    { id: 2, operator: 'admin', action: '修改配置', module: '系统设置', description: '修改了系统名称', ip_address: '192.168.1.100', created_at: '2026-06-15 09:15:00' },
    { id: 3, operator: 'user1', action: '新增记录', module: '体征数据', description: '添加了新的体征数据', ip_address: '192.168.1.101', created_at: '2026-06-14 18:30:00' }
])

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return dateStr.replace('T', ' ').substring(0, 19)
}

const saveSystemConfig = () => {
    // TODO: 调用API保存系统配置
    ElMessage.success('系统配置保存成功')
}

const resetSystemConfig = () => {
    Object.assign(systemConfig, {
        systemName: '健康管理系统',
        version: 'v1.0.0',
        maintenanceMode: false,
        allowRegister: true,
        backupCycle: 'weekly',
        dataRetention: 365
    })
    ElMessage.info('已重置为默认配置')
}

const saveAiConfig = () => {
    // TODO: 调用API保存AI配置
    ElMessage.success('AI配置保存成功')
}

const testAiConnection = () => {
    // TODO: 调用API测试AI连接
    ElMessage.success('AI连接测试成功')
}

const saveEmailConfig = () => {
    // TODO: 调用API保存邮件配置
    ElMessage.success('邮件配置保存成功')
}

const testEmailConnection = () => {
    // TODO: 调用API发送测试邮件
    ElMessage.success('测试邮件发送成功')
}

onMounted(() => {
    logPagination.total = logData.value.length
})
</script>

<style scoped>
.page-container {
    padding: 0;
}

.el-tabs {
    min-height: 600px;
}
</style>