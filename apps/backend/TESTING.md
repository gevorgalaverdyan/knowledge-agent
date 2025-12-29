# Backend Testing Documentation

This document describes the comprehensive testing suite for the Knowledge Agent backend.

## Test Suite Overview

The backend testing infrastructure includes **62 comprehensive tests** covering:

- **Unit Tests**: Testing individual functions and components in isolation
- **Integration Tests**: Testing interactions between components and API endpoints
- **Edge Cases**: Boundary conditions and error handling

## Test Categories

### 1. Utility Functions Tests (`test_utils.py`)
**13 tests** covering `utils/utils.py`:

- **Text Chunking**: 
  - Valid section parsing
  - Empty section handling
  - Whitespace normalization
  - Missing section markers

- **Year Extraction**:
  - Valid 2000s and 2020s years
  - Missing year handling
  - Invalid format detection
  - Multiple year scenarios

- **Chat History Formatting**:
  - Empty history
  - Single and multiple messages
  - User vs system message formatting

### 2. TFSA Calculation Tests (`test_calculations.py`)
**16 tests** covering `tools/calculations.py`:

- **Contribution Room Calculations**:
  - Single year contributions
  - Multi-year cumulative totals
  - Historical data from 2009
  - Future year validation (error handling)
  - Special year limits (e.g., 2015's $10,000)
  - Yearly breakdown accuracy
  - Total vs sum validation

- **TFSA Limit Verification**:
  - Complete year coverage (2009-2025)
  - Correct historical limits
  - Special case years
  - Recent year updates

### 3. Retrieval Tools Tests (`test_retrieval.py`)
**7 tests** covering `tools/retrieval.py`:

- **Section Retrieval**:
  - Section object creation
  - Custom and default top_k parameters
  - Empty result handling
  - Optional field defaults
  - Field preservation
  - Query-specific retrieval

### 4. TFSA Agent Tests (`test_agent.py`)
**9 tests** covering `agents/tfsa_agent.py`:

- **Question Handling**:
  - Contribution questions with valid years
  - Missing year error handling
  - Case-insensitive keyword detection
  - Non-contribution question routing
  - Complex question parsing
  - Section context retrieval

- **Tool Integration**:
  - Calculation tool invocation
  - Section retrieval coordination
  - Error message generation

### 5. Prompt Building Tests (`test_prompt.py`)
**13 tests** covering `rag/prompt.py`:

- **Context Building**:
  - Dictionary chunk processing
  - Section object handling
  - Empty list management
  - Single chunk formatting
  - Multi-chunk separation

- **Prompt Construction**:
  - Basic prompt structure
  - Chat history integration
  - Tool result inclusion
  - Instruction completeness
  - Fallback messages
  - Warning inclusion
  - Full parameter handling

### 6. API Endpoint Tests (`test_api_simple.py`)
**4 tests** covering `main.py` and API structure:

- **Root Endpoint**:
  - Health check response
  - JSON structure validation

- **API Structure**:
  - Endpoint registration verification
  - CORS configuration testing

## Running Tests

### Run All Tests
```bash
cd apps/backend
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/ -v
```

### Run Specific Test Suite
```bash
# Unit tests only
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/test_utils.py -v

# Calculation tests
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/test_calculations.py -v

# Agent tests
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/test_agent.py -v
```

### Run with Coverage
```bash
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/ -v --cov=. --cov-report=html
```

Coverage reports are generated in `htmlcov/` directory.

### Run Specific Test
```bash
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/test_calculations.py::TestCalculateTFSAContributionRoom::test_calculate_from_2009 -v
```

## Test Configuration

### pytest.ini
The project uses pytest configuration in `pytest.ini`:
- Test discovery pattern: `test_*.py`
- Verbose output enabled
- Coverage reporting enabled
- Async test support

### Environment Variables
Tests require the following environment variables:
- `DB_URL`: Database connection string (use `sqlite:///:memory:` for tests)
- `GEMINI_API_KEY`: Gemini API key (use `test-key` for mocked tests)

## Test Structure

### Fixtures (`conftest.py`)
Common test fixtures include:
- `mock_gemini_client`: Mocked LLM client
- `mock_retriever`: Mocked FAISS retriever
- `sample_chat_data`: Test data for chat operations

### Mocking Strategy
Tests use `unittest.mock` for:
- External API calls (Gemini)
- Database operations
- FAISS retriever
- File system operations

## Test Coverage

The test suite provides comprehensive coverage of:

1. **Core Business Logic** (100%)
   - TFSA calculation engine
   - Agent decision-making
   - Prompt generation

2. **Utility Functions** (100%)
   - Text processing
   - Date extraction
   - Formatting functions

3. **API Layer** (Basic)
   - Health endpoints
   - Route registration
   - CORS configuration

4. **Edge Cases**
   - Invalid input handling
   - Empty result scenarios
   - Boundary conditions
   - Error messages

## Adding New Tests

When adding new functionality:

1. Create test file: `tests/test_<module_name>.py`
2. Import necessary modules and fixtures
3. Organize tests into classes by functionality
4. Use descriptive test names: `test_<what>_<scenario>`
5. Include docstrings explaining test purpose
6. Mock external dependencies
7. Assert expected behavior
8. Test edge cases and error conditions

Example:
```python
class TestNewFeature:
    """Tests for new feature"""
    
    def test_feature_with_valid_input(self):
        """Test feature handles valid input correctly"""
        # Arrange
        input_data = "test"
        
        # Act
        result = new_feature(input_data)
        
        # Assert
        assert result == expected_output
```

## Continuous Integration

Tests should be run:
- Before committing code
- In CI/CD pipelines
- Before deploying to production

## Dependencies

Testing dependencies (from `requirements.txt`):
- `pytest`: Test framework
- `pytest-asyncio`: Async test support
- `pytest-cov`: Coverage reporting
- `httpx`: HTTP client for API testing
- `sqlalchemy`: Database for integration tests

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the backend directory
2. **Database Errors**: Use in-memory SQLite for tests
3. **API Key Errors**: Set dummy API key for mocked tests
4. **Coverage Issues**: Run with `--no-cov` to skip coverage

### Debug Mode
Run tests with more verbose output:
```bash
DB_URL="sqlite:///:memory:" GEMINI_API_KEY="test-key" python -m pytest tests/ -vv -s
```

## Performance

Test suite performance:
- **Total Tests**: 62
- **Execution Time**: ~1.5 seconds
- **Fast Feedback**: Unit tests run in <0.5s

## Future Improvements

Potential testing enhancements:
1. End-to-end integration tests with real database
2. Performance/load testing
3. Security testing
4. Mutation testing
5. Property-based testing with Hypothesis
