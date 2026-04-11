#!/bin/bash

# Integration Test Suite for Max Cognitive Shield
# Run comprehensive tests to validate skill functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_HOST="localhost"
TEST_PORT="8080"
TEST_BASE_URL="http://${TEST_HOST}:${TEST_PORT}"
CONTAINER_NAME="cognitive-shield-test"
IMAGE_NAME="skill-max-cognitive-shield:test"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Function to print test results
print_result() {
    local status=$1
    local test_name=$2
    local message=$3

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}[PASS]${NC} $test_name: $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}[FAIL]${NC} $test_name: $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
}

# Function to make HTTP requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4

    local curl_cmd="curl -s -w '%{http_code}'"

    if [ "$method" = "POST" ]; then
        curl_cmd="$curl_cmd -X POST -H 'Content-Type: application/json'"
        if [ -n "$data" ]; then
            curl_cmd="$curl_cmd -d '$data'"
        fi
    fi

    curl_cmd="$curl_cmd ${TEST_BASE_URL}${endpoint}"

    # Execute request and capture response and status code
    local result=$(eval $curl_cmd)
    local status_code=${result: -3}
    local response=${result%???}

    echo "$status_code|$response"
}

# Function to check if service is ready
wait_for_service() {
    local max_attempts=30
    local attempt=1

    echo -e "${BLUE}[INFO]${NC} Waiting for service to be ready..."

    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "${TEST_BASE_URL}/health" > /dev/null 2>&1; then
            echo -e "${GREEN}[SUCCESS]${NC} Service is ready!"
            return 0
        fi

        echo -e "${YELLOW}[WAIT]${NC} Attempt $attempt/$max_attempts"
        sleep 2
        attempt=$((attempt + 1))
    done

    echo -e "${RED}[ERROR]${NC} Service failed to start within timeout"
    return 1
}

# Function to build test image
build_test_image() {
    echo -e "${BLUE}[INFO]${NC} Building test Docker image..."

    if docker build -f Dockerfile.multi -t $IMAGE_NAME . > /dev/null 2>&1; then
        echo -e "${GREEN}[SUCCESS]${NC} Test image built successfully"
        return 0
    else
        echo -e "${RED}[ERROR]${NC} Failed to build test image"
        return 1
    fi
}

# Function to start test container
start_test_container() {
    echo -e "${BLUE}[INFO]${NC} Starting test container..."

    docker run -d \
        --name $CONTAINER_NAME \
        -p ${TEST_PORT}:8080 \
        -e LOG_LEVEL=DEBUG \
        -e MAX_INTERVENTIONS_PER_SESSION=5 \
        $IMAGE_NAME > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS]${NC} Test container started"
        return 0
    else
        echo -e "${RED}[ERROR]${NC} Failed to start test container"
        return 1
    fi
}

# Function to stop test container
stop_test_container() {
    echo -e "${BLUE}[INFO]${NC} Stopping test container..."

    docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
    docker rm $CONTAINER_NAME > /dev/null 2>&1 || true

    echo -e "${GREEN}[SUCCESS]${NC} Test container stopped"
}

# Test functions

