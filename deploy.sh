#!/bin/bash

# OpenClaw Skill Deployment Script
# One-click deployment for skill-max-cognitive-shield

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SKILL_NAME="skill-max-cognitive-shield"
SKILL_VERSION="1.0.0"
IMAGE_NAME="${SKILL_NAME}:${SKILL_VERSION}"
CONTAINER_NAME="${SKILL_NAME}-container"
GRPC_PORT=50051
HTTP_PORT=8080

# Default ports (can be overridden by environment variables)
export TARGET_GRPC_PORT=${TARGET_GRPC_PORT:-$GRPC_PORT}
export TARGET_HTTP_PORT=${TARGET_HTTP_PORT:-$HTTP_PORT}

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is required but not installed. Please install $1 and try again."
        exit 1
    fi
}

# Function to check if a port is available
check_port() {
    local port=$1
    local service_name=$2

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port $port is already in use. Attempting to use alternative port."
        return 1
    fi
    return 0
}

# Function to find an available port
find_available_port() {
    local start_port=$1
    local port=$start_port

    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; do
        port=$((port + 1))
        if [ $port -gt 65535 ]; then
            print_error "No available ports found in range $start_port-65535"
            exit 1
        fi
    done

    echo $port
}

# Function to detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)
            echo "linux"
            ;;
        Darwin*)
            echo "macos"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Function to check Docker version
check_docker_version() {
    local docker_version=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "unknown")
    print_status "Docker version: $docker_version"

    # Check if version is >= 20.10
    if [[ "$docker_version" != "unknown" ]]; then
        local major_version=$(echo $docker_version | cut -d'.' -f1)
        local minor_version=$(echo $docker_version | cut -d'.' -f2)

        if [ $major_version -lt 20 ] || ([ $major_version -eq 20 ] && [ $minor_version -lt 10 ]); then
            print_warning "Docker version $docker_version detected. Version 20.10 or higher is recommended."
        fi
    fi
}

