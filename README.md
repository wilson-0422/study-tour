# 研学实践管理系统

## 项目简介

研学实践管理系统是一个基于 Python Flask 框架开发的综合性研学旅行管理平台，旨在为学校和教育机构提供一站式的研学活动管理解决方案。系统涵盖了研学线路设计、学生报名管理、出行保险配置、食宿安排、研学成果归档和导师考核等核心功能模块。

## 技术栈

- **后端框架**：Python 3.11 + Flask 3.0
- **ORM**：Flask-SQLAlchemy 3.1
- **数据库**：SQLite
- **认证**：Flask-Login 0.6
- **模板引擎**：Jinja2
- **前端**：原生 HTML/CSS/JavaScript

## 功能模块

### 1. 研学线路设计
- 创建、编辑、删除研学线路
- 设置线路名称、目的地、行程天数、价格、最大人数
- 管理线路状态（草稿/发布）
- 查看线路详情和报名情况

### 2. 学生报名
- 学生在线报名研学线路
- 教师审核报名（通过/拒绝）
- 学生可取消待审核的报名
- 报名状态跟踪（待审核/已通过/已拒绝/已取消）

### 3. 出行保险
- 为出行学生配置保险
- 记录保险公司、保单号、保额、保费
- 管理保险期限
- 保险与报名关联

### 4. 食宿安排
- 为研学线路配置住宿信息
- 管理酒店名称、地址、入住退房日期
- 设置房型、含餐情况、人均费用

### 5. 研学成果归档
- 学生提交研学报告
- 教师在线评分（0-100分）
- 教师给出反馈意见
- 成果统计和查询

### 6. 导师考核
- 导师信息管理
- 多维度评分考核（0-10分）
- 综合评分自动计算
- 考核次数统计

### 7. 管理控制台
- 数据统计仪表盘
- 线路数量、报名总数、待审核报名
- 研学成果数、导师数量、平均成绩
- 最近报名动态
- 快捷操作入口

## 项目结构

```
repo/
├── app.py                  # 应用入口
├── config.py               # 配置文件
├── seed.py                 # 种子数据
├── requirements.txt        # 依赖清单
├── app/
│   ├── __init__.py         # 应用工厂
│   ├── models/             # 数据模型
│   │   ├── user.py         # 用户模型
│   │   ├── route.py        # 研学线路模型
│   │   ├── registration.py # 报名模型
│   │   ├── insurance.py    # 保险模型
│   │   ├── accommodation.py# 食宿模型
│   │   ├── achievement.py  # 成果模型
│   │   └── mentor.py       # 导师模型
│   ├── routes/             # 路由蓝图
│   │   ├── main.py         # 主页和仪表盘
│   │   ├── auth.py         # 认证路由
│   │   ├── routes.py       # 线路路由
│   │   ├── registrations.py# 报名路由
│   │   ├── insurances.py   # 保险路由
│   │   ├── accommodations.py# 食宿路由
│   │   ├── achievements.py # 成果路由
│   │   └── mentors.py      # 导师路由
│   ├── services/           # 业务服务层
│   │   ├── user_service.py
│   │   ├── route_service.py
│   │   ├── registration_service.py
│   │   ├── insurance_service.py
│   │   ├── accommodation_service.py
│   │   ├── achievement_service.py
│   │   └── mentor_service.py
│   ├── templates/          # Jinja2 模板
│   └── static/             # 静态资源
│       ├── css/style.css
│       └── js/main.js
```

## 快速开始

### 环境要求

- Python 3.11+
- pip

### 安装步骤

```bash
# 1. 进入项目目录
cd repo

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库和种子数据
python seed.py

# 4. 启动应用
python app.py
```

应用将在 http://localhost:5000 启动。

### Docker 部署

```bash
# 构建镜像
docker build -t study-tour .

# 运行容器
docker run -p 5000:5000 -p 2222:22 study-tour
```

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 教师 | zhanglaoshi | 123456 |
| 学生 | liming | 123456 |
| 导师 | wangdaoshi | 123456 |

## 用户角色

- **管理员（admin）**：拥有所有功能权限
- **教师（teacher）**：管理线路、审核报名、评分成果、管理保险和食宿
- **学生（student）**：浏览线路、报名、提交成果
- **导师（mentor）**：接受考核评分

## 许可证

MIT License
