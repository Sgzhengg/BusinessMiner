/**
 * RedditMiner - 前端配置文件
 */

const CONFIG = {
    // API 配置
    api: {
        baseUrl: process.env.API_URL || '/api',
        timeout: 30000,
        retryAttempts: 3,
        retryDelay: 1000,
    },

    // 应用配置
    app: {
        name: 'RedditMiner',
        version: '1.0.0',
        description: 'Reddit 商机发现平台',
        debug: process.env.NODE_ENV === 'development',
    },

    // 路由配置
    routes: {
        dashboard: {
            path: 'dashboard',
            title: '洞察仪表盘',
            icon: 'home',
        },
        'mining-config': {
            path: 'mining-config',
            title: '挖掘任务配置',
            icon: 'settings_input_component',
        },
        strategies: {
            path: 'strategies',
            title: '执行策略',
            icon: 'terminal',
        },
        'analysis-details': {
            path: 'analysis-details',
            title: '洞察分析详情',
            icon: 'analytics',
        },
        profile: {
            path: 'profile',
            title: '个人中心',
            icon: 'person',
        },
        onboarding: {
            path: 'onboarding',
            title: '智能挖掘引导',
            icon: 'rocket_launch',
        },
    },

    // UI 配置
    ui: {
        theme: 'dark',
        primaryColor: '#00E5BF',
        backgroundColor: '#0A1929',
        animationDuration: 300,
        autoRefreshInterval: 5 * 60 * 1000, // 5分钟
    },

    // 分页配置
    pagination: {
        defaultPageSize: 20,
        maxPageSize: 100,
    },

    // 缓存配置
    cache: {
        enabled: true,
        ttl: 5 * 60 * 1000, // 5分钟
        maxSize: 100, // 最大缓存条目数
    },

    // 通知配置
    notifications: {
        enabled: true,
        duration: 5000, // 显示时长
        position: 'bottom',
    },

    // 分析配置
    analytics: {
        enabled: false, // 设为 true 启用分析
        trackingId: '', // Google Analytics 跟踪 ID
    },

    // 功能开关
    features: {
        darkMode: true,
        pushNotifications: false,
        offlineMode: false,
        advancedFilters: true,
        exportData: true,
        shareFindings: true,
    },
};

// 导出配置（支持不同模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
if (typeof window !== 'undefined') {
    window.CONFIG = CONFIG;
}
