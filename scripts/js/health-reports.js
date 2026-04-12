/**
 * health-reports.js
 * 核心逻辑：报告生成
 * 功能：生成简单易懂的健康状态摘要
 */

function generateHealthReport(sleepData, energyLevel) {
    return {
        timestamp: new Date().toISOString(),
        sleep_duration: `${sleepData.toFixed(1)}h`,
        energy_level: energyLevel,
        advice: energyLevel === "LOW" ? "🌙 强制休息模式已启动，请立即关机。" : "✅ 系统状态良好，支持深度认知任务。"
    };
}

const sleepData = 4.5; // 示例
const energyLevel = "LOW"; // 示例
console.log(JSON.stringify(generateHealthReport(sleepData, energyLevel), null, 2));
