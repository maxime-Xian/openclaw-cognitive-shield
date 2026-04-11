# REST API Server for Cognitive Shield Skill
from flask import Flask, request, jsonify
import grpc
import logging
import json
from datetime import datetime
from concurrent import futures
import threading
import time

from src.main import CognitiveShieldServicer
import src.cognitive_shield_pb2 as pb2
import src.cognitive_shield_pb2_grpc as pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global gRPC servicer instance
grpc_servicer = None

def start_grpc_server():
    """Start gRPC server in background thread"""
    global grpc_servicer
    grpc_servicer = CognitiveShieldServicer()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CognitiveShieldSkillServicer_to_server(grpc_servicer, server)

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)

    logger.info(f"Starting gRPC server on {listen_addr}")
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "skill-max-cognitive-shield"
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get skill status"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        # Create gRPC request
        request = pb2.StatusRequest(session_id="status_check")

        # Call gRPC method
        response = grpc_servicer.GetStatus(request, None)

        if response is None:
            return jsonify({"error": "Failed to get status"}), 500

        return jsonify({
            "skill_status": response.skill_status,
            "active_sessions": response.active_sessions,
            "metrics": {
                "cpu_usage": response.metrics.cpu_usage,
                "memory_usage": response.metrics.memory_usage,
                "total_requests": response.metrics.total_requests,
                "average_response_time": response.metrics.average_response_time
            }
        })

    except Exception as e:
        logger.error(f"Status endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_input():
    """Analyze user input for cognitive patterns"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Missing text parameter"}), 400

        session_id = data.get('session_id', f"anon_{int(time.time())}")
        user_text = data['text']

        # Create gRPC request
        user_input = pb2.UserInput(
            text=user_text,
            timestamp=datetime.utcnow().isoformat(),
            type=pb2.InputType.TEXT
        )

        user_context = pb2.UserContext(
            user_id_hash=data.get('user_id', 'anonymous'),
            session_duration_minutes=data.get('session_duration', 0)
        )

        analyze_request = pb2.AnalyzeInputRequest(
            session_id=session_id,
            user_input=user_input,
            user_context=user_context
        )

        # Call gRPC method
        response = grpc_servicer.AnalyzeInput(analyze_request, None)

        if response is None:
            return jsonify({"error": "Analysis failed"}), 500

        # Convert response to JSON
        detected_patterns = []
        for pattern in response.detected_patterns:
            detected_patterns.append({
                "pattern_id": pattern.pattern_id,
                "pattern_name": pattern.pattern_name,
                "description": pattern.description,
                "severity": pattern.severity
            })

        return jsonify({
            "cognitive_state": {
                "cognitive_load": response.cognitive_state.cognitive_load,
                "stress_indicator": response.cognitive_state.stress_indicator,
                "focus_level": response.cognitive_state.focus_level,
                "active_biases": list(response.cognitive_state.active_biases)
            },
            "detected_patterns": detected_patterns,
            "recommended_intervention": response.recommended_intervention,
            "confidence_score": response.confidence_score
        })

    except Exception as e:
        logger.error(f"Analyze endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/intervention', methods=['POST'])
def request_intervention():
    """Request cognitive intervention"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing request data"}), 400

        session_id = data.get('session_id', f"anon_{int(time.time())}")
        level = data.get('level', 1)  # Default to LEVEL_1_MONITOR
        reason = data.get('reason', 'Manual intervention request')

        # Create gRPC request
        intervention_request = pb2.InterventionRequest(
            session_id=session_id,
            level=level,
            reason=reason
        )

        # Call gRPC method
        response = grpc_servicer.RequestIntervention(intervention_request, None)

        return jsonify({
            "intervention_applied": response.intervention_applied,
            "intervention_message": response.intervention_message,
            "suggested_actions": list(response.suggested_actions)
        })

    except Exception as e:
        logger.error(f"Intervention endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/initialize', methods=['POST'])
def initialize_session():
    """Initialize new skill session"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json() or {}

        # Create gRPC request
        initialize_request = pb2.InitializeRequest(
            skill_id=data.get('skill_id', 'skill-max-cognitive-shield'),
            config=data.get('config', {})
        )

        # Call gRPC method
        response = grpc_servicer.Initialize(initialize_request, None)

        return jsonify({
            "success": response.success,
            "message": response.message,
            "session_id": response.session_id
        })

    except Exception as e:
        logger.error(f"Initialize endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/session/<session_id>/pause', methods=['POST'])
def pause_session(session_id):
    """Pause skill session"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        pause_request = pb2.PauseRequest(session_id=session_id)
        response = grpc_servicer.Pause(pause_request, None)

        return jsonify({
            "success": response.success,
            "saved_state": response.saved_state
        })

    except Exception as e:
        logger.error(f"Pause endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/session/<session_id>/resume', methods=['POST'])
def resume_session(session_id):
    """Resume skill session"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json() or {}
        saved_state = data.get('saved_state', '')

        resume_request = pb2.ResumeRequest(
            session_id=session_id,
            saved_state=saved_state
        )
        response = grpc_servicer.Resume(resume_request, None)

        return jsonify({
            "success": response.success,
            "message": response.message
        })

    except Exception as e:
        logger.error(f"Resume endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/session/<session_id>/destroy', methods=['POST'])
def destroy_session(session_id):
    """Destroy skill session"""
    try:
        if grpc_servicer is None:
            return jsonify({"error": "Service not initialized"}), 503

        destroy_request = pb2.DestroyRequest(session_id=session_id)
        response = grpc_servicer.Destroy(destroy_request, None)

        return jsonify({
            "success": response.success,
            "message": response.message
        })

    except Exception as e:
        logger.error(f"Destroy endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start gRPC server in background thread
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()

    # Wait for gRPC server to initialize
    time.sleep(2)

    # Start REST API server
    logger.info("Starting REST API server on port 8080")
    app.run(host='0.0.0.0', port=8080, debug=False)