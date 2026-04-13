# 🛠️ Prefrontal Shield 故障排查指南

## 📋 常见问题与解决方案

---

## 🔧 安装问题

### 问题 1: 依赖安装失败

**症状**: 运行 `pip install` 或 `npm install` 时报错

**可能原因**:
- Node.js/Python 版本不兼容
- 网络问题导致包下载失败
- 系统缺少编译工具

**解决方案**:

```bash
# 1. 检查 Node.js 版本 (需要 >= 14.0.0)
node --version

# 2. 检查 Python 版本 (需要 >= 3.8)
python3 --version

# 3. 使用国内镜像源
npm install --registry=https://registry.npmmirror.com
pip install --index-url=https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 如果是系统依赖问题 (Linux)
sudo apt-get install build-essential python3-dev

# 5. 如果是权限问题
sudo npm install -g <package>
```

---

### 问题 2: 配置文件加载失败

**症状**: 启动时报错 "Failed to load manifest.yaml"

**解决方案**:

```bash
# 1. 检查文件是否存在
ls -la skills/guardian-safety-engine/manifest.yaml

# 2. 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('manifest.yaml'))"

# 3. 检查文件权限
chmod 644 skills/guardian-safety-engine/manifest.yaml

# 4. 使用绝对路径
export GUARDIAN_CONFIG_PATH=/full/path/to/manifest.yaml
```

---

## 🚀 运行时问题

### 问题 3: 服务启动失败

**症状**: 运行 `npm start` 或 `python main.py` 时崩溃

**诊断步骤**:

```bash
# 1. 检查端口是否被占用
lsof -i :8080  # Guardian Safety Engine
lsof -i :8081  # Sleep Guardian

# 2. 查看详细错误日志
npm start 2>&1 | tee debug.log
python main.py 2>&1 | tee debug.log

# 3. 检查环境变量
echo $GUARDIAN_LOG_LEVEL
echo $GUARDIAN_DEBUG_MODE

# 4. 验证配置文件
node -e "console.log(require('./manifest.yaml'))"
```

**常见错误及解决方案**:

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `Port already in use` | 端口被占用 | 更换端口或杀死占用进程 |
| `Config validation failed` | manifest.yaml 格式错误 | 检查 YAML 语法 |
| `Module not found` | 依赖未安装 | 重新运行 npm install |
| `Permission denied` | 文件权限不足 | 修改文件权限 |

---

### 问题 4: API 请求无响应

**症状**: 发送请求后长时间无响应或超时

**诊断步骤**:

```bash
# 1. 检查服务是否运行
curl http://localhost:8080/health

# 2. 检查服务日志
tail -f logs/guardian-safety-engine.log

# 3. 测试本地连接
curl -v http://127.0.0.1:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input":"test","context":{"time":"14:00"}}'

# 4. 检查超时配置
# 在 manifest.yaml 中增加超时时间
resources:
  timeout: 60  # 增加到60秒
```

---

## 📊 性能问题

### 问题 5: 响应时间过长

**症状**: API 响应时间超过 100ms (P95)

**诊断与优化**:

```bash
# 1. 启用性能日志
export GUARDIAN_DEBUG_MODE=true

# 2. 运行性能测试
npm run benchmark

# 3. 检查资源使用
top -p $(pgrep -f guardian-safety-engine)

# 4. 优化配置
# 在 manifest.yaml 中启用缓存
config:
  monitoring:
    enable_cache: true
    cache_ttl: 300
```

**性能基准**:

| 指标 | 目标值 | 当前平均值 | 优化建议 |
|------|--------|-----------|---------|
| 响应时间 (P95) | < 100ms | 实测值 | 启用缓存 |
| 内存使用 | < 100MB | 实测值 | 减少历史记录 |
| CPU 使用 | < 20% | 实测值 | 降低检查频率 |
| 并发能力 | > 100 req/s | 实测值 | 增加工作线程 |

---

### 问题 6: 内存占用过高

**症状**: 服务内存持续增长，最终 OOM

**解决方案**:

```bash
# 1. 检查内存使用
ps aux | grep guardian

# 2. 限制内存使用
# 在 manifest.yaml 中设置
resources:
  memory_limit: "100MB"

# 3. 启用内存监控
export ENABLE_MEMORY_MONITORING=true

# 4. 定期清理缓存
npm run cleanup-cache
```

