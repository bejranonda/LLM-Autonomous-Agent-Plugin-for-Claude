# Testing Documentation

This document provides comprehensive information about the testing infrastructure for the Autonomous Agent Plugin.

## Overview

The plugin includes a comprehensive testing suite designed to ensure reliability, cross-platform compatibility, and maintainability. The testing framework covers unit tests, integration tests, performance benchmarks, and security validation.

## Test Structure

```
tests/
├── __init__.py                 # Test package configuration
├── conftest.py                 # Shared fixtures and utilities
├── unit/                       # Unit tests for individual components
│   ├── __init__.py
│   ├── test_pattern_storage.py     # Pattern storage system tests
│   ├── test_quality_tracker.py     # Quality tracking tests
│   ├── test_plugin_path_resolver.py # Path resolution tests
│   ├── test_learning_engine.py     # Learning engine tests
│   └── test_agent_feedback_system.py # Agent feedback tests
├── integration/               # Integration tests for component interactions
│   ├── __init__.py
│   └── test_core_integration.py     # Cross-component integration tests
└── fixtures/                   # Test data and fixtures
    └── __init__.py
```

## Core Components Tested

### 1. Pattern Storage System (`test_pattern_storage.py`)

**Coverage Areas:**
- Pattern storage and retrieval
- JSON file handling with cross-platform file locking
- Pattern validation and statistics
- Data corruption handling
- Backward compatibility

**Key Test Cases:**
- Cross-platform file locking (Windows/Linux/macOS)
- Pattern validation (required fields, quality scores)
- Skill effectiveness calculation
- Large dataset performance
- JSON corruption recovery

### 2. Quality Tracker (`test_quality_tracker.py`)

**Coverage Areas:**
- Quality score recording and retrieval
- Trend analysis and statistics
- Metric calculations
- Time-based filtering
- Performance with large datasets

**Key Test Cases:**
- Quality score validation (0-1 range)
- Trend calculation with insufficient data
- Average quality with time filtering
- Metric statistics calculation
- Performance benchmarks (1000+ records)

### 3. Plugin Path Resolver (`test_plugin_path_resolver.py`)

**Coverage Areas:**
- Cross-platform plugin discovery
- Development vs marketplace installations
- Environment variable support
- Path validation and script resolution
- Edge case handling

**Key Test Cases:**
- Windows-specific path handling
- Marketplace plugin detection
- Environment variable override
- Symbolic link handling
- Unicode path support

### 4. Learning Engine (`test_learning_engine.py`)

**Coverage Areas:**
- Learning system initialization
- Pattern capture and storage
- Quality assessment tracking
- Status reporting and analytics
- Data integrity validation

**Key Test Cases:**
- System initialization with project context
- Pattern capture with existing data
- Cross-platform file operations
- Large pattern data handling
- Concurrent access simulation

### 5. Agent Feedback System (`test_agent_feedback_system.py`)

**Coverage Areas:**
- Agent feedback exchange
- Collaboration matrix tracking
- Learning insights management
- Performance statistics
- Cross-group communication

**Key Test Cases:**
- Feedback addition with metadata updates
- Collaboration matrix tracking
- Feedback effectiveness calculation
- Large volume performance testing
- Agent group classification

### 6. Integration Tests (`test_core_integration.py`)

**Coverage Areas:**
- End-to-end workflows
- Cross-component data consistency
- Error propagation and recovery
- Performance under load
- Data consolidation

**Key Test Cases:**
- Complete task execution workflow
- Pattern-quality correlation
- Agent feedback loops
- Cross-platform data consistency
- System-wide status reporting

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### Basic Usage

```bash
# Run all tests with coverage
python run_tests.py

# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run tests without coverage (faster)
python run_tests.py --fast

# Run cross-platform tests
python run_tests.py --platform

# Run performance benchmarks
python run_tests.py --performance

# Generate HTML coverage report
python run_tests.py --report
```

