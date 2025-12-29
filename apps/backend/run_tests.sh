#!/bin/bash

# Backend Test Runner Script
# This script runs the complete test suite for the Knowledge Agent backend

# Set required environment variables for testing
export DB_URL="sqlite:///:memory:"
export GEMINI_API_KEY="test-key-for-testing"

echo "====================================="
echo "Knowledge Agent Backend Test Suite"
echo "====================================="
echo ""

# Check if pytest is installed, try both python and python3
PYTHON_CMD=""
if command -v python &> /dev/null && python -m pytest --version &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null && python3 -m pytest --version &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "ERROR: pytest is not installed or python/python3 not found"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"
echo "Running tests..."
echo ""

# Run tests with options
$PYTHON_CMD -m pytest tests/ \
    -v \
    --tb=short \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html

TEST_EXIT_CODE=$?

echo ""
echo "====================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed"
fi
echo "====================================="
echo ""
echo "Coverage report generated in: htmlcov/index.html"
echo ""

exit $TEST_EXIT_CODE
