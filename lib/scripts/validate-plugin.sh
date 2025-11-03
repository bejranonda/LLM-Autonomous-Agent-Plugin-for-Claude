#!/bin/bash
# Plugin Validation Script for Linux/Mac
# Usage: ./validate-plugin.sh [options]

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " Autonomous Agent Plugin Validation"
echo -e "========================================${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}ERROR: Python is not installed${NC}"
        echo "Please install Python from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if plugin validator exists
if [ ! -f "lib/plugin_validator.py" ]; then
    echo -e "${RED}ERROR: Plugin validator not found at lib/plugin_validator.py${NC}"
    echo "Please run this script from the plugin root directory"
    exit 1
fi

# Check if PyYAML is installed
if ! $PYTHON_CMD -c "import yaml" &> /dev/null; then
    echo -e "${YELLOW}Installing PyYAML dependency...${NC}"
    pip install PyYAML
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to install PyYAML${NC}"
        echo "Please run: pip install PyYAML"
        exit 1
    fi
fi

# Run validation with all arguments passed to this script
$PYTHON_CMD lib/plugin_validator.py "$@"
VALIDATION_EXIT_CODE=$?

# Display result based on exit code
echo
if [ $VALIDATION_EXIT_CODE -eq 2 ]; then
    echo -e "${RED}Validation FAILED due to errors${NC}"
    exit 2
elif [ $VALIDATION_EXIT_CODE -eq 1 ]; then
    echo -e "${YELLOW}Validation COMPLETED with issues found${NC}"
    exit 1
else
    echo -e "${GREEN}Validation PASSED successfully${NC}"
    exit 0
fi