# Function to create Docker network if it doesn't exist
create_docker_network() {
    local network_name="openclaw-network"

    if ! docker network ls | grep -q $network_name; then
        print_status "Creating Docker network: $network_name"
        docker network create $network_name
        print_success "Network created: $network_name"
    else
        print_status "Using existing network: $network_name"
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image: $IMAGE_NAME"

    if [ ! -f "Dockerfile.multi" ]; then
        print_error "Dockerfile.multi not found in current directory"
        exit 1
    fi

    docker build -f Dockerfile.multi -t $IMAGE_NAME .

    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully: $IMAGE_NAME"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to run the container
run_container() {
    local grpc_port=$1
    local http_port=$2

    print_status "Starting container: $CONTAINER_NAME"
    print_status "gRPC port: $grpc_port"
    print_status "HTTP port: $http_port"

    # Stop and remove existing container if it exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_status "Stopping existing container: $CONTAINER_NAME"
        docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
        docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
    fi

    # Run the container
    docker run -d \
        --name $CONTAINER_NAME \
        --network openclaw-network \
        -p $grpc_port:50051 \
        -p $http_port:8080 \
        --restart unless-stopped \
        --log-driver json-file \
        --log-opt max-size=10m \
        --log-opt max-file=3 \
        $IMAGE_NAME

    if [ $? -eq 0 ]; then
        print_success "Container started successfully: $CONTAINER_NAME"
    else
        print_error "Failed to start container"
        exit 1
    fi
}

# Function to perform health check
perform_health_check() {
    local http_port=$1
    local max_attempts=30
    local attempt=1

    print_status "Performing health check..."

    while [ $attempt -le $max_attempts ]; do
        print_status "Health check attempt $attempt/$max_attempts"

        if curl -s -f http://localhost:$http_port/health > /dev/null 2>&1; then
            print_success "Health check passed!"
            return 0
        fi

        sleep 2
        attempt=$((attempt + 1))
    done

    print_error "Health check failed after $max_attempts attempts"
    return 1
}

# Function to display deployment summary
display_summary() {
    local grpc_port=$1
    local http_port=$2
    local os_type=$3

    echo
    echo "=============================================="
    echo "  OpenClaw Skill Deployment Summary"
    echo "=============================================="
    echo "Skill Name: $SKILL_NAME"
    echo "Version: $SKILL_VERSION"
    echo "Container: $CONTAINER_NAME"
    echo "OS: $os_type"
    echo
    echo "Ports:"
    echo "  gRPC: $grpc_port"
    echo "  HTTP: $http_port"
    echo
    echo "Endpoints:"
    echo "  Health: http://localhost:$http_port/health"
    echo "  Status: http://localhost:$http_port/status"
    echo "  Analyze: http://localhost:$http_port/analyze"
    echo "  Intervention: http://localhost:$http_port/intervention"
    echo
    echo "Quick Test:"
    echo "  curl http://localhost:$http_port/health"
    echo "  curl http://localhost:$http_port/status"
    echo
    echo "Container Logs:"
    echo "  docker logs $CONTAINER_NAME"
    echo "  docker logs -f $CONTAINER_NAME"
    echo
    echo "Management:"
    echo "  docker stop $CONTAINER_NAME"
    echo "  docker start $CONTAINER_NAME"
    echo "  docker restart $CONTAINER_NAME"
    echo "=============================================="
}

# Function to cleanup on failure
cleanup_on_failure() {
    print_warning "Cleaning up due to deployment failure..."

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
        docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
        print_status "Container removed: $CONTAINER_NAME"
    fi

    print_error "Deployment failed. Please check the logs above for details."
    exit 1
}

# Main deployment function
main() {
    print_status "Starting OpenClaw Skill deployment..."
    print_status "Skill: $SKILL_NAME v$SKILL_VERSION"

    # Detect OS
    local os_type=$(detect_os)
    print_status "Detected OS: $os_type"

    if [ "$os_type" = "unknown" ]; then
        print_warning "Unknown OS detected. Proceeding with generic configuration."
    fi

    # Check required commands
    print_status "Checking prerequisites..."
    check_command "docker"
    check_command "curl"

    # Check Docker version
    check_docker_version

    # Check and find available ports
    print_status "Checking port availability..."

    if ! check_port $TARGET_GRPC_PORT "gRPC"; then
        TARGET_GRPC_PORT=$(find_available_port $((TARGET_GRPC_PORT + 1)))
        print_warning "Using alternative gRPC port: $TARGET_GRPC_PORT"
    fi

    if ! check_port $TARGET_HTTP_PORT "HTTP"; then
        TARGET_HTTP_PORT=$(find_available_port $((TARGET_HTTP_PORT + 1)))
        print_warning "Using alternative HTTP port: $TARGET_HTTP_PORT"
    fi

    # Create Docker network
    create_docker_network

    # Build Docker image
    build_image

    # Run container
    run_container $TARGET_GRPC_PORT $TARGET_HTTP_PORT

    # Perform health check
    if ! perform_health_check $TARGET_HTTP_PORT; then
        cleanup_on_failure
    fi

    # Display summary
    display_summary $TARGET_GRPC_PORT $TARGET_HTTP_PORT $os_type

    print_success "Deployment completed successfully!"
    print_status "Your OpenClaw skill is now running and ready to use."
}

# Function to show usage
show_usage() {
    cat << EOF
OpenClaw Skill Deployment Script

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -g, --grpc-port PORT    gRPC port (default: 50051)
    -H, --http-port PORT    HTTP port (default: 8080)
    -v, --version VERSION   Skill version (default: 1.0.0)
    --no-build              Skip Docker image build
    --no-health-check       Skip health check

Environment Variables:
    TARGET_GRPC_PORT        Override gRPC port
    TARGET_HTTP_PORT        Override HTTP port

Examples:
    $0                                    # Deploy with default ports
    $0 --grpc-port 60051 --http-port 8081   # Deploy with custom ports
    TARGET_GRPC_PORT=60051 $0             # Deploy using environment variables

EOF
}

# Parse command line arguments
NO_BUILD=false
NO_HEALTH_CHECK=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -g|--grpc-port)
            TARGET_GRPC_PORT=$2
            shift 2
            ;;
        -H|--http-port)
            TARGET_HTTP_PORT=$2
            shift 2
            ;;
        -v|--version)
            SKILL_VERSION=$2
            IMAGE_NAME="${SKILL_NAME}:${SKILL_VERSION}"
            shift 2
            ;;
        --no-build)
            NO_BUILD=true
            shift
            ;;
        --no-health-check)
            NO_HEALTH_CHECK=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Export variables for use in functions
export TARGET_GRPC_PORT
export TARGET_HTTP_PORT

# Run main deployment
main

# Trap errors
trap 'cleanup_on_failure' ERR