---

## 🛡️ 功能问题

### 问题 7: 干预级别判断不准确

**症状**: 高风险输入没有被正确识别

**诊断步骤**:

```bash
# 1. 启用调试模式
export GUARDIAN_DEBUG_MODE=true

# 2. 测试特定输入
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I must finish this now no matter what!",
    "context": {
      "time": "03:00",
      "sleep_hours": 2,
      "stress_level": 10
    }
  }'

# 3. 检查返回的 evidence
# 查看 debug_info 中的特征提取结果
```

**调整阈值**:

```yaml
# 在 manifest.yaml 中调整
config:
  intervention_levels:
    l1_threshold: 0.3   # 提高敏感度
    l2_threshold: 0.6
    l3_threshold: 0.85
```

---

### 问题 8: 睡眠检测不准确

**症状**: Sleep Guardian 的能量状态与实际不符

**诊断步骤**:

```javascript
// 1. 检查系统监控数据
curl http://localhost:8081/system-status

// 2. 查看详细检测日志
tail -f logs/sleep-guardian.log | grep DETECTION

// 3. 手动提供睡眠数据
const guardian = new SleepGuardian();
guardian.setExplicitSleepData({
  last_sleep: '2026-04-11T23:00:00Z',
  wake_time: '2026-04-12T06:30:00Z'
});
```

**常见场景处理**:

| 场景 | 问题 | 解决方案 |
|------|------|---------|
| 夜班工作 | 白天睡觉 | 设置工作时段配置 |
| 不规律作息 | 检测不准 | 提供显式睡眠数据 |
| 频繁小睡 | 误判为睡眠 | 设置最小睡眠时长阈值 |

---

## 🔒 安全问题

### 问题 9: 权限验证失败

**症状**: API 返回 403 Forbidden

**解决方案**:

```bash
# 1. 检查权限配置
# 在 manifest.yaml 中
permissions:
  - name: "read_memory"
    description: "Read access to user's memory"
    required: true

# 2. 提供认证 token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8080/analyze

# 3. 禁用安全检查 (仅测试环境)
export GUARDIAN_DISABLE_AUTH=true
```

---

## 📝 日志分析

### 日志级别说明

```yaml
DEBUG: 详细的调试信息，包括特征提取、中间计算结果
INFO: 正常的运行信息，包括请求处理、状态变更
WARN: 警告信息，包括边界情况、性能下降
ERROR: 错误信息，包括异常、失败的操作
```

### 日志格式

```json
{
  "timestamp": "2026-04-12T14:30:00.000Z",
  "level": "INFO",
  "service": "guardian-safety-engine",
  "message": "Risk analysis completed",
  "metadata": {
    "request_id": "uuid",
    "processing_time_ms": 45,
    "risk_score": 0.78,
    "intervention_level": "L2"
  }
}
```

### 常用日志查询

```bash
# 查看最近 100 行错误日志
grep "ERROR" logs/guardian-safety-engine.log | tail -100

# 查看特定请求的日志
grep "request_id=abc123" logs/guardian-safety-engine.log

# 查看性能相关日志
grep "processing_time" logs/guardian-safety-engine.log | awk '{print $8}' | sort -n

# 统计各干预级别次数
grep "intervention_level" logs/guardian-safety-engine.log | \
  awk -F'"' '{print $4}' | sort | uniq -c
```

---

## 🆘 获取帮助

### 自助排查

1. **查看完整日志**: `tail -500 logs/*.log`
2. **运行诊断脚本**: `npm run diagnostics`
3. **检查系统状态**: `npm run status`
4. **验证配置**: `npm run validate-config`

### 联系支持

如果以上方法都无法解决问题，请提供以下信息：

```
1. 错误日志 (logs/ 目录下的完整日志文件)
2. 配置文件 (manifest.yaml)
3. 系统信息 (node --version, python --version)
4. 复现步骤 (如何触发这个问题的)
5. 环境变量设置
```

**联系方式**:
- 📧 邮箱: support@openclaw-shield.com
- 🐛 GitHub Issues: https://github.com/maxime-Xian/openclaw-cognitive-shield/issues
- 💬 Discord: https://discord.gg/prefrontal-shield

---

**最后更新**: 2026-04-12
**版本**: 1.0.0
