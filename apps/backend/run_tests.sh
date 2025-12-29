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

# Check if pytest is installed
if ! python -m pytest --version &> /dev/null; then
    echo "ERROR: pytest is not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "Running tests..."
echo ""

# Run tests with options
python -m pytest tests/ \
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