### Advanced Usage

```bash
# Run with specific markers
python run_tests.py --markers "not slow"

# Run code quality checks
python run_tests.py --quality

# Verbose output
python run_tests.py --verbose

# Skip dependency checking
python run_tests.py --no-deps-check
```

### Direct pytest Usage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lib --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_pattern_storage.py

# Run with markers
pytest -m "unit and not slow"

# Run in parallel
pytest -n auto
```

## Test Markers

The test suite uses pytest markers for categorization:

- `@pytest.mark.unit`: Unit tests for individual functions/classes
- `@pytest.mark.integration`: Integration tests for component interactions
- `@pytest.mark.cross_platform`: Tests that must work on all platforms
- `@pytest.mark.windows`: Windows-specific tests
- `@pytest.mark.unix`: Unix/Linux/macOS-specific tests
- `@pytest.mark.slow`: Tests that take significant time to run

## Cross-Platform Testing

### Windows Compatibility

The test suite ensures Windows compatibility through:

1. **File Locking**: Tests both `msvcrt` (Windows) and `fcntl` (Unix) locking mechanisms
2. **Path Separators**: Tests handle both `\` and `/` path separators
3. **Environment Variables**: Tests Windows-specific paths (APPDATA, PROGRAMFILES)
4. **Unicode Handling**: Tests Unicode filenames and paths
5. **Permission Handling**: Tests file permission scenarios

### Platform-Specific Fixtures

```python
@pytest.fixture(params=['Windows', 'Linux', 'Darwin'])
def mock_platform(request):
    """Parametrized fixture for testing on different platforms"""
    with patch('platform.system', return_value=request.param):
        yield request.param
```

## Coverage Requirements

### Target Coverage Metrics

- **Overall Coverage**: 70% minimum (configured in `pytest.ini`)
- **Core Utilities**: 85% target coverage
- **Critical Functions**: 90% target coverage
- **Error Handling**: 80% coverage required

### Coverage Reports

1. **Terminal**: Real-time coverage display during test execution
2. **HTML**: Detailed interactive report (`htmlcov/index.html`)
3. **JSON**: Machine-readable report (`coverage.json`)

### Coverage Exclusions

The following patterns are excluded from coverage calculations:
- Test files (`tests/`)
- Example and demo code
- Configuration files
- Type checking imports
- Debug/development code

## Test Data and Fixtures

### Shared Fixtures

**`conftest.py`** provides common fixtures:

```python
@pytest.fixture
def temp_directory():
    """Create a temporary directory for test files"""

@pytest.fixture
def sample_pattern_data():
    """Sample pattern data for testing"""

@pytest.fixture
def mock_platform():
    """Mock platform for cross-platform testing"""
```

### Test Data Organization

- **Temporary directories**: Created per test for isolation
- **Sample data**: Realistic test data structures
- **Mock objects**: Platform-specific functionality mocking
- **Error scenarios**: Corrupted files, permission errors, etc.

## Performance Testing

### Benchmarks

The test suite includes performance benchmarks for:

1. **Pattern Storage**: 1000+ pattern operations
2. **Quality Tracking**: Large dataset analytics
3. **File Operations**: Cross-platform I/O performance
4. **Memory Usage**: Large data structure handling

### Performance Targets

- **Pattern capture**: < 2 seconds for 1000 patterns
- **Quality analytics**: < 1 second for calculations
- **File operations**: < 5 seconds for large files
- **Test execution**: < 30 seconds for full suite

## Security Testing

### Security Scanners

The test suite integrates with security tools:

```bash
# Run security checks
bandit -r lib/
safety check

