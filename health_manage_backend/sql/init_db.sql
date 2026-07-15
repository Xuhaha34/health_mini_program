-- ============================================
-- 个人健康管理系统 - 数据库初始化脚本
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS health_manage_db 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE health_manage_db;

-- ============================================
-- 1. 用户表（扩展Django默认用户模型）
-- ============================================
-- Django会自动创建auth_user相关表，这里只创建扩展信息表
CREATE TABLE IF NOT EXISTS users_userinfo (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL UNIQUE COMMENT '关联Django用户ID',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    gender TINYINT DEFAULT 0 COMMENT '性别：0-未知，1-男，2-女',
    age INT COMMENT '年龄',
    height DECIMAL(5,2) COMMENT '身高(cm)',
    weight DECIMAL(5,2) COMMENT '体重(kg)',
    phone VARCHAR(20) COMMENT '手机号',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户扩展信息表';

-- ============================================
-- 2. 体征数据表
-- ============================================
CREATE TABLE IF NOT EXISTS health_record_bodydata (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    weight DECIMAL(5,2) COMMENT '体重(kg)',
    height DECIMAL(5,2) COMMENT '身高(cm)',
    blood_pressure_systolic INT COMMENT '收缩压(mmHg)',
    blood_pressure_diastolic INT COMMENT '舒张压(mmHg)',
    heart_rate INT COMMENT '心率(次/分)',
    blood_sugar DECIMAL(5,2) COMMENT '血糖(mmol/L)',
    temperature DECIMAL(4,2) COMMENT '体温(℃)',
    record_date DATE NOT NULL COMMENT '记录日期',
    remark TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_date (user_id, record_date),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='体征数据记录表';

-- ============================================
-- 3. 饮食记录表
-- ============================================
CREATE TABLE IF NOT EXISTS health_record_dietrecord (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    meal_type VARCHAR(20) NOT NULL COMMENT '餐别：breakfast/lunch/dinner/snack',
    food_name VARCHAR(200) NOT NULL COMMENT '食物名称',
    calories DECIMAL(8,2) COMMENT '热量(kcal)',
    protein DECIMAL(8,2) COMMENT '蛋白质(g)',
    fat DECIMAL(8,2) COMMENT '脂肪(g)',
    carbohydrate DECIMAL(8,2) COMMENT '碳水化合物(g)',
    portion_size VARCHAR(50) COMMENT '份量',
    record_datetime DATETIME NOT NULL COMMENT '记录时间',
    remark TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_datetime (user_id, record_datetime),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='饮食记录表';

-- ============================================
-- 4. 运动记录表
-- ============================================
CREATE TABLE IF NOT EXISTS health_record_sportrecord (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    sport_type VARCHAR(50) NOT NULL COMMENT '运动类型',
    duration INT COMMENT '运动时长(分钟)',
    distance DECIMAL(8,2) COMMENT '距离(km)',
    calories DECIMAL(8,2) COMMENT '消耗热量(kcal)',
    steps INT COMMENT '步数',
    sport_date DATE NOT NULL COMMENT '运动日期',
    remark TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_date (user_id, sport_date),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运动记录表';

-- ============================================
-- 5. 健康计划表
-- ============================================
CREATE TABLE IF NOT EXISTS health_plan_healthplan (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    title VARCHAR(200) NOT NULL COMMENT '计划标题',
    plan_type VARCHAR(50) COMMENT '计划类型：diet/sport/body/comprehensive',
    target_value VARCHAR(100) COMMENT '目标值',
    start_date DATE NOT NULL COMMENT '开始日期',
    end_date DATE NOT NULL COMMENT '结束日期',
    status TINYINT DEFAULT 0 COMMENT '状态：0-进行中，1-已完成，2-已放弃',
    description TEXT COMMENT '计划描述',
    reminder TINYINT DEFAULT 0 COMMENT '是否提醒：0-否，1-是',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_status (user_id, status),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康计划表';

-- ============================================
-- 6. 健康资讯分类表
-- ============================================
CREATE TABLE IF NOT EXISTS health_news_newscategory (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资讯分类表';

-- ============================================
-- 7. 健康资讯表
-- ============================================
CREATE TABLE IF NOT EXISTS health_news_news (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    category_id INT NOT NULL COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    cover_image VARCHAR(255) COMMENT '封面图片',
    summary TEXT COMMENT '摘要',
    content LONGTEXT NOT NULL COMMENT '内容',
    author VARCHAR(50) COMMENT '作者',
    source VARCHAR(100) COMMENT '来源',
    view_count INT DEFAULT 0 COMMENT '浏览量',
    is_published TINYINT DEFAULT 0 COMMENT '是否发布：0-草稿，1-已发布',
    published_at DATETIME COMMENT '发布时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category_published (category_id, is_published),
    INDEX idx_published_at (published_at),
    FOREIGN KEY (category_id) REFERENCES health_news_newscategory(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康资讯表';

-- ============================================
-- 8. AI对话历史表
-- ============================================
CREATE TABLE IF NOT EXISTS ai_chat_chathistory (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role VARCHAR(20) NOT NULL COMMENT '角色：user/assistant',
    message TEXT NOT NULL COMMENT '消息内容',
    session_id VARCHAR(100) COMMENT '会话ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_session (user_id, session_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI对话历史记录表';

-- ============================================
-- 完成提示
-- ============================================
SELECT '数据库表结构创建完成！' AS message;
