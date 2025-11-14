# Data Integrity Prevention Guide

## Overview

This document outlines procedures to maintain data integrity in the dashboard performance tracking system and prevent issues like model attribution errors.

## Root Causes of Data Inconsistency

### 1. Test Data Contamination
- **Issue**: Test scripts creating records with fake models or test data
- **Impact**: Corrupts dashboard visualizations with incorrect model attribution
- **Prevention**: Always clean up test data immediately after testing

### 2. Model Detection Logic Issues
- **Issue**: Dashboard using heuristics instead of reading actual model data
- **Impact**: Shows wrong model performance for specific dates
- **Prevention**: Use actual `details.model_used` field from assessments

## Prevention Procedures

### Before Running Tests

1. **Backup Production Data**:
   ```bash
   cp .claude-patterns/quality_history.json .claude-patterns/quality_history.json.backup
   cp .claude-patterns/model_performance.json .claude-patterns/model_performance.json.backup
   ```

2. **Use Test-Specific Models**:
   - Always use model names like "Test Model" or "Debug Model" for test records
   - Never use real model names in test data

### During Test Execution

1. **Isolate Test Data**:
   ```python
   # Use test-specific identifiers
   test_task = {
       "model_used": "Test Model",
       "task_type": "test-refactoring",
       "description": "Test refactoring task"
   }
   ```

2. **Use Test Cleanup Function**:
   ```python
   # Call cleanup immediately after tests
   cleanup_test_data()
   ```

### After Test Execution

1. **Verify Data Cleanup**:
   ```bash
   # Check for test data
   grep -i "test" .claude-patterns/quality_history.json
   grep -i "test" .claude-patterns/model_performance.json
   ```

2. **Validate Dashboard**:
   - Load dashboard and verify no test data appears
   - Check model attribution is correct

## Data Validation Checks

### Automatic Validation

Add this function to your dashboard initialization:

```python
def validate_data_integrity():
    """Check for data integrity issues."""
    issues = []

    # Check for test data contamination
    quality_history = load_json("quality_history.json")
    for assessment in quality_history.get("quality_assessments", []):
        if is_test_data(assessment):
            issues.append(f"Test data found: {assessment['assessment_id']}")

    # Check for missing model information
    for assessment in quality_history.get("quality_assessments", []):
        if not assessment.get("details", {}).get("model_used"):
            issues.append(f"Missing model info: {assessment['assessment_id']}")

    return issues

def is_test_data(assessment):
    """Check if assessment is test data."""
    indicators = [
        "test" in assessment.get("assessment_id", "").lower(),
        "test" in assessment.get("task_type", "").lower(),
        "test" in assessment.get("details", {}).get("model_used", "").lower(),
        "test" in assessment.get("details", {}).get("task_description", "").lower()
    ]
    return any(indicators)
```

### Manual Validation Checklist

- [ ] No "Test Model" entries in production data
- [ ] All assessments have valid `details.model_used` field
- [ ] Dashboard shows correct model attribution
- [ ] Timeline data matches actual usage patterns
- [ ] No test dates (like test execution dates) in recent timeline

## Model Attribution Rules

### Correct Model Detection

1. **Read from Assessment Details**:
   ```python
   model_used = assessment.get("details", {}).get("model_used", "Unknown")
   ```

2. **Never Guess Based on Task Type**:
   - Don't assume validation tasks use Claude
   - Don't assume development tasks use GLM
   - Always read the actual model field

3. **Handle Missing Model Data**:
   - Show as "Unknown" rather than guessing
   - Log warnings for missing model information

### Model Name Standardization

Use consistent model names:
- "Claude Sonnet 4.5"
- "GLM 4.6"
- "Test Model" (for tests only)

## Emergency Data Recovery

If data corruption is detected:

1. **Stop All Writing Operations**:
   - Stop the dashboard
   - Stop any automated recording

2. **Backup Current State**:
   ```bash
   cp .claude-patterns/quality_history.json .claude-patterns/quality_history.json.corrupted
   ```

3. **Restore from Backup**:
   ```bash
   cp .claude-patterns/quality_history.json.backup .claude-patterns/quality_history.json
   ```

4. **Validate Recovery**:
   - Run data integrity checks
   - Verify dashboard accuracy

## Monitoring

### Dashboard Health Checks

Add these monitoring endpoints:

```python
@app.route('/api/health/data-integrity')
def data_integrity_health():
    """Check data integrity health."""
    issues = validate_data_integrity()

    return jsonify({
        "status": "healthy" if not issues else "degraded",
        "issues": issues,
        "timestamp": datetime.now().isoformat()
    })
```

### Regular Maintenance

1. **Weekly**: Run data integrity validation
2. **Monthly**: Review model attribution accuracy
3. **Quarterly**: Clean up any accumulated test data

## Troubleshooting

### Common Issues

1. **Test Data in Production**:
   - Run cleanup script
   - Validate removal
   - Update test procedures

2. **Missing Model Information**:
   - Check assessment structure
   - Update recording logic
   - Manual data correction if needed

3. **Incorrect Model Attribution**:
   - Verify dashboard logic uses actual model data
   - Check for hardcoded model assignments
   - Update model detection code

### Debug Commands

```bash
# Check for test data
grep -i "test" .claude-patterns/quality_history.json

# Check model distribution
jq '.quality_assessments[] | .details.model_used' .claude-patterns/quality_history.json | sort | uniq -c

# Validate recent data
jq '.quality_assessments[-5:]' .claude-patterns/quality_history.json
```

## Conclusion

Following these procedures will prevent data integrity issues and ensure accurate model attribution in the dashboard. The key is proper test data isolation and using actual model data rather than heuristics.