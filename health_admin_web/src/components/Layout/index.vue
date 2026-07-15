<template>
    <div class="layout-container">
        <el-container>
            <el-aside width="200px">
                <div class="logo">健康管理系统</div>
                <el-menu :default-active="activeMenu" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
                    <el-menu-item index="/dashboard">
                        <el-icon><DataAnalysis /></el-icon>
                        <span>数据看板</span>
                    </el-menu-item>
                    <el-menu-item index="/users">
                        <el-icon><User /></el-icon>
                        <span>用户管理</span>
                    </el-menu-item>
                    <el-sub-menu index="records">
                        <template #title>
                            <el-icon><Monitor /></el-icon>
                            <span>健康记录</span>
                        </template>
                        <el-menu-item index="/body-records">体征数据</el-menu-item>
                        <el-menu-item index="/diet-records">饮食记录</el-menu-item>
                        <el-menu-item index="/sport-records">运动记录</el-menu-item>
                    </el-sub-menu>
                    <el-menu-item index="/news">
                        <el-icon><Document /></el-icon>
                        <span>资讯管理</span>
                    </el-menu-item>
                    <el-menu-item index="/plans">
                        <el-icon><List /></el-icon>
                        <span>健康计划</span>
                    </el-menu-item>
                    <el-menu-item index="/system">
                        <el-icon><Setting /></el-icon>
                        <span>系统配置</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-container>
                <el-header>
                    <div class="header-content">
                        <h2>{{ currentTitle }}</h2>
                        <div class="user-info">
                            <el-dropdown>
                                <span class="el-dropdown-link">
                                    管理员 <el-icon><arrow-down /></el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </div>
                    </div>
                </el-header>
                <el-main>
                    <router-view :key="route.fullPath" />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { DataAnalysis, User, Monitor, Document, List, Setting, ArrowDown } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || '健康管理系统')

const handleLogout = () => {
    userStore.logout()
    router.push('/login')
}
</script>

<style scoped>
.layout-container {
    height: 100vh;
    width: 100%;
}

.el-aside {
    background-color: #304156;
    color: #fff;
    overflow-x: hidden;
}

.logo {
    height: 60px;
    line-height: 60px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #2b3a4a;
    margin-bottom: 10px;
}

.el-header {
    background-color: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
    display: flex;
    align-items: center;
    padding: 0 20px;
    height: 60px !important;
}

.header-content {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-content h2 {
    margin: 0;
    font-size: 18px;
    color: #303133;
}

.user-info {
    cursor: pointer;
}

.el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
    display: flex;
    align-items: center;
    gap: 5px;
}

.el-main {
    background-color: #f0f2f5;
    padding: 20px;
    overflow-y: auto;
}
</style>