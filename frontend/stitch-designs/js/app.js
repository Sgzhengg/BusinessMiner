/**
 * RedditMiner - 前端应用路由和导航
 */

// 页面路由配置
const routes = {
    '': 'pages/dashboard.html',
    'dashboard': 'pages/dashboard.html',
    'mining-config': 'pages/mining-config.html',
    'strategies': 'pages/strategies.html',
    'analysis-details': 'pages/analysis-details.html',
    'chat': 'pages/chat.html',
    'profile': 'pages/profile.html',
    'onboarding': 'pages/onboarding.html'
};

// 当前页面状态
let currentPage = 'dashboard';
let navigationHistory = [];
let autoRefreshInterval = null;

/**
 * 初始化应用
 */
function initApp() {
    console.log('🚀 RedditMiner 正在初始化...');

    // 初始化设备ID
    const deviceId = initDeviceId();
    console.log('✓ 设备ID已初始化');

    // 从 URL 获取当前页面
    const hash = window.location.hash.slice(1) || 'dashboard';
    navigateTo(hash, false);

    // 监听浏览器后退按钮
    window.addEventListener('popstate', (event) => {
        if (event.state && event.state.page) {
            loadPage(event.state.page, false);
        }
    });

    // 初始化 API 请求拦截器
    initAPI();

    console.log('✓ 应用初始化完成');
}

/**
 * 导航到指定页面
 * @param {string} pageName - 页面名称
 * @param {boolean} addToHistory - 是否添加到历史记录
 * @param {object} params - URL参数
 */
function navigateTo(pageName, addToHistory = true, params = {}) {
    if (routes[pageName]) {
        if (addToHistory) {
            navigationHistory.push(currentPage);
            const url = `#${pageName}`;
            window.history.pushState({ page: pageName }, '', url);
        }
        loadPage(pageName, false, params);
    } else {
        console.error(`❌ 页面 ${pageName} 不存在`);
    }
}

/**
 * 加载页面内容
 * @param {string} pageName - 页面名称
 * @param {boolean} addToHistory - 是否添加到历史记录
 * @param {object} params - URL参数
 */
async function loadPage(pageName, addToHistory = true, params = {}) {
    const pagePath = routes[pageName];
    if (!pagePath) return;

    // 显示加载状态
    showLoading();

    try {
        const response = await fetch(pagePath);
        if (!response.ok) {
            throw new Error(`无法加载页面: ${response.status}`);
        }

        const html = await response.text();
        const mainContent = document.getElementById('main-content');

        if (mainContent) {
            mainContent.innerHTML = html;
            currentPage = pageName;

            // 初始化页面事件
            initPageEvents(pageName, params);

            // 更新导航栏激活状态
            updateNavigation();

            // 添加页面过渡动画
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(20px)';
            setTimeout(() => {
                mainContent.style.transition = 'all 0.3s ease-out';
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 50);
        }
    } catch (error) {
        console.error('❌ 加载页面失败:', error);
        showErrorPage(error.message);
    }
}

/**
 * 显示加载状态
 */
function showLoading() {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        mainContent.innerHTML = `
            <div class="flex items-center justify-center min-h-screen">
                <div class="text-center">
                    <div class="loading-spinner mx-auto mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                </div>
            </div>
        `;
    }
}

/**
 * 初始化页面特定事件
 * @param {string} pageName - 页面名称
 * @param {object} params - URL参数
 */
function initPageEvents(pageName, params = {}) {
    console.log(`📄 初始化页面: ${pageName}`);

    // 清除之前的自动刷新
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }

    // 添加页面特定的事件监听器
    switch (pageName) {
        case 'dashboard':
            initDashboard();
            break;
        case 'mining-config':
            initMiningConfig();
            break;
        case 'strategies':
            initStrategies(params);
            break;
        case 'analysis-details':
            initAnalysisDetails(params);
            break;
        case 'chat':
            initChat(params);
            break;
        case 'profile':
            initProfile();
            break;
        case 'onboarding':
            initOnboarding();
            break;
    }
}

/**
 * 初始化仪表板页面
 */
async function initDashboard() {
    console.log('📊 加载仪表板数据...');

    // 更新日期显示
    updateDateDisplay();

    // 加载数据
    await Promise.all([
        loadStats(),
        loadRecentFindings()
    ]);

    // 设置自动刷新
    setupAutoRefresh();
}

