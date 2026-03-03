# BusinessMiner - 前端架构说明

## 📁 目录结构

```
frontend/stitch-designs/
├── index.html              # 主入口文件（包含路由和导航）
├── css/
│   └── common.css          # 公共样式文件
├── js/
│   └── app.js              # 应用主逻辑（路由、API、页面初始化）
├── pages/                  # 页面组件
│   ├── dashboard.html      # 洞察仪表盘
│   ├── mining-config.html  # 挖掘任务配置
│   ├── strategies.html     # 执行策略
│   ├── analysis-details.html # 洞察分析详情
│   ├── profile.html        # 用户资料统计
│   └── onboarding.html     # 智能挖掘引导
└── assets/                 # 静态资源（图片、图标等）
```

## 🎨 设计系统

### 颜色方案
- **主色调**: `#00E5BF` (青绿色)
- **背景色**: `#0A1929` (深空蓝)
- **卡片背景**: `rgba(255, 255, 255, 0.05)` (玻璃态)
- **表面颜色**: `#132F4C` (深蓝)

### 字体
- **主要字体**: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto'
- **图标**: Material Symbols Outlined

### 设计特性
- 暗色主题
- 移动端优先
- 玻璃态效果 (Glassmorphism)
- iOS 风格导航栏
- 响应式设计

## 🚀 功能特性

### 页面路由
- 基于 Hash 的 SPA 路由
- 浏览器历史记录支持
- 页面过渡动画

### API 集成
- RESTful API 客户端
- 请求拦截和错误处理
- 自动数据刷新

### UI 组件
- 玻璃态卡片
- 霓虹边框效果
- 浮动操作按钮 (FAB)
- 底部导航栏
- 标签系统
- 加载动画

## 📱 页面说明

### 1. 洞察仪表盘 (`dashboard.html`)
- 显示统计信息（新发现、未读洞察、运行中任务）
- 最近商机发现列表
- 置信度指标
- 趋势图表

### 2. 挖掘任务配置 (`mining-config.html`)
- 运行中的挖掘任务管理
- 新建挖掘任务表单
- Subreddit 选择
- 关键词输入
- 推送频率设置
- 推送渠道选择（Slack、Email、Webhook）

### 3. 执行策略 (`strategies.html`)
- 已挖掘的洞察展示
- 方案库浏览
- 分类筛选（热门、SaaS、B2B、移动端、电子商务）
- Masonry 布局

### 4. 洞察分析详情 (`analysis-details.html`)
- 详细分析结果
- AI 生成的解决方案
- 用户评论和讨论
- 相关洞察推荐

### 5. 用户资料统计 (`profile.html`)
- 用户基本信息
- 使用统计
- 发现历史
- 收藏列表

### 6. 智能挖掘引导 (`onboarding.html`)
- 新用户引导流程
- 功能介绍
- 快速设置

## 🔧 开发指南

### 本地开发

1. 启动后端服务：
```bash
cd backend
python app.py
```

2. 访问前端：
```
http://localhost:8000/stitch-designs/
```

### 添加新页面

1. 在 `pages/` 目录创建新的 HTML 文件
2. 在 `js/app.js` 的 `routes` 对象中添加路由配置
3. 在 `initPageEvents()` 函数中添加页面初始化逻辑
4. 在底部导航栏中添加导航项（如果需要）

### API 调用

使用全局 `API` 对象进行 API 调用：

```javascript
// GET 请求
const data = await API.get('/findings');

// POST 请求
const result = await API.post('/tasks', {
    name: '新任务',
    config: {...}
});

// PUT 请求
await API.put('/tasks/1', { status: 'active' });

// DELETE 请求
await API.delete('/tasks/1');
```

### 页面导航

```javascript
// 导航到指定页面
navigateTo('dashboard');
navigateTo('mining-config');
navigateTo('strategies');
```

### 样式使用

```html
<!-- 玻璃态卡片 -->
<div class="glass-card">内容</div>

<!-- 霓虹边框 -->
<div class="neon-border">内容</div>

<!-- 主按钮 -->
<button class="btn-primary">点击</button>

<!-- 标签 -->
<span class="tag tag-primary">高需求</span>
```

## 🔄 与旧版本的兼容性

### 旧版前端
- `frontend/index.html` - 保留，作为备用版本
- 使用传统 CSS，没有路由功能

### 新版前端
- `frontend/stitch-designs/` - 推荐，现代 SPA 架构
- 使用 Tailwind CSS，具有完整路由功能

## 📊 后端 API 集成

前端需要以下 API 端点（由 FastAPI 后端提供）：

```
GET    /api/stats              # 获取统计数据
GET    /api/findings           # 获取商机发现列表
GET    /api/findings/:id       # 获取单个商机详情
POST   /api/findings           # 创建新商机
GET    /api/tasks/active       # 获取活跃任务
POST   /api/tasks              # 创建新任务
PUT    /api/tasks/:id          # 更新任务
DELETE /api/tasks/:id          # 删除任务
GET    /api/strategies         # 获取策略列表
GET    /api/analysis/:id       # 获取分析详情
GET    /api/user/profile       # 获取用户资料
GET    /api/user/stats         # 获取用户统计
```

## 🎯 后续优化建议

1. **性能优化**
   - 实现页面懒加载
   - 添加资源缓存策略
   - 优化图片加载

2. **功能增强**
   - 添加离线支持（PWA）
   - 实现推送通知
   - 添加数据导出功能

3. **用户体验**
   - 添加更多动画效果
   - 实现手势操作
   - 优化加载速度

4. **开发体验**
   - 使用构建工具（Vite/Webpack）
   - 添加 TypeScript 支持
   - 实现组件化开发

## 📝 注意事项

1. **浏览器兼容性**
   - 推荐 Chrome 90+
   - 支持 Safari 14+
   - 需要 CSS Grid 和 Flexbox 支持

2. **网络要求**
   - 需要 CDN 访问（Tailwind CSS、Google Fonts）
   - 后端 API 需要运行在 `http://localhost:8000`

3. **移动端适配**
   - 优先为移动端设计
   - 支持 iPhone 刘海屏
   - 底部安全区域适配

## 🆘 故障排除

### 页面无法加载
- 检查后端服务是否运行
- 检查控制台错误信息
- 确认 CDN 资源可访问

### API 请求失败
- 检查 API 端点是否正确
- 确认 CORS 配置
- 检查网络连接

### 样式显示异常
- 清除浏览器缓存
- 检查 Tailwind CDN 是否加载
- 确认 CSS 文件路径正确

---

**Created with ❤️ using Stitch Design**
