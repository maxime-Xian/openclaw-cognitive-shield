import grpc
from concurrent import futures
import time
import logging
import json
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

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
        self.sessions = {}
        self.intervention_patterns = self._load_intervention_patterns()
        self.max_interventions_per_session = 3
        self.session_timeout = timedelta(minutes=60)

    def _load_intervention_patterns(self) -> Dict:
        """Load intervention patterns from configuration"""
        # Default patterns if config file not found
        return {
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
                "triggers": ["好恨自己", "我太废了", "我怎么总是做来自好"],
                "level": "L2"
            }
        }

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

    def _detect_patterns(self, text: str) -> List[Dict]:
        """Detect cognitive risk patterns in user input"""
        detected_patterns = []

        for pattern_id, pattern_data in self.intervention_patterns.items():
            for trigger in pattern_data["triggers"]:
                if trigger.lower() in text.lower():
                    detected_patterns.append({
                        "pattern_id": pattern_id,
                        "pattern_name": pattern_data["name"],
                        "trigger": trigger,
                        "level": pattern_data["level"]
                    })

        return detected_patterns

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
        """Analyze user input for cognitive patterns"""
        try:
            session_id = request.session_id
            user_input = request.user_input
            user_context = request.user_context

            # Update session activity
            if session_id in self.sessions:
                self.sessions[session_id]["last_activity"] = datetime.utcnow()

            # Hash user ID for privacy
            user_id_hash = self._hash_user_id(user_context.user_id_hash or "anonymous")

            # Log data access
            self._log_data_access(
                "analyze_input",
                "user_text",
                user_id_hash,
                "processed"
            )

            # Detect patterns
            detected_patterns = self._detect_patterns(user_input.text)

            # Convert to protobuf format
            pb_patterns = []
            for pattern in detected_patterns:
                pb_pattern = pb2.RiskPattern(
                    pattern_id=pattern["pattern_id"],
                    pattern_name=pattern["pattern_name"],
                    description=f"Detected trigger: {pattern['trigger']}",
                    severity=self._get_intervention_level([pattern])
                )
                pb_patterns.append(pb_pattern)

            # Determine intervention level
            intervention_level = self._get_intervention_level(detected_patterns)

            # Create cognitive state
            cognitive_state = pb2.CognitiveState(
                cognitive_load=0.5 if detected_patterns else 0.2,
                stress_indicator=0.7 if detected_patterns else 0.3,
                focus_level=0.3 if detected_patterns else 0.8,
                active_biases=[pattern["pattern_name"] for pattern in detected_patterns]
            )

            return pb2.AnalyzeInputResponse(
                cognitive_state=cognitive_state,
                detected_patterns=pb_patterns,
                recommended_intervention=intervention_level,
                confidence_score=0.85 if detected_patterns else 0.95
            )

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_message(f"Analysis failed: {str(e)}")
            return None

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