test_health_endpoint() {
    echo -e "\n${BLUE}[TEST]${NC} Testing health endpoint..."

    local result=$(make_request "GET" "/health" "" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"status":"healthy"'; then
            print_result "PASS" "Health Endpoint" "Returns healthy status"
        else
            print_result "FAIL" "Health Endpoint" "Invalid response format"
        fi
    else
        print_result "FAIL" "Health Endpoint" "Expected 200, got $status_code"
    fi
}

test_status_endpoint() {
    echo -e "\n${BLUE}[TEST]${NC} Testing status endpoint..."

    local result=$(make_request "GET" "/status" "" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"skill_status"'; then
            print_result "PASS" "Status Endpoint" "Returns valid status information"
        else
            print_result "FAIL" "Status Endpoint" "Invalid response format"
        fi
    else
        print_result "FAIL" "Status Endpoint" "Expected 200, got $status_code"
    fi
}

test_initialize_session() {
    echo -e "\n${BLUE}[TEST]${NC} Testing session initialization..."

    local test_data='{"skill_id":"test-skill","config":{"test_mode":true}}'
    local result=$(make_request "POST" "/initialize" "$test_data" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"success":true'; then
            SESSION_ID=$(echo $response | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
            print_result "PASS" "Initialize Session" "Session created with ID: $SESSION_ID"
        else
            print_result "FAIL" "Initialize Session" "Session creation failed"
        fi
    else
        print_result "FAIL" "Initialize Session" "Expected 200, got $status_code"
    fi
}

test_analyze_normal_input() {
    echo -e "\n${BLUE}[TEST]${NC} Testing normal input analysis..."

    local test_data="{\"text\":\"I'm working on a project and feeling focused\",\"session_id\":\"$SESSION_ID\",\"user_id\":\"test-user\",\"session_duration\":10}"
    local result=$(make_request "POST" "/analyze" "$test_data" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"cognitive_state"'; then
            print_result "PASS" "Analyze Normal Input" "Analysis completed successfully"
        else
            print_result "FAIL" "Analyze Normal Input" "Invalid analysis response"
        fi
    else
        print_result "FAIL" "Analyze Normal Input" "Expected 200, got $status_code"
    fi
}

test_analyze_stressful_input() {
    echo -e "\n${BLUE}[TEST]${NC} Testing stressful input analysis..."

    local test_data="{\"text\":\"I have to finish this tonight no matter what, I'll just push through the pain\",\"session_id\":\"$SESSION_ID\",\"user_id\":\"test-user\",\"session_duration\":120}"
    local result=$(make_request "POST" "/analyze" "$test_data" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"detected_patterns"' && echo $response | grep -q '"recommended_intervention"'; then
            local intervention_level=$(echo $response | grep -o '"recommended_intervention":[0-9]' | cut -d':' -f2)
            if [ "$intervention_level" -gt 0 ]; then
                print_result "PASS" "Analyze Stressful Input" "Detected patterns and recommended intervention level $intervention_level"
            else
                print_result "FAIL" "Analyze Stressful Input" "Failed to detect concerning patterns"
            fi
        else
            print_result "FAIL" "Analyze Stressful Input" "Invalid analysis response"
        fi
    else
        print_result "FAIL" "Analyze Stressful Input" "Expected 200, got $status_code"
    fi
}

test_intervention_request() {
    echo -e "\n${BLUE}[TEST]${NC} Testing intervention request..."

    local test_data="{\"session_id\":\"$SESSION_ID\",\"level\":2,\"reason\":\"Test intervention\"}"
    local result=$(make_request "POST" "/intervention" "$test_data" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"intervention_applied"'; then
            print_result "PASS" "Intervention Request" "Intervention applied successfully"
        else
            print_result "FAIL" "Intervention Request" "Invalid intervention response"
        fi
    else
        print_result "FAIL" "Intervention Request" "Expected 200, got $status_code"
    fi
}

test_session_management() {
    echo -e "\n${BLUE}[TEST]${NC} Testing session management..."

    # Test pause
    local pause_result=$(make_request "POST" "/session/$SESSION_ID/pause" "" "200")
    local pause_status=$(echo $pause_result | cut -d'|' -f1)

    if [ "$pause_status" = "200" ]; then
        print_result "PASS" "Session Pause" "Session paused successfully"

        # Test resume
        local resume_data='{"saved_state":"test-state"}'
        local resume_result=$(make_request "POST" "/session/$SESSION_ID/resume" "$resume_data" "200")
        local resume_status=$(echo $resume_result | cut -d'|' -f1)

        if [ "$resume_status" = "200" ]; then
            print_result "PASS" "Session Resume" "Session resumed successfully"
        else
            print_result "FAIL" "Session Resume" "Failed to resume session"
        fi
    else
        print_result "FAIL" "Session Pause" "Failed to pause session"
    fi
}

test_error_handling() {
    echo -e "\n${BLUE}[TEST]${NC} Testing error handling..."

    # Test invalid session ID
    local test_data="{\"session_id\":\"invalid-session\",\"level\":1,\"reason\":\"Test\"}"
    local result=$(make_request "POST" "/intervention" "$test_data" "200")
    local status_code=$(echo $result | cut -d'|' -f1)
    local response=$(echo $result | cut -d'|' -f2)

    if [ "$status_code" = "200" ]; then
        if echo $response | grep -q '"intervention_applied":false'; then
            print_result "PASS" "Error Handling" "Properly handled invalid session"
        else
            print_result "FAIL" "Error Handling" "Did not handle invalid session correctly"
        fi
    else
        print_result "FAIL" "Error Handling" "Unexpected status code: $status_code"
    fi
}

test_performance() {
    echo -e "\n${BLUE}[TEST]${NC} Testing performance..."

    local start_time=$(date +%s%N)
    local num_requests=10
    local successful_requests=0

    for i in $(seq 1 $num_requests); do
        local test_data="{\"text\":\"Performance test $i\",\"session_id\":\"perf-test\",\"user_id\":\"perf-user\"}"
        local result=$(make_request "POST" "/analyze" "$test_data" "200")
        local status_code=$(echo $result | cut -d'|' -f1)

        if [ "$status_code" = "200" ]; then
            successful_requests=$((successful_requests + 1))
        fi
    done

    local end_time=$(date +%s%N)
    local duration_ms=$(( (end_time - start_time) / 1000000 ))
    local avg_response_time=$(echo "scale=2; $duration_ms / $num_requests" | bc)

    if [ $successful_requests -eq $num_requests ]; then
        if (( $(echo "$avg_response_time < 1000" | bc -l) )); then
            print_result "PASS" "Performance Test" "All $num_requests requests successful, avg response time: ${avg_response_time}ms"
        else
            print_result "WARN" "Performance Test" "All requests successful but slow response time: ${avg_response_time}ms"
        fi
    else
        print_result "FAIL" "Performance Test" "Only $successful_requests/$num_requests requests successful"
    fi
}

test_security_headers() {
    echo -e "\n${BLUE}[TEST]${NC} Testing security headers..."

    local headers=$(curl -s -I "${TEST_BASE_URL}/health")

    # Check for security headers (if implemented)
    if echo "$headers" | grep -i "X-Content-Type-Options" > /dev/null; then
        print_result "PASS" "Security Headers" "X-Content-Type-Options header present"
    else
        print_result "INFO" "Security Headers" "X-Content-Type-Options header not found (may be added by reverse proxy)"
    fi
}

# Main test execution
main() {
    echo -e "${BLUE}[INFO]${NC} Starting Max Cognitive Shield Integration Tests"
    echo -e "${BLUE}[INFO]${NC} Test configuration:"
    echo -e "  Host: $TEST_HOST"
    echo -e "  Port: $TEST_PORT"
    echo -e "  Container: $CONTAINER_NAME"
    echo -e "  Image: $IMAGE_NAME"

    # Build test image
    if ! build_test_image; then
        echo -e "${RED}[ERROR]${NC} Failed to build test image. Exiting."
        exit 1
    fi

    # Start test container
    if ! start_test_container; then
        echo -e "${RED}[ERROR]${NC} Failed to start test container. Exiting."
        exit 1
    fi

    # Wait for service to be ready
    if ! wait_for_service; then
        echo -e "${RED}[ERROR]${NC} Service failed to start. Cleaning up and exiting."
        stop_test_container
        exit 1
    fi

    # Run tests
    echo -e "\n${BLUE}[INFO]${NC} Running integration tests...\n"

    test_health_endpoint
    test_status_endpoint
    test_initialize_session
    test_analyze_normal_input
    test_analyze_stressful_input
    test_intervention_request
    test_session_management
    test_error_handling
    test_performance
    test_security_headers

    # Print test summary
    echo -e "\n${BLUE}[SUMMARY]${NC} Test Results:"
    echo -e "  Total Tests: $TESTS_TOTAL"
    echo -e "  ${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "  ${RED}Failed: $TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}[SUCCESS]${NC} All tests passed!"
        exit_code=0
    else
        echo -e "\n${RED}[FAILURE]${NC} Some tests failed."
        exit_code=1
    fi

    # Cleanup
    stop_test_container

    exit $exit_code
}

# Show usage
show_usage() {
    cat << EOF
Max Cognitive Shield Integration Test Suite

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -H, --host HOST         Test host (default: localhost)
    -p, --port PORT         Test port (default: 8080)
    -c, --container NAME    Container name (default: cognitive-shield-test)
    --no-build              Skip Docker image build
    --no-cleanup            Skip container cleanup

Examples:
    $0                                    # Run with defaults
    $0 --host 127.0.0.1 --port 8081      # Custom host and port
    $0 --no-build                        # Skip build step

EOF
}

# Parse command line arguments
NO_BUILD=false
NO_CLEANUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -H|--host)
            TEST_HOST=$2
            TEST_BASE_URL="http://${TEST_HOST}:${TEST_PORT}"
            shift 2
            ;;
        -p|--port)
            TEST_PORT=$2
            TEST_BASE_URL="http://${TEST_HOST}:${TEST_PORT}"
            shift 2
            ;;
        -c|--container)
            CONTAINER_NAME=$2
            shift 2
            ;;
        --no-build)
            NO_BUILD=true
            shift
            ;;
        --no-cleanup)
            NO_CLEANUP=true
            shift
            ;;
        *)
            echo -e "${RED}[ERROR]${NC} Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Run main test suite
main

# Cleanup trap
trap 'if [ "$NO_CLEANUP" = false ]; then stop_test_container; fi' EXIT