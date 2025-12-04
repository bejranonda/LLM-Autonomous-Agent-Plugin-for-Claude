# Release Notes: v7.19.0 - Browser Console Validation with Authentication

**Release Date**: 2025-12-04

## Summary

This release introduces comprehensive browser console error validation with authentication support, screenshot capture, and multi-viewport testing across 14 device presets. The web page validator (`lib/web_page_validator.py`) has been upgraded to v2.0.0 with ~400 lines of new functionality.

## Key Features

### Authentication Support
- **Form-Based Login**: Validate protected pages by automatically logging in
- **Environment Variables**: Credentials via `TEST_EMAIL` and `TEST_PASSWORD` for CI/CD
- **Customizable Selectors**: Configure email, password, and submit button CSS selectors
- **Session Persistence**: Maintain authenticated state across multiple page validations

### Screenshot Capture
- **Automatic Capture**: Screenshot on validation with configurable timing
- **On Error Only**: Capture only when validation fails (default)
- **Full Page**: Option to capture entire scrollable page
- **Organized Storage**: Screenshots saved to `.claude/screenshots/`

### Multi-Viewport Testing
14 device presets covering desktop, mobile, and tablet:

| Category | Presets |
|----------|---------|
| Desktop | desktop (1920x1080), desktop_small (1280x720) |
| iOS | mobile (375x812), mobile_small (320x568), tablet (768x1024), ipad_pro (1024x1366) |
| Android | android_pixel (393x851), android_samsung (360x800), android_tablet (800x1280) |

### React Hydration Error Detection
- **Error #185 Detection**: Automatically detects React hydration mismatches
- **Error Boundary UI**: Detects "Something went wrong" error boundaries
- **Next.js Support**: Detects Next.js hydration warnings

### Error Categorization
10 error categories with severity levels:
- `REACT_HYDRATION` - Critical
- `JAVASCRIPT_SYNTAX` - Critical
- `JAVASCRIPT_RUNTIME` - High
- `NETWORK_FAILURE` - High
- `UNCAUGHT_EXCEPTION` - High
- `RESOURCE_LOADING` - Medium
- `CONSOLE_ERROR` - Medium
- `HTTP_ERROR` - High
- `NAVIGATION_ERROR` - High
- `UNKNOWN` - Low

## Usage Examples

### Basic Validation with Screenshots
```bash
python lib/web_page_validator.py http://localhost:3000 --screenshot
```

### With Authentication
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

### Mobile-Only Validation
```bash
python lib/web_page_validator.py http://localhost:3000 --viewport mobile
```

## Python API

```python
from lib.web_page_validator import (
    WebPageValidator, AuthConfig, ScreenshotConfig, ViewportConfig
)

# Configure authentication
auth = AuthConfig(
    login_url="http://localhost:3000/auth/signin",
    email="test@example.com",
    password="TestPass123!"
)

# Configure screenshots
screenshot_config = ScreenshotConfig(
    enabled=True,
    capture_on_error=True
)

# Validate with authentication
with WebPageValidator(auth_config=auth, screenshot_config=screenshot_config) as validator:
    validator.authenticate()
    result = validator.validate_url('http://localhost:3000/dashboard')

    if result.has_react_hydration_error:
        print("[CRITICAL] React hydration error detected!")
```

## Files Changed

| File | Change |
|------|--------|
| `lib/web_page_validator.py` | Major upgrade to v2.0.0 (+400 lines) |
| `skills/web-validation/SKILL.md` | Updated to v2.0.0 with new sections |
| `docs/BROWSER_CONSOLE_VALIDATION.md` | New consolidated documentation |

## Upgrade Notes

This release is backwards compatible. Existing `validate_url()` calls continue to work unchanged. New features are opt-in via additional parameters and configuration classes.

## Requirements

- Python 3.8+
- Selenium or Playwright (optional, falls back to basic HTTP validation)
- Chrome/Chromium browser (for browser automation)

---

**Full Changelog**: https://github.com/ChildWerapol/llm-autonomous-agent-plugin-for-claude/compare/v7.18.2...v7.19.0