# Security-focused tests
pytest -m security
```

### Security Test Areas

- **File Access**: Validates secure file handling
- **Path Traversal**: Prevents directory traversal attacks
- **Input Validation**: Tests data validation and sanitization
- **Code Injection**: Prevents code injection vulnerabilities

## Continuous Integration

### CI Configuration

The test suite is designed for CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Tests
  run: python run_tests.py --fast

- name: Generate Coverage
  run: python run_tests.py --report

- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

### CI Test Matrix

- **Python Versions**: 3.8, 3.9, 3.10, 3.11
- **Platforms**: Windows, Ubuntu, macOS
- **Dependencies**: Multiple versions of key packages

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `lib/` is in Python path
2. **Permission Errors**: Check file permissions on test directories
3. **Coverage Failures**: Verify `pytest-cov` is installed
4. **Platform-Specific Failures**: Check platform-specific requirements

### Debug Mode

Run tests with debug output:

```bash
pytest -v -s --tb=long
```

### Test Isolation

Each test runs in isolation using:
- Temporary directories
- Mock objects
- Database rollbacks
- Process isolation

## Contributing Tests

### Adding New Tests

1. **Follow Naming Conventions**: `test_*.py` for files, `test_*` for functions
2. **Use Fixtures**: Share setup code through fixtures
3. **Add Markers**: Categorize tests with appropriate markers
4. **Document**: Include docstrings explaining test purpose
5. **Cover Edge Cases**: Test error conditions and edge cases

### Test Structure Template

```python
class TestNewFeature:
    """Test suite for new feature"""

    @pytest.fixture
    def setup_data(self):
        """Setup test data"""
        return {}

    @pytest.mark.unit
    def test_happy_path(self, setup_data):
        """Test successful operation"""
        pass

    @pytest.mark.unit
    def test_error_case(self, setup_data):
        """Test error handling"""
        pass

    @pytest.mark.cross_platform
    def test_platform_compatibility(self):
        """Test cross-platform compatibility"""
        pass
```

## Best Practices

### Test Design

1. **Arrange-Act-Assert**: Clear test structure
2. **Single Responsibility**: Each test should test one thing
3. **Descriptive Names**: Test names should describe what they test
4. **Isolation**: Tests should not depend on each other
5. **Deterministic**: Tests should produce consistent results

### Mock Usage

1. **Mock External Dependencies**: Don't test external systems
2. **Use Interfaces**: Mock based on interfaces, not implementation
3. **Verify Interactions**: Check that methods are called correctly
4. **Reset State**: Clean up mocks between tests

### Data Management

1. **Use Factories**: Generate test data programmatically
2. **Boundary Values**: Test minimum, maximum, and edge cases
3. **Realistic Data**: Use realistic test data structures
4. **Cleanup**: Remove test data after test completion

## Test Metrics and KPIs

### Quality Metrics

- **Code Coverage**: Percentage of code covered by tests
- **Test Pass Rate**: Percentage of tests passing
- **Test Execution Time**: Total time to run test suite
- **Flaky Test Rate**: Percentage of tests with inconsistent results

### Performance Metrics

- **Test Suite Duration**: Total execution time
- **Individual Test Duration**: Slowest test identification
- **Memory Usage**: Peak memory during test execution
- **File I/O**: Disk I/O performance during tests

### Maintenance Metrics

- **Test Coverage Trend**: Coverage changes over time
- **Test Growth**: Number of tests added over time
- **Defect Detection**: Number of bugs found by tests
- **Regression Prevention**: Number of regressions caught

## Future Enhancements

### Planned Improvements

1. **Visual Testing**: Screenshot-based UI testing
2. **Load Testing**: High-volume concurrent user testing
3. **Contract Testing**: API contract validation
4. **Mutation Testing**: Code mutation-based test quality
5. **Property-Based Testing**: Hypothesis-based testing

### Tool Integration

1. **IDE Integration**: Better IDE test runner support
2. **Code Coverage IDE**: Real-time coverage in IDE
3. **Automated Reports**: Enhanced test reporting
4. **Test Data Management**: Automated test data generation
5. **Performance Profiling**: Integrated performance profiling