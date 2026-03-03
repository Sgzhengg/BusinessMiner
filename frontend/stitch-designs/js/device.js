/**
 * RedditMiner - 设备ID管理
 */

/**
 * 生成UUID v4
 */
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * 获取或生成设备ID
 */
function getDeviceId() {
    let deviceId = localStorage.getItem('redditminer_device_id');

    if (!deviceId) {
        deviceId = generateUUID();
        localStorage.setItem('redditminer_device_id', deviceId);
        console.log('✓ 新设备ID已生成:', deviceId);
    } else {
        console.log('✓ 设备ID:', deviceId);
    }

    return deviceId;
}

/**
 * 获取设备信息
 */
function getDeviceInfo() {
    const ua = navigator.userAgent;
    const deviceInfo = {
        deviceId: getDeviceId(),
        userAgent: ua,
        platform: navigator.platform,
        language: navigator.language,
        screen: {
            width: screen.width,
            height: screen.height
        },
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight
        }
    };

    return deviceInfo;
}

/**
 * 初始化设备ID
 */
function initDeviceId() {
    const deviceId = getDeviceId();

    // 将设备ID添加到所有API请求的header中
    if (typeof window !== 'undefined' && !window.API_HEADERS) {
        window.API_HEADERS = {
            'X-Device-ID': deviceId,
            'Content-Type': 'application/json'
        };
    }

    return deviceId;
}

// 页面加载时自动初始化
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDeviceId);
    } else {
        initDeviceId();
    }
}

// 导出函数
if (typeof window !== 'undefined') {
    window.getDeviceId = getDeviceId;
    window.getDeviceInfo = getDeviceInfo;
    window.initDeviceId = initDeviceId;
}
