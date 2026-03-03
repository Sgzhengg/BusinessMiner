# 🚀 BusinessMiner 前端快速启动指南

## 📋 前置条件

1. 后端服务已启动（FastAPI 运行在 http://localhost:8000）
2. 现代浏览器（Chrome 90+, Safari 14+, Firefox 88+）
3. 网络连接（需要访问 CDN 资源）

## 🌐 访问前端

### 方法一：直接访问
启动后端服务后，访问：
```
http://localhost:8000/stitch-designs/
```

### 方法二：使用本地服务器
如果需要独立运行前端：

```bash
# 进入前端目录
cd frontend/stitch-designs

# 使用 Python 启动简单 HTTP 服务器
python -m http.server 8080

# 或使用 Node.js 的 http-server
npx http-server -p 8080

# 访问 http://localhost:8080
```

**注意**: 如果使用独立服务器，需要修改 `js/app.js` 中的 API baseUrl：

```javascript
// 将 baseUrl 从 '/api' 改为 'http://localhost:8000/api'
const API = {
    baseUrl: 'http://localhost:8000/api',
    // ...
};
```

## 📱 页面导航

底部导航栏提供四个主要入口：

| 图标 | 名称 | 功能 |
|------|------|------|
| 🏠 | 首页 | 查看统计信息和最近商机发现 |
| ⚙️ | 挖掘配置 | 配置和管理 Reddit 挖掘任务 |
| 📋 | 方案 | 浏览已生成的解决方案和策略 |
| 👤 | 我的 | 查看个人资料和使用统计 |

## 🔧 配置说明

### API 配置
编辑 `js/app.js` 文件：

```javascript
const API = {
    baseUrl: '/api', // 修改为你的 API 地址
    // ...
};
```

### 主题配置
编辑 `index.html` 中的 Tailwind 配置：

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                "primary": "#00E5BF",  // 主色调
                "deep-space": "#0A1929", // 背景色
                // ...
            },
        },
    },
}
```

## 🧪 测试 API 连接

在浏览器控制台运行：

```javascript
// 测试 API 连接
API.get('/health').then(console.log).catch(console.error);

// 获取商机列表
API.get('/findings?limit=5').then(console.log).catch(console.error);
```

## 🐛 常见问题

### 1. 页面显示"正在加载..."但不跳转
- 检查浏览器控制台错误
- 确认 `js/app.js` 文件路径正确
- 检查 CDN 资源是否可访问

### 2. API 请求失败
- 确认后端服务正在运行
- 检查 API baseUrl 配置
- 查看浏览器网络面板请求详情

### 3. 页面样式错乱
- 清除浏览器缓存
- 检查 Tailwind CDN 是否加载
- 确认 CSS 文件路径正确

### 4. 点击导航无反应
- 检查浏览器控制台是否有 JavaScript 错误
- 确认页面路由配置正确
- 尝试手动输入 URL（如 `#dashboard`）

## 📊 开发者工具

### 查看当前路由
```javascript
console.log('当前页面:', currentPage);
console.log('历史记录:', navigationHistory);
```

### 手动导航
```javascript
navigateTo('dashboard');      // 跳转到首页
navigateTo('mining-config');  // 跳转到挖掘配置
navigateTo('strategies');     // 跳转到方案
navigateTo('profile');        // 跳转到个人中心
```

### 直接访问特定页面
在 URL 后添加 hash：
```
http://localhost:8000/stitch-designs/#dashboard
http://localhost:8000/stitch-designs/#mining-config
http://localhost:8000/stitch-designs/#strategies
```

## 🎨 自定义样式

### 修改主色调
编辑 `css/common.css`：

```css
:root {
    --primary: #00E5BF; /* 修改为你想要的颜色 */
    /* ... */
}
```

### 添加新样式
在 `css/common.css` 末尾添加：

```css
.my-custom-class {
    /* 你的样式 */
}
```

## 🚀 下一步

1. **查看前端架构说明**: 阅读 [README.md](./README.md)
2. **了解 API 端点**: 访问 http://localhost:8000/docs
3. **定制页面**: 修改 `pages/` 目录下的 HTML 文件
4. **扩展功能**: 在 `js/app.js` 中添加新的功能

## 📚 相关文档

- [前端架构说明](./README.md)
- [项目主 README](../../README.md)
- [API 文档](http://localhost:8000/docs)

---

**💡 提示**: 首次访问时，浏览器会从 CDN 加载 Tailwind CSS 和 Google Fonts，可能需要几秒钟时间。后续访问会使用浏览器缓存，速度会更快。