/**
 * 更新日期显示
 */
function updateDateDisplay() {
    const dateElement = document.querySelector('[data-date]');
    if (dateElement) {
        const now = new Date();
        const options = { month: 'long', day: 'numeric', weekday: 'long' };
        dateElement.textContent = now.toLocaleDateString('zh-CN', options);
    }
}

/**
 * 初始化挖掘配置页面
 */
function initMiningConfig() {
    console.log('⚙️ 加载挖掘配置...');
    // 暂时显示占位内容
    showPlaceholder('挖掘任务配置功能开发中...');
}

/**
 * 初始化策略页面
 */
async function initStrategies(params = {}) {
    console.log('📋 加载策略列表...');
    await loadStrategies(params);
}

/**
 * 初始化分析详情页面
 */
async function initAnalysisDetails(params = {}) {
    const findingId = params.id;

    if (!findingId) {
        showError('缺少商机ID参数');
        return;
    }

    console.log(`🔍 加载商机详情: ${findingId}`);
    await loadFindingDetail(findingId);
}

/**
 * 初始化聊天页面
 */
async function initChat(params = {}) {
    const findingId = params.findingId;
    const sessionId = params.sessionId;

    console.log(`💬 初始化聊天: finding=${findingId}, session=${sessionId}`);
    await initChatSession(findingId, sessionId);
}

/**
 * 初始化个人资料页面
 */
async function initProfile() {
    console.log('👤 加载用户资料...');
    await loadUserProfile();
}

/**
 * 初始化引导页面
 */
function initOnboarding() {
    console.log('🎯 显示引导流程...');
    setupOnboardingWizard();
}

/**
 * 更新导航栏激活状态
 */
function updateNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        const href = item.getAttribute('href')?.slice(1) || '';
        if (href === currentPage) {
            item.classList.add('active');
            item.classList.remove('text-slate-500');
        } else {
            item.classList.remove('active');
            item.classList.add('text-slate-500');
        }
    });
}

/**
 * 显示错误页面
 */
function showErrorPage(message = '页面加载失败') {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        mainContent.innerHTML = `
            <div class="flex items-center justify-center min-h-screen px-4">
                <div class="text-center">
                    <div class="text-6xl mb-4">⚠️</div>
                    <h2 class="text-xl font-bold mb-2">出错了</h2>
                    <p class="text-slate-400 mb-4">${message}</p>
                    <button onclick="navigateTo('dashboard')" class="btn-primary">
                        返回首页
                    </button>
                </div>
            </div>
        `;
    }
}

/**
 * 显示错误提示
 */
function showError(message) {
    console.error('❌ 错误:', message);
    alert(message); // 简单提示，可以改进为 toast
}

/**
 * 显示占位内容
 */
function showPlaceholder(message) {
    console.log('ℹ️', message);
}

/**
 * API 请求配置
 */
