/**
 * sleep-guardian.js
 * 核心逻辑：基于开机/关机时间计算睡眠时长并更新能量状态
 * 运行方式：由系统 Cron 触发 (如 23:45)
 */

const fs = require('fs');
const path = require('path');

// 定义状态存储路径
const STATUS_PATH = path.join(__dirname, '../memory/.status/energy_status.json');

// 模拟读取系统开关机时间
function getSystemPowerLogs() {
    return {
        last_shutdown: new Date(Date.now() - 8 * 3600 * 1000), // 模拟 8 小时前关机
        last_startup: new Date()
    };
}

function updateEnergyState() {
    const logs = getSystemPowerLogs();
    const sleepDuration = (logs.last_startup - logs.last_shutdown) / (1000 * 3600);
    
    let energyLevel = "NORMAL";
    if (sleepDuration < 5) energyLevel = "LOW";
    else if (sleepDuration < 7) energyLevel = "SUBOPTIMAL";

    const status = {
        timestamp: new Date().toISOString(),
        sleep_duration: sleepDuration.toFixed(1),
        energy_level: energyLevel,
        advice: energyLevel === "LOW" ? "🌙 强制休息模式建议启动。" : "✅ 状态良好。"
    };

    // 确保目录存在
    const dir = path.dirname(STATUS_PATH);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(STATUS_PATH, JSON.stringify(status, null, 2));
    console.log(`[SleepGuardian] Current Energy Level: ${energyLevel} (${sleepDuration.toFixed(1)}h). Status saved to ${STATUS_PATH}`);
}

updateEnergyState();
