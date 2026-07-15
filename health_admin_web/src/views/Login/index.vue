<template>
    <div class="login-container">
        <el-card class="login-card">
            <template #header>
                <h2>管理员登录</h2>
            </template>
            <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="loginForm.username" placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">
                        登录
                    </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
    username: '',
    password: ''
})

const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
    ]
}

const handleLogin = async () => {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    try {
        await userStore.login(loginForm)
        ElMessage.success('登录成功')
        router.push('/')
    } catch (error) {
        ElMessage.error(error.message || '登录失败')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f0f2f5;
}

.login-card {
    width: 400px;
}

.login-card h2 {
    text-align: center;
    margin: 0;
}
</style>
