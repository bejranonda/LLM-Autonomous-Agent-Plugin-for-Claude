# Browser Console Error Validation with Authentication

> Documentation integrated from research folder. Original research available in `research/Browser Console Error Validation with Authentication/`.

## Overview

This document describes the browser console error validation system with authentication support, screenshot capture, and mobile/desktop testing capabilities integrated into the plugin.

## Quick Start

### Basic Validation with Screenshots
```bash
python lib/web_page_validator.py http://localhost:3000 --screenshot
```

### Validation with Authentication
```bash
python lib/web_page_validator.py http://localhost:3000/dashboard \
  --auth-url http://localhost:3000/auth/signin \
  --auth-email test@example.com \
  --auth-password TestPass123!
```

### Multi-Viewport Testing
```bash
python lib/web_page_validator.py http://localhost:3000 --viewport all --screenshot --verbose
```

## Components

### Core Module
- **Location**: `lib/web_page_validator.py`
- **Features**: Authentication, screenshots, multi-viewport, error categorization

### Configuration Classes

| Class | Purpose |
|-------|---------|
| `ViewportConfig` | Browser viewport dimensions and device emulation |
| `AuthConfig` | Form-based authentication credentials and selectors |
| `ScreenshotConfig` | Screenshot capture settings |
| `ScreenshotResult` | Screenshot capture result metadata |

### Error Categories

| Category | Pattern | Severity |
|----------|---------|----------|
| `REACT_HYDRATION` | "#185", "hydration" | Critical |
| `JAVASCRIPT_SYNTAX` | "SyntaxError" | Critical |
| `JAVASCRIPT_RUNTIME` | "TypeError", "ReferenceError" | High |
| `NETWORK_FAILURE` | Failed fetch/XHR | High |
| `UNCAUGHT_EXCEPTION` | Unhandled throw | High |
| `CONSOLE_ERROR` | Generic console.error | Medium |

## Device Viewports

### Desktop
- `desktop` - 1920x1080 (Full HD)
- `desktop_small` - 1280x720 (HD)

### iOS Devices
- `mobile` - 375x812 (iPhone X/12/13)
- `mobile_small` - 320x568 (iPhone SE)
- `tablet` - 768x1024 (iPad)
- `ipad_pro` - 1024x1366 (iPad Pro 12.9)

### Android Devices
- `android_pixel` - 393x851 (Pixel 5)
- `android_samsung` - 360x800 (Galaxy S21)
- `android_tablet` - 800x1280 (Android Tablet)

## Authentication Flow

### Form-Based Login
```python
from lib.web_page_validator import WebPageValidator, AuthConfig

auth = AuthConfig(
    login_url="http://localhost:3000/auth/signin",
    email="test@example.com",
    password="TestPass123!",
    email_selector='input[type="email"]',
    password_selector='input[type="password"]',
    submit_selector='button[type="submit"]',
    post_login_wait=2.0,
    typing_delay=50
)

with WebPageValidator(auth_config=auth) as validator:
    validator.authenticate()
    result = validator.validate_url('http://localhost:3000/dashboard')
```

### Environment Variables
```bash
export TEST_EMAIL="test@example.com"
export TEST_PASSWORD="TestPass123!"
```

## Screenshot Capture

### Configuration
```python
from lib.web_page_validator import ScreenshotConfig, ViewportConfig

screenshot_config = ScreenshotConfig(
    enabled=True,
    output_directory=".claude/screenshots",
    capture_on_error=True,
    capture_on_success=False,
    full_page=False,
    format="png",
    viewports=[ViewportConfig.desktop(), ViewportConfig.mobile()]
)
```

### Output
Screenshots are saved to: `.claude/screenshots/{page_name}_{viewport}_{timestamp}.png`

## React Hydration Error Detection

### What is Detected
- Minified React error #185
- "Something went wrong" error boundary
- React Error Overlay presence
- Next.js hydration warnings

### Detection Code
```python
result = validator.validate_url('http://localhost:3000')

if result.has_react_hydration_error:
    print("[CRITICAL] React hydration mismatch detected!")

if result.error_boundary_visible:
    print("[WARN] Error boundary is visible to users!")

for error in result.console_errors:
    if error.is_react_hydration:
        print(f"Hydration error: {error.message}")
```

## CLI Reference

### Basic Arguments
```
--verbose, -v       Show detailed output
--output, -o FILE   Save report to file
--json              Output in JSON format
--no-headless       Show browser window
--timeout N         Page load timeout (default: 30)
--wait N            Wait after load (default: 3)
```

### Authentication Arguments
```
--auth-url URL              Login page URL
--auth-email EMAIL          Login email
--auth-password PASS        Login password
--auth-email-selector SEL   CSS selector for email
--auth-password-selector    CSS selector for password
--auth-submit-selector      CSS selector for submit
```

### Screenshot Arguments
```
--screenshot            Enable screenshots
--screenshot-dir DIR    Output directory
--screenshot-on-error   Only capture on failure
--full-page             Capture full page
```

### Viewport Arguments
```
--viewport PRESET       desktop|mobile|tablet|all
--viewport-width N      Custom width
--viewport-height N     Custom height
```

## Integration Examples

### Python API
```python
from lib.web_page_validator import (
    WebPageValidator, AuthConfig, ScreenshotConfig, ViewportConfig
)

# Full configuration
validator = WebPageValidator(
    headless=True,
    timeout=30,
    auth_config=AuthConfig(login_url="..."),
    screenshot_config=ScreenshotConfig(enabled=True),
    default_viewport=ViewportConfig.mobile()
)

# Multi-page validation
results = validator.validate_pages_with_auth(
    public_pages=[("/", "Home"), ("/about", "About")],
    protected_pages=[("/dashboard", "Dashboard")]
)
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Validate Web App
  run: |
    python lib/web_page_validator.py ${{ env.APP_URL }} \
      --viewport all \
      --screenshot \
      --output validation-report.txt
  env:
    TEST_EMAIL: ${{ secrets.TEST_EMAIL }}
    TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
```

## Common Issues and Solutions

### React Hydration Error #185
- **Cause**: Server-rendered HTML doesn't match client-rendered
- **Solution**: Check for client-only code (window, document access)

### Authentication Failures
- **Cause**: Wrong selectors or timing
- **Solution**: Increase `post_login_wait` or adjust selectors

### Screenshot Capture Fails
- **Cause**: Page not fully loaded
- **Solution**: Increase `--wait` time

### Console Logs Not Captured
- **Cause**: Browser automation unavailable
- **Solution**: Install Selenium or Playwright

## Original Research

For detailed methodology and additional examples, see:
- `research/Browser Console Error Validation with Authentication/README.md`
- `research/Browser Console Error Validation with Authentication/HYDRATION_VALIDATION_GUIDE.md`
- `research/Browser Console Error Validation with Authentication/COMMON_HYDRATION_ISSUES.md`