const API = {
    baseUrl: '/api',

    /**
     * 基础请求方法
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const deviceId = getDeviceId();

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Device-ID': deviceId,
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('资源不存在');
                } else if (response.status === 500) {
                    throw new Error('服务器错误');
                } else {
                    throw new Error(`API 请求失败: ${response.status}`);
                }
            }

            return await response.json();
        } catch (error) {
            console.error('❌ API 请求错误:', error);
            throw error;
        }
    },

    get(endpoint) {
        return this.request(endpoint);
    },

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    patch(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },

    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE',
        });
    },
};

/**
 * 初始化 API
 */
function initAPI() {
    window.API = API;
    console.log('✓ API 已初始化');
}

/**
 * 数据加载函数
 */

// 加载统计数据
async function loadStats() {
    try {
        // 从 findings 数据计算统计
        const findings = await API.get('/findings?limit=1000');

        const stats = {
            total: findings.length,
            new: findings.filter(f => f.status === 'new').length,
            researching: findings.filter(f => f.status === 'researching').length,
            completed: findings.filter(f => f.status === 'completed').length,
        };

        updateStatsUI(stats);
    } catch (error) {
        console.error('❌ 加载统计数据失败:', error);
        updateStatsUI({ total: 0, new: 0, researching: 0, completed: 0 });
    }
}

// 加载最近发现
async function loadRecentFindings() {
    try {
        const findings = await API.get('/findings?limit=10&status=new');
        updateFindingsUI(findings);
    } catch (error) {
        console.error('❌ 加载发现数据失败:', error);
        showFindingsError();
    }
}

// 加载策略列表
async function loadStrategies(params = {}) {
    try {
        const findings = await API.get('/findings?limit=50');

        // 筛选有解决方案的
        const strategies = findings.filter(f =>
            f.potential_solutions && f.potential_solutions.length > 0
        );

        updateStrategiesUI(strategies);
    } catch (error) {
        console.error('❌ 加载策略数据失败:', error);
    }
}

// 加载商机详情
async function loadFindingDetail(findingId) {
    try {
        const finding = await API.get(`/findings/${findingId}`);
        updateFindingDetailUI(finding);
    } catch (error) {
        console.error('❌ 加载商机详情失败:', error);
        showError('无法加载商机详情');
    }
}

// 加载用户资料
async function loadUserProfile() {
    try {
        // 暂时使用设备信息
        const deviceInfo = getDeviceInfo();
        updateUserProfileUI(deviceInfo);
    } catch (error) {
        console.error('❌ 加载用户资料失败:', error);
    }
}

/**
 * UI 更新函数
 */

// 更新统计UI
function updateStatsUI(stats) {
    // 更新仪表板统计卡片
    const statsMap = {
        'totalFindings': stats.total,
        'newFindings': stats.new,
        'researchingFindings': stats.researching,
        'completedFindings': stats.completed,
    };

    for (const [id, value] of Object.entries(statsMap)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    // 也更新 data-stat 属性的元素
    const elements = document.querySelectorAll('[data-stat]');
    elements.forEach(el => {
        const statKey = el.getAttribute('data-stat');
        if (stats[statKey] !== undefined) {
            el.textContent = stats[statKey];
        }
    });
}

// 更新商机列表UI
function updateFindingsUI(findings) {
    const container = document.querySelector('.space-y-4');
    if (!container) return;

    if (!findings || findings.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12">
                <div class="text-4xl mb-4">🔍</div>
                <p class="text-slate-400">暂无新发现</p>
            </div>
        `;
        return;
    }

    container.innerHTML = findings.slice(0, 5).map(finding => {
        const confidence = Math.floor(Math.random() * 20) + 80; // 模拟置信度
        const hoursAgo = Math.floor(Math.random() * 24) + 1;

        return `
            <div class="glass-card rounded-2xl p-4 cursor-pointer hover:scale-[0.98] transition-transform"
                 onclick="window.viewFinding(${finding.id})">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="text-white font-bold text-[17px] leading-snug flex-1 pr-4">
                        ${escapeHtml(finding.pain_point?.substring(0, 50) || '无标题')}
                    </h4>
                    <div class="bg-primary/10 border border-primary/20 text-primary px-2 py-0.5 rounded-md text-[11px] font-bold">
                        ${confidence}% 置信度
                    </div>
                </div>
                <div class="flex items-center gap-3 mb-4">
                    <div class="flex items-center gap-1 bg-white/5 px-2 py-0.5 rounded-full">
                        <span class="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
                        <span class="text-slate-300 text-[11px] font-medium">Reddit</span>
                    </div>
                    <span class="text-slate-500 text-[11px]">${hoursAgo}小时前</span>
                </div>
            </div>
        `;
    }).join('');
}

// 更新策略列表UI
function updateStrategiesUI(strategies) {
    const container = document.querySelector('.masonry-grid');
    if (!container) return;

    if (!strategies || strategies.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="text-4xl mb-4">📋</div>
                <p class="text-slate-400">暂无策略方案</p>
                <p class="text-slate-500 text-sm mt-2">分析商机后将自动生成策略</p>
            </div>
        `;
        return;
    }

    container.innerHTML = strategies.map(strategy => {
        const solutions = strategy.potential_solutions || [];
        const firstSolution = solutions[0] || '';

        return `
            <div class="break-inside-avoid bg-surface-dark/40 border border-primary/10 rounded-xl overflow-hidden shadow-xl cursor-pointer hover:scale-[0.98] transition-transform"
                 onclick="window.viewFinding(${strategy.id})">
                <div class="p-4 pt-6">
                    <div class="flex gap-2 mb-2">
                        <span class="bg-primary/20 text-primary text-[10px] font-bold px-2 py-0.5 rounded uppercase">推荐</span>
                        <span class="bg-slate-700/50 text-slate-300 text-[10px] font-bold px-2 py-0.5 rounded uppercase">
                            ${strategy.status === 'completed' ? '已完成' : '研究中'}
                        </span>
                    </div>
                    <h3 class="text-lg font-bold mb-2">${escapeHtml(strategy.pain_point?.substring(0, 30) || '无标题')}</h3>
                    <p class="text-slate-400 text-sm leading-relaxed mb-4">
                        ${escapeHtml(firstSolution.substring(0, 100))}...
                    </p>
                    <div class="flex gap-2">
                        <button class="flex-1 bg-primary text-background-dark text-sm font-bold py-2.5 rounded-lg">
                            查看详情
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// 更新商机详情UI
function updateFindingDetailUI(finding) {
    // 更新标题
    const titleElement = document.querySelector('[data-finding-title]');
    if (titleElement) {
        titleElement.textContent = finding.pain_point || '无标题';
    }

    // 更新痛点描述
    const painPointElement = document.querySelector('[data-pain-point]');
    if (painPointElement) {
        painPointElement.textContent = finding.pain_point || '暂无';
    }

    // 更新商机描述
    const opportunityElement = document.querySelector('[data-opportunity]');
    if (opportunityElement) {
        opportunityElement.textContent = finding.opportunity || '暂无';
    }

    // 更新目标用户
    const targetUserElement = document.querySelector('[data-target-user]');
    if (targetUserElement) {
        targetUserElement.textContent = finding.target_user || '未指定';
    }

    // 更新状态
    const statusElement = document.querySelector('[data-status]');
    if (statusElement) {
        const statusMap = {
            'new': '新发现',
            'researching': '研究中',
            'completed': '已完成'
        };
        statusElement.textContent = statusMap[finding.status] || finding.status;
    }

    // 更新解决方案
    const solutionsElement = document.querySelector('[data-solutions]');
    if (solutionsElement && finding.potential_solutions) {
        solutionsElement.innerHTML = finding.potential_solutions.map(solution => `
            <div class="bg-white/5 rounded-lg p-4 mb-3">
                <p class="text-slate-300">${escapeHtml(solution)}</p>
            </div>
        `).join('');
    }

    // 设置按钮事件
    const generateBtn = document.querySelector('[data-action="generate-solutions"]');
    if (generateBtn) {
        generateBtn.onclick = async () => {
            try {
                generateBtn.disabled = true;
                generateBtn.textContent = '生成中...';

                await API.post(`/findings/${finding.id}/generate-solutions`);

                // 重新加载详情
                await loadFindingDetail(finding.id);

                alert('✓ 解决方案已生成');
            } catch (error) {
                alert('生成失败: ' + error.message);
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = '生成解决方案';
            }
        };
    }

    // 开始研究按钮
    const researchBtn = document.querySelector('[data-action="start-research"]');
    if (researchBtn) {
        researchBtn.onclick = () => {
            // 导航到聊天页面
            navigateTo('chat', true, { findingId: finding.id });
        };
    }
}

// 更新用户资料UI
function updateUserProfileUI(deviceInfo) {
    // 更新用户名
    const nameElement = document.querySelector('[data-user-name]');
    if (nameElement) {
        nameElement.textContent = `用户 ${deviceInfo.deviceId.substring(0, 8)}`;
    }

    // 更新设备ID
    const deviceIdElement = document.querySelector('[data-device-id]');
    if (deviceIdElement) {
        deviceIdElement.textContent = deviceInfo.deviceId;
    }
}

// 显示商机加载错误
function showFindingsError() {
    const container = document.querySelector('.space-y-4');
    if (container) {
        container.innerHTML = `
            <div class="text-center py-12">
                <div class="text-4xl mb-4">❌</div>
                <p class="text-slate-400">加载失败</p>
                <button onclick="loadRecentFindings()" class="mt-4 text-primary text-sm">
                    点击重试
                </button>
            </div>
        `;
    }
}

/**
 * 工具函数
 */

// HTML转义
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 格式化时间
function formatTime(timestamp) {
    if (!timestamp) return '未知';

    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
    return `${Math.floor(diff / 86400000)}天前`;
}

// 设置自动刷新
function setupAutoRefresh() {
    autoRefreshInterval = setInterval(() => {
        if (currentPage === 'dashboard') {
            loadStats();
            loadRecentFindings();
        }
    }, 5 * 60 * 1000); // 每5分钟刷新一次
}

// 设置任务表单
function setupTaskForm() {
    // TODO: 实现任务表单提交
}

// 设置筛选标签
function setupFilterTabs() {
    // TODO: 实现筛选功能
}

// 设置引导流程
function setupOnboardingWizard() {
    // TODO: 实现引导流程
}

/**
 * 全局函数
 */

// 查看商机详情
window.viewFinding = function(findingId) {
    navigateTo('analysis-details', true, { id: findingId });
};

// 刷新当前页面
window.refreshPage = function() {
    if (currentPage) {
        initPageEvents(currentPage);
    }
};

/**
 * 聊天相关函数
 */

async function initChatSession(findingId, sessionId) {
    try {
        let session;

        if (sessionId) {
            // 加载现有会话
            const sessions = await API.get('/chat/sessions');
            session = sessions.find(s => s.id === parseInt(sessionId));
        }

        if (!session && findingId) {
            // 创建新会话
            session = await API.post(`/findings/${findingId}/chat`, {
                title: '深度研究'
            });
        }

        if (session) {
            updateChatUI(session);
            await loadChatMessages(session.id);
        }
    } catch (error) {
        console.error('❌ 初始化聊天失败:', error);
        showError('无法启动对话');
    }
}

async function loadChatMessages(sessionId) {
    try {
        const messages = await API.get(`/chat/${sessionId}/messages`);
        updateChatMessagesUI(messages);
    } catch (error) {
        console.error('❌ 加载消息失败:', error);
    }
}

function updateChatUI(session) {
    const titleElement = document.querySelector('[data-chat-title]');
    if (titleElement) {
        titleElement.textContent = session.title || '深度研究';
    }
}

function updateChatMessagesUI(messages) {
    const container = document.querySelector('[data-messages-container]');
    if (!container) return;

    container.innerHTML = messages.map(msg => `
        <div class="flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} mb-4">
            <div class="max-w-[80%] rounded-2xl px-4 py-3 ${
                msg.role === 'user'
                    ? 'bg-primary text-background-dark'
                    : 'bg-white/10 text-slate-100'
            }">
                <p class="text-sm leading-relaxed">${escapeHtml(msg.content)}</p>
            </div>
        </div>
    `).join('');

    // 滚动到底部
    container.scrollTop = container.scrollHeight;
}

// 发送消息
window.sendMessage = async function(sessionId) {
    const input = document.querySelector('[data-message-input]');
    if (!input || !input.value.trim()) return;

    const message = input.value.trim();
    input.value = '';

    try {
        // 显示用户消息
        const container = document.querySelector('[data-messages-container]');
        if (container) {
            const userMsg = document.createElement('div');
            userMsg.className = 'flex justify-end mb-4';
            userMsg.innerHTML = `
                <div class="max-w-[80%] rounded-2xl px-4 py-3 bg-primary text-background-dark">
                    <p class="text-sm leading-relaxed">${escapeHtml(message)}</p>
                </div>
            `;
            container.appendChild(userMsg);
            container.scrollTop = container.scrollHeight;
        }

        // 发送到API
        const response = await API.post(`/chat/${sessionId}/message`, {
            content: message
        });

        // 显示AI响应
        if (container && response) {
            const aiMsg = document.createElement('div');
            aiMsg.className = 'flex justify-start mb-4';
            aiMsg.innerHTML = `
                <div class="max-w-[80%] rounded-2xl px-4 py-3 bg-white/10 text-slate-100">
                    <p class="text-sm leading-relaxed">${escapeHtml(response.content)}</p>
                </div>
            `;
            container.appendChild(aiMsg);
            container.scrollTop = container.scrollHeight;
        }
    } catch (error) {
        console.error('❌ 发送消息失败:', error);
        showError('发送失败，请重试');
    }
};

// 页面加载完成后初始化应用
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// 导出全局函数
window.navigateTo = navigateTo;
window.API = API;
window.refreshPage = refreshPage;
