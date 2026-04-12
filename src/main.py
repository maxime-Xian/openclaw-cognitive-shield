import grpc
from concurrent import futures
import time
import logging
import json
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

import src.cognitive_shield_pb2 as pb2
import src.cognitive_shield_pb2_grpc as pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CognitiveShieldServicer(pb2_grpc.CognitiveShieldSkillServicer):
    def __init__(self):
        # 优先级：OpenClaw 持久化存储 > 本地文件缓存 > 进程内存
        self.sessions = {}
        self.knowledge_dir = Path("knowledge")
        self.memory_dir = Path("memory/evolution")
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 尝试初始化 OpenClaw Memory Client (占位，实际由平台注入或配置)
        self.memory_client = None 
        
        self.intervention_patterns = self._load_intervention_patterns()
        self.max_interventions_per_session = 3
        self.session_timeout = timedelta(minutes=60)

    def _get_pattern_count(self, user_id_hash: str, pattern_id: str) -> int:
        """从持久化内存读取模式触发计数"""
        key = f"shield:{user_id_hash}:{pattern_id}:count"
        
        # 1. 尝试使用 OpenClaw Memory API
        if self.memory_client:
            try:
                result = self.memory_client.get(key)
                return int(result) if result else 0
            except Exception as e:
                logger.error(f"OpenClaw Memory read failed: {e}")

        # 2. 尝试使用本地文件缓存 (OpenClaw Skill 工作目录持久化)
        cache_file = self.memory_dir / f"{user_id_hash}_counts.json"
        if cache_file.exists():
            try:
                counts = json.loads(cache_file.read_text())
                return counts.get(pattern_id, 0)
            except:
                pass
        
        return 0

    def _increment_pattern_count(self, user_id_hash: str, pattern_id: str) -> int:
        """增加模式触发计数并持久化"""
        new_count = self._get_pattern_count(user_id_hash, pattern_id) + 1
        key = f"shield:{user_id_hash}:{pattern_id}:count"
        
        # 1. 写入 OpenClaw Memory API
        if self.memory_client:
            try:
                self.memory_client.set(key, str(new_count), ttl=30*24*3600)
            except Exception as e:
                logger.error(f"OpenClaw Memory write failed: {e}")

        # 2. 写入本地文件缓存
        cache_file = self.memory_dir / f"{user_id_hash}_counts.json"
        counts = {}
        if cache_file.exists():
            try: counts = json.loads(cache_file.read_text())
            except: pass
        counts[pattern_id] = new_count
        cache_file.write_text(json.dumps(counts))
        
        return new_count

    def _load_intervention_patterns(self) -> Dict:
        """Load intervention patterns from knowledge files"""
        patterns = {}
        
        # 核心知识文件列表
        knowledge_files = [
            self.knowledge_dir / "cognitive_bias_evidence.md",
            self.knowledge_dir / "error_knowledge_v1.0.0.md"
        ]
        
        for f in knowledge_files:
            if f.exists():
                try:
                    parsed = self._parse_knowledge_file(f)
                    patterns.update(parsed)
                    logger.info(f"Loaded {len(parsed)} patterns from {f.name}")
                except Exception as e:
                    logger.error(f"Failed to parse {f.name}: {e}")
        
        # 硬编码兜底，确保核心模式永远存在且优先级最高
        fallback = {
            "OS-001": {
                "name": "意志力崇拜 (过度自耗)",
                "triggers": ["硬扛", "再撑一会", "不累", "今晚必须干完"],
                "level": "L3"
            },
            "OS-002": {
                "name": "偷懒与逃避行为",
                "triggers": ["先把这个没用的美化一下", "顺手全部重构", "明天再说"],
                "level": "L2"
            },
            "OS-003": {
                "name": "价值观偏离行为",
                "triggers": ["为了赚钱不择手段", "忘了初衷", "情绪化攻击"],
                "level": "L3"
            },
            "OS-004": {
                "name": "自我攻击倾向",
                "triggers": ["好恨自己", "我太废了", "我怎么总是这么差"],
                "level": "L2"
            }
        }
        
        # 合并模式，硬编码模式覆盖同名 ID
        patterns.update(fallback)
        return patterns

    def _parse_knowledge_file(self, filepath: Path) -> Dict:
        """
        从 Markdown 文件解析触发模式
        约定格式：
        ## 模式ID: OS-XXX
        名称: 模式名称
        触发词: 词1, 词2, 词3
        级别: L1/L2/L3
        """
        patterns = {}
        content = filepath.read_text(encoding='utf-8')
        
        # 使用正则匹配约定块
        blocks = re.findall(
            r'##\s*模式ID:\s*([\w-]+)\s*\n名称:\s*(.+)\s*\n触发词:\s*(.+)\s*\n级别:\s*(L[123])',
            content
        )
        
        for pid, name, triggers_str, level in blocks:
            patterns[pid] = {
                "name": name.strip(),
                "triggers": [t.strip() for t in triggers_str.split(',')],
                "level": level.strip()
            }
        return patterns

    def _hash_user_id(self, user_id: str) -> str:
        """Hash user ID for privacy"""
        return hashlib.sha256(user_id.encode()).hexdigest()

    def _log_data_access(self, event: str, data_category: str, user_id_hash: str, result: str):
        """Log all data access for audit purposes"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "skill_id": "skill-max-cognitive-shield",
            "event": event,
            "data_category": data_category,
            "hash_user_id": user_id_hash,
            "result": result
        }
        logger.info(f"DATA_ACCESS: {json.dumps(log_entry)}")

    def _detect_patterns(self, text: str) -> Dict:
        """识别输入中的风险模式 (升级：简单语义匹配)"""
        detected = {}
        # 简单分词 (仅用于演示，生产环境建议用 jieba/hanlp)
        tokens = list(set(re.findall(r'\w+', text.lower())))
        
        for pid, pdata in self.intervention_patterns.items():
            best_score = 0.0
            matched_trigger = ""
            
            for trigger in pdata['triggers']:
                trigger_tokens = list(set(re.findall(r'\w+', trigger.lower())))
                score = self._compute_similarity(tokens, trigger_tokens)
                
                # 字符串直接包含作为强匹配
                if trigger.lower() in text.lower():
                    score = 1.0
                
                if score > best_score:
                    best_score = score
                    matched_trigger = trigger
            
            # 相似度阈值 0.6 (对应文档 80%，但在词袋模型下调低)
            if best_score >= 0.6:
                detected[pid] = pdata.copy()
                detected[pid]['matched_trigger'] = matched_trigger
                detected[pid]['confidence'] = best_score
                
        return detected

    def _compute_similarity(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """TF-IDF Cosine Similarity (简化版)"""
        from collections import Counter
        import math
        
        q_tf = Counter(query_tokens)
        d_tf = Counter(doc_tokens)
        
        # 计算点积
        dot = sum(q_tf[t] * d_tf[t] for t in q_tf if t in d_tf)
        q_norm = math.sqrt(sum(v**2 for v in q_tf.values()))
        d_norm = math.sqrt(sum(v**2 for v in d_tf.values()))
        
        return dot / (q_norm * d_norm) if q_norm * d_norm > 0 else 0.0

    def _generate_intervention_prompt(self, pattern, count, user_id_hash) -> str:
        """生成给 LLM 的干预指令"""
        if not pattern:
            return ""
        
        level = pattern['level']
        name = pattern['name']
        
        if level == "L3" or count >= 3:
            return (f"### [CRITICAL] 触发 Mode D 协议\n"
                    f"检测到高危模式「{name}」，这是30天内第 {count} 次触发。\n"
                    f"请立即中断当前任务流程，引用历史记录进行元认知质询。")
        elif level == "L2":
            return (f"### [WARNING] 触发 L2 积极干预\n"
                    f"识别到风险模式「{name}」(频次: {count})。\n"
                    f"请在回答用户前，先展示历史证据链并要求用户确认当前认知状态。")
        else:
            return f"### [INFO] L1 温和提醒\n检测到「{name}」信号。请在回复末尾附加一句关于能量管理的温和提示。"

    def _get_intervention_level(self, patterns: List[Dict]) -> pb2.InterventionLevel:
        """Determine intervention level based on detected patterns"""
        if not patterns:
            return pb2.InterventionLevel.NONE

        # Check for L3 patterns first
        for pattern in patterns:
            if pattern["level"] == "L3":
                return pb2.InterventionLevel.LEVEL_3_CRITICAL

        # Check for L2 patterns
        for pattern in patterns:
            if pattern["level"] == "L2":
                return pb2.InterventionLevel.LEVEL_2_INTERVENTION

        # Default to L1 for any detected pattern
        return pb2.InterventionLevel.LEVEL_1_MONITOR

    def Initialize(self, request, context):
        """Initialize skill session"""
        try:
            session_id = f"session_{int(time.time())}_{hash(request.skill_id) % 10000}"

            self.sessions[session_id] = {
                "created_at": datetime.utcnow(),
                "config": dict(request.config),
                "intervention_count": 0,
                "last_activity": datetime.utcnow()
            }

            logger.info(f"Initialized session: {session_id}")

            return pb2.InitializeResponse(
                success=True,
                message="Cognitive Shield skill initialized successfully",
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return pb2.InitializeResponse(
                success=False,
                message=f"Initialization failed: {str(e)}",
                session_id=""
            )

    def AnalyzeInput(self, request, context):
        """Analyze user input for cognitive risks"""
        user_id_hash = request.user_context.user_id_hash
        text = request.user_input.text
        intent_type = request.user_input.intent_type
        
        # 1. 检测风险模式 (升级为语义匹配)
        detected_patterns = self._detect_patterns(text)
        
        # 2. 统计频次与确定干预等级
        intervention_level = pb2.InterventionLevel.LEVEL_NONE
        max_count = 0
        top_pattern = None
        
        pb_patterns = []
        for pid, pdata in detected_patterns.items():
            count = self._increment_pattern_count(user_id_hash, pid)
            if count > max_count:
                max_count = count
                top_pattern = pdata
                top_pattern['id'] = pid
            
            # 确定干预等级
            level_map = {"L1": pb2.InterventionLevel.L1, "L2": pb2.InterventionLevel.L2, "L3": pb2.InterventionLevel.L3}
            current_level = level_map.get(pdata['level'], pb2.InterventionLevel.LEVEL_NONE)
            if current_level > intervention_level:
                intervention_level = current_level
            
            pb_patterns.append(pb2.RiskPattern(
                pattern_id=pid,
                pattern_name=pdata['name'],
                level=current_level,
                description=f"触发词语义匹配: {pdata['matched_trigger']}"
            ))

        # 3. 生成干预文案草稿与证据摘要
        intervention_prompt = self._generate_intervention_prompt(top_pattern, max_count, user_id_hash)
        evidence_summary = f"用户输入: '{text}' | 匹配模式: {top_pattern['name'] if top_pattern else 'None'} | 30天内频次: {max_count}" if top_pattern else ""

        return pb2.AnalyzeInputResponse(
            cognitive_state=pb2.CognitiveState.NORMAL, # 示例
            detected_patterns=pb_patterns,
            intervention_level=intervention_level,
            pattern_occurrence_count=max_count,
            intervention_prompt=intervention_prompt,
            evidence_summary=evidence_summary
        )

    def ScanPatterns(self, request, context):
        """心跳扫描巡检 (HEARTBEAT 任务 3)"""
        all_text = " ".join(request.recent_messages)
        detected = self._detect_patterns(all_text)
        
        pb_patterns = []
        for pid, pdata in detected.items():
            pb_patterns.append(pb2.RiskPattern(
                pattern_id=pid,
                pattern_name=pdata['name'],
                level=pb2.InterventionLevel.L2 # 默认为 L2
            ))
            
        return pb2.ScanPatternsResponse(
            detected_patterns=pb_patterns,
            intervention_needed=len(detected) >= 3,
            recommended_action="建议执行 Mode D 协议" if len(detected) >= 3 else "继续观察",
            evidence_summary=f"在最近 {request.scan_window_minutes} 分钟内识别到 {len(detected)} 个风险特征。"
        )

    def RequestIntervention(self, request, context):
        """Apply cognitive intervention"""
        try:
            session_id = request.session_id
            level = request.level
            reason = request.reason

            if session_id not in self.sessions:
                return pb2.InterventionResponse(
                    intervention_applied=False,
                    intervention_message="Invalid session",
                    suggested_actions=[]
                )

            session = self.sessions[session_id]

            # Check intervention limit
            if session["intervention_count"] >= self.max_interventions_per_session:
                return pb2.InterventionResponse(
                    intervention_applied=False,
                    intervention_message="Maximum interventions reached for this session",
                    suggested_actions=["Consider taking a break", "Session may need to end"]
                )

            # Apply intervention based on level
            intervention_messages = {
                pb2.InterventionLevel.LEVEL_1_MONITOR: [
                    "I notice you might be falling into a familiar pattern. Would you like to pause and reflect?"
                ],
                pb2.InterventionLevel.LEVEL_2_INTERVENTION: [
                    "Let's take a moment to step back from this. What's the most important thing right now?",
                    "I'm detecting some concerning patterns. Can we reassess your approach?"
                ],
                pb2.InterventionLevel.LEVEL_3_CRITICAL: [
                    "I need to intervene here. This approach may be harmful to your wellbeing.",
                    "Let's stop and consider a different path. Your health is more important than this task."
                ]
            }

            suggested_actions = {
                pb2.InterventionLevel.LEVEL_1_MONITOR: [
                    "Take 5 deep breaths",
                    "Review your goals for this session"
                ],
                pb2.InterventionLevel.LEVEL_2_INTERVENTION: [
                    "Take a 10-minute break",
                    "Step away from the screen",
                    "Drink some water"
                ],
                pb2.InterventionLevel.LEVEL_3_CRITICAL: [
                    "Stop working immediately",
                    "Take a 30-minute rest",
                    "Consider ending the session",
                    "Contact support if needed"
                ]
            }

            message_list = intervention_messages.get(level, ["Please take a moment to reflect."])
            action_list = suggested_actions.get(level, ["Take a break"])

            # Update session
            session["intervention_count"] += 1
            session["last_activity"] = datetime.utcnow()

            logger.info(f"Applied {level} intervention to session {session_id}")

            return pb2.InterventionResponse(
                intervention_applied=True,
                intervention_message=message_list[0],
                suggested_actions=action_list
            )

        except Exception as e:
            logger.error(f"Intervention failed: {e}")
            return pb2.InterventionResponse(
                intervention_applied=False,
                intervention_message="Intervention failed",
                suggested_actions=[]
            )

    def GetStatus(self, request, context):
        """Get skill status and metrics"""
        try:
            active_sessions = len([
                sid for sid, session in self.sessions.items()
                if datetime.utcnow() - session["last_activity"] < self.session_timeout
            ])

            # Calculate basic metrics
            total_requests = sum(session.get("intervention_count", 0) for session in self.sessions.values())

            metrics = pb2.SystemMetrics(
                cpu_usage=0.3,  # Placeholder - would use actual system metrics
                memory_usage=0.4,  # Placeholder
                total_requests=total_requests,
                average_response_time=0.05  # 50ms average
            )

            return pb2.StatusResponse(
                skill_status="healthy",
                active_sessions=active_sessions,
                metrics=metrics
            )

        except Exception as e:
            logger.error(f"Status check failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_message(f"Status check failed: {str(e)}")
            return None

    def Pause(self, request, context):
        """Pause skill session"""
        try:
            session_id = request.session_id
            if session_id in self.sessions:
                session = self.sessions[session_id]
                saved_state = json.dumps({
                    "intervention_count": session["intervention_count"],
                    "config": session["config"]
                })
                return pb2.PauseResponse(success=True, saved_state=saved_state)
            else:
                return pb2.PauseResponse(success=False, saved_state="")
        except Exception as e:
            logger.error(f"Pause failed: {e}")
            return pb2.PauseResponse(success=False, saved_state="")

    def Resume(self, request, context):
        """Resume skill session"""
        try:
            session_id = request.session_id
            saved_state = request.saved_state

            if session_id in self.sessions and saved_state:
                try:
                    state_data = json.loads(saved_state)
                    self.sessions[session_id].update(state_data)
                    self.sessions[session_id]["last_activity"] = datetime.utcnow()
                    return pb2.ResumeResponse(success=True, message="Session resumed")
                except json.JSONDecodeError:
                    return pb2.ResumeResponse(success=False, message="Invalid saved state")
            else:
                return pb2.ResumeResponse(success=False, message="Session not found")
        except Exception as e:
            logger.error(f"Resume failed: {e}")
            return pb2.ResumeResponse(success=False, message=str(e))

    def Destroy(self, request, context):
        """Destroy skill session"""
        try:
            session_id = request.session_id
            if session_id in self.sessions:
                del self.sessions[session_id]
                logger.info(f"Destroyed session: {session_id}")
                return pb2.DestroyResponse(success=True, message="Session destroyed")
            else:
                return pb2.DestroyResponse(success=False, message="Session not found")
        except Exception as e:
            logger.error(f"Destroy failed: {e}")
            return pb2.DestroyResponse(success=False, message=str(e))

    def Run(self, request, context):
        """Main execution loop - streaming response"""
        try:
            session_id = request.session_id
            user_input = request.user_input

            if session_id not in self.sessions:
                yield pb2.RunResponse(
                    response_id=f"error_{int(time.time())}",
                    content="Invalid session",
                    intervention_level=pb2.InterventionLevel.NONE,
                    requires_action=False
                )
                return

            # Analyze input
            analyze_request = pb2.AnalyzeInputRequest(
                session_id=session_id,
                user_input=user_input,
                user_context=pb2.UserContext(user_id_hash="anonymous")
            )

            # For this example, we'll create a simple analysis
            detected_patterns = self._detect_patterns(user_input.text)
            intervention_level = self._get_intervention_level(detected_patterns)

            # Generate response
            response_id = f"resp_{int(time.time())}_{hash(user_input.text) % 10000}"

            if detected_patterns:
                content = f"I notice you might be using language that could indicate cognitive stress. Would you like to explore this further?"
                requires_action = True
            else:
                content = f"I've processed your input. How can I support your cognitive wellbeing today?"
                requires_action = False

            # Update session activity
            self.sessions[session_id]["last_activity"] = datetime.utcnow()

            yield pb2.RunResponse(
                response_id=response_id,
                content=content,
                intervention_level=intervention_level,
                requires_action=requires_action
            )

        except Exception as e:
            logger.error(f"Run failed: {e}")
            yield pb2.RunResponse(
                response_id=f"error_{int(time.time())}",
                content="An error occurred during processing",
                intervention_level=pb2.InterventionLevel.NONE,
                requires_action=False
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CognitiveShieldSkillServicer_to_server(
        CognitiveShieldServicer(), server
    )
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)

    logger.info(f"Starting gRPC server on {listen_addr}")
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
        server.stop(0)

if __name__ == '__main__':
    serve()