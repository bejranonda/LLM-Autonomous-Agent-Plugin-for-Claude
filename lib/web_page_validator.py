#!/usr/bin/env python3
"""
Web Page Validator with JavaScript Error Detection

Automatically validates web pages (like dashboard.py) and detects:
- JavaScript syntax errors
- Console errors, warnings, and logs
- Network request failures
- HTML/CSS validation issues
- Page load performance
- Broken links and resources

Uses Selenium WebDriver for headless browser automation to capture
real browser console output without manual inspection.

Version: 2.0.0
Author: Autonomous Agent Development Team
"""
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict, field
from enum import Enum
import subprocess
import urllib.request
import urllib.error
import os
from collections import defaultdict

# Try to import Selenium for browser automation
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[WARN] Selenium not available. Install with: pip install selenium", file=sys.stderr)

# Try to import playwright as alternative
try:
    from playwright.sync_api import sync_playwright, Error as PlaywrightError

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# =============================================================================
# Error Categories
# =============================================================================

class ErrorCategory(Enum):
    """Categories for console errors with severity levels"""
    REACT_HYDRATION = "react_hydration"        # React #185 and hydration errors
    JAVASCRIPT_SYNTAX = "javascript_syntax"     # SyntaxError
    JAVASCRIPT_RUNTIME = "javascript_runtime"   # TypeError, ReferenceError
    NETWORK_FAILURE = "network_failure"         # Failed HTTP requests
    RESOURCE_LOADING = "resource_loading"       # 404 for CSS/JS/images
    CONSOLE_ERROR = "console_error"             # Generic console.error
    UNCAUGHT_EXCEPTION = "uncaught_exception"   # Unhandled exceptions
    HTTP_ERROR = "http_error"                   # 4xx/5xx responses
    NAVIGATION_ERROR = "navigation_error"       # Page failed to load
    UNKNOWN = "unknown"


# =============================================================================
# Configuration Dataclasses
# =============================================================================

@dataclass
class ViewportConfig:
    """Browser viewport configuration for desktop/mobile testing"""
    name: str               # e.g., "desktop", "mobile", "tablet"
    width: int              # Viewport width in pixels
    height: int             # Viewport height in pixels
    device_scale_factor: float = 1.0    # For retina displays
    is_mobile: bool = False             # Enable mobile emulation
    has_touch: bool = False             # Enable touch events

    @classmethod
    def desktop(cls) -> "ViewportConfig":
        """Full HD desktop viewport (1920x1080)"""
        return cls(name="desktop", width=1920, height=1080)

    @classmethod
    def desktop_small(cls) -> "ViewportConfig":
        """Smaller desktop/laptop viewport (1280x720)"""
        return cls(name="desktop_small", width=1280, height=720)

    @classmethod
    def tablet(cls) -> "ViewportConfig":
        """iPad portrait viewport (768x1024)"""
        return cls(name="tablet", width=768, height=1024, is_mobile=True, has_touch=True)

    @classmethod
    def tablet_landscape(cls) -> "ViewportConfig":
        """iPad landscape viewport (1024x768)"""
        return cls(name="tablet_landscape", width=1024, height=768, is_mobile=True, has_touch=True)

    @classmethod
    def mobile(cls) -> "ViewportConfig":
        """iPhone X/12/13 viewport (375x812)"""
        return cls(name="mobile", width=375, height=812, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    @classmethod
    def mobile_small(cls) -> "ViewportConfig":
        """iPhone SE viewport (320x568)"""
        return cls(name="mobile_small", width=320, height=568, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    @classmethod
    def mobile_landscape(cls) -> "ViewportConfig":
        """Mobile landscape viewport (812x375)"""
        return cls(name="mobile_landscape", width=812, height=375, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    # Android devices
    @classmethod
    def android_pixel(cls) -> "ViewportConfig":
        """Google Pixel 5 viewport (393x851)"""
        return cls(name="android_pixel", width=393, height=851, device_scale_factor=2.75,
                   is_mobile=True, has_touch=True)

    @classmethod
    def android_samsung(cls) -> "ViewportConfig":
        """Samsung Galaxy S21 viewport (360x800)"""
        return cls(name="android_samsung", width=360, height=800, device_scale_factor=3.0,
                   is_mobile=True, has_touch=True)

    @classmethod
    def android_small(cls) -> "ViewportConfig":
        """Small Android device viewport (320x640)"""
        return cls(name="android_small", width=320, height=640, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    # Additional tablets
    @classmethod
    def ipad_pro(cls) -> "ViewportConfig":
        """iPad Pro 12.9 viewport (1024x1366)"""
        return cls(name="ipad_pro", width=1024, height=1366, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    @classmethod
    def ipad_pro_landscape(cls) -> "ViewportConfig":
        """iPad Pro 12.9 landscape viewport (1366x1024)"""
        return cls(name="ipad_pro_landscape", width=1366, height=1024, device_scale_factor=2.0,
                   is_mobile=True, has_touch=True)

    @classmethod
    def android_tablet(cls) -> "ViewportConfig":
        """Android tablet viewport (800x1280)"""
        return cls(name="android_tablet", width=800, height=1280, device_scale_factor=1.5,
                   is_mobile=True, has_touch=True)


@dataclass
class AuthConfig:
    """Configuration for form-based authentication"""
    login_url: str                                  # URL of login page
    email: str = ""                                 # Login email (or use TEST_EMAIL env var)
    password: str = ""                              # Login password (or use TEST_PASSWORD env var)
    email_selector: str = 'input[type="email"]'    # CSS selector for email input
    password_selector: str = 'input[type="password"]'  # CSS selector for password input
    submit_selector: str = 'button[type="submit"]' # CSS selector for submit button
    success_indicator: Optional[str] = None        # Element to verify login success
    post_login_wait: float = 2.0                   # Seconds to wait after login
    typing_delay: int = 50                         # Milliseconds between keystrokes

    def __post_init__(self):
        # Support environment variables for credentials
        if not self.email:
            self.email = os.environ.get("TEST_EMAIL", "")
        if not self.password:
            self.password = os.environ.get("TEST_PASSWORD", "")


@dataclass
class ScreenshotConfig:
    """Configuration for screenshot capture"""
    enabled: bool = True
    output_directory: str = ".claude/screenshots"
    capture_on_error: bool = True           # Always capture on validation failure
    capture_on_success: bool = False        # Optionally capture on success
    full_page: bool = False                 # Capture full scrollable page
    format: str = "png"                     # png or jpeg
    quality: int = 90                       # JPEG quality (1-100)
    viewports: List[ViewportConfig] = None  # Viewports to capture

    def __post_init__(self):
        if self.viewports is None:
            self.viewports = [ViewportConfig.desktop(), ViewportConfig.mobile()]


@dataclass
class ScreenshotResult:
    """Result of screenshot capture"""
    viewport: str                   # Viewport name (e.g., "desktop", "mobile")
    file_path: str                  # Absolute path to screenshot file
    width: int
    height: int
    success: bool
    timestamp: str
    capture_time: float = 0.0       # Time taken to capture in seconds
    error_message: Optional[str] = None


# =============================================================================
# Console Log and Validation Result Dataclasses
# =============================================================================

@dataclass
class ConsoleLog:
    """Represents a browser console log entry with enhanced categorization"""

    level: str  # error, warning, info, log, debug
    message: str
    source: str
    line: Optional[int] = None
    column: Optional[int] = None
    timestamp: str = ""
    # Enhanced fields for error categorization
    category: ErrorCategory = ErrorCategory.UNKNOWN
    stack_trace: Optional[str] = None       # Full stack trace if available
    is_react_hydration: bool = False        # React #185 detection flag
    raw_args: Optional[List[str]] = None    # JSHandle extracted values

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        self._categorize()

    def _categorize(self):
        """Auto-categorize error based on message patterns"""
        if not self.message:
            return

        msg_lower = self.message.lower()

        # React hydration errors (highest priority)
        if "#185" in self.message or "hydration" in msg_lower or "minified react error" in msg_lower:
            self.category = ErrorCategory.REACT_HYDRATION
            self.is_react_hydration = True
        elif "syntaxerror" in msg_lower:
            self.category = ErrorCategory.JAVASCRIPT_SYNTAX
        elif "typeerror" in msg_lower or "referenceerror" in msg_lower:
            self.category = ErrorCategory.JAVASCRIPT_RUNTIME
        elif "uncaught" in msg_lower:
            self.category = ErrorCategory.UNCAUGHT_EXCEPTION
        elif "failed to load" in msg_lower or "404" in self.message:
            self.category = ErrorCategory.RESOURCE_LOADING
        elif "network" in msg_lower or "fetch" in msg_lower or "xhr" in msg_lower:
            self.category = ErrorCategory.NETWORK_FAILURE
        elif self.level in ("error", "severe"):
            self.category = ErrorCategory.CONSOLE_ERROR


@dataclass
class ValidationResult:
    """Comprehensive validation result with screenshot and authentication support"""

    url: str
    success: bool
    load_time: float
    console_errors: List[ConsoleLog]
    console_warnings: List[ConsoleLog]
    console_logs: List[ConsoleLog]
    network_errors: List[Dict[str, Any]]
    javascript_errors: List[str]
    html_issues: List[str]
    performance_metrics: Dict[str, Any]
    page_title: str
    status_code: int
    timestamp: str
    error_summary: str = ""
    # Enhanced fields for screenshots and authentication
    screenshots: List[ScreenshotResult] = None      # Captured screenshots
    authenticated: bool = False                      # Was authentication performed
    has_react_hydration_error: bool = False         # React #185 detected
    error_boundary_visible: bool = False            # Error boundary UI shown
    viewport_tested: Optional[str] = None           # Current viewport name

    def __post_init__(self):
        if self.screenshots is None:
            self.screenshots = []
        self._detect_special_errors()

    def _detect_special_errors(self):
        """Detect special error conditions from console errors"""
        for error in self.console_errors:
            if error.is_react_hydration:
                self.has_react_hydration_error = True
                break

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            "url": self.url,
            "success": self.success,
            "load_time": self.load_time,
            "console_errors": [],
            "console_warnings": [],
            "console_logs": [],
            "network_errors": self.network_errors,
            "javascript_errors": self.javascript_errors,
            "html_issues": self.html_issues,
            "performance_metrics": self.performance_metrics,
            "page_title": self.page_title,
            "status_code": self.status_code,
            "timestamp": self.timestamp,
            "error_summary": self.error_summary,
            "screenshots": [asdict(s) for s in self.screenshots] if self.screenshots else [],
            "authenticated": self.authenticated,
            "has_react_hydration_error": self.has_react_hydration_error,
            "error_boundary_visible": self.error_boundary_visible,
            "viewport_tested": self.viewport_tested,
        }
        # Handle ConsoleLog with Enum (category needs special handling)
        for log in self.console_errors:
            log_dict = asdict(log)
            log_dict["category"] = log.category.value if log.category else "unknown"
            result["console_errors"].append(log_dict)
        for log in self.console_warnings:
            log_dict = asdict(log)
            log_dict["category"] = log.category.value if log.category else "unknown"
            result["console_warnings"].append(log_dict)
        for log in self.console_logs:
            log_dict = asdict(log)
            log_dict["category"] = log.category.value if log.category else "unknown"
            result["console_logs"].append(log_dict)
        return result


class WebPageValidator:
    """Validates web pages with authentication, screenshots, and enhanced error detection"""

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 30,
        auth_config: Optional[AuthConfig] = None,
        screenshot_config: Optional[ScreenshotConfig] = None,
        default_viewport: Optional[ViewportConfig] = None
    ):
        """
        Initialize validator with enhanced configuration

        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in seconds
            auth_config: Authentication configuration for protected pages
            screenshot_config: Screenshot capture configuration
            default_viewport: Default viewport configuration
        """
        self.headless = headless
        self.timeout = timeout
        self.auth_config = auth_config
        self.screenshot_config = screenshot_config or ScreenshotConfig(enabled=False)
        self.default_viewport = default_viewport or ViewportConfig.desktop()
        self.driver = None
        self.browser_type = None
        self._authenticated = False
        self._session_cookies = []
        self._current_viewport = self.default_viewport

    # =========================================================================
    # Viewport Management Methods
    # =========================================================================

    def set_viewport(self, viewport: ViewportConfig) -> None:
        """
        Set browser viewport size

        Args:
            viewport: ViewportConfig with desired dimensions
        """
        self._current_viewport = viewport
        if self.browser_type == "selenium" and self.driver:
            self.driver.set_window_size(viewport.width, viewport.height)

    def get_viewport_presets(self) -> Dict[str, ViewportConfig]:
        """Get all available viewport presets"""
        return {
            # Desktop
            "desktop": ViewportConfig.desktop(),
            "desktop_small": ViewportConfig.desktop_small(),
            # iOS devices
            "mobile": ViewportConfig.mobile(),
            "mobile_small": ViewportConfig.mobile_small(),
            "mobile_landscape": ViewportConfig.mobile_landscape(),
            "tablet": ViewportConfig.tablet(),
            "tablet_landscape": ViewportConfig.tablet_landscape(),
            "ipad_pro": ViewportConfig.ipad_pro(),
            "ipad_pro_landscape": ViewportConfig.ipad_pro_landscape(),
            # Android devices
            "android_pixel": ViewportConfig.android_pixel(),
            "android_samsung": ViewportConfig.android_samsung(),
            "android_small": ViewportConfig.android_small(),
            "android_tablet": ViewportConfig.android_tablet(),
        }

    # =========================================================================
    # Authentication Methods
    # =========================================================================

    def authenticate(self, page=None) -> bool:
        """
        Perform form-based authentication

        Args:
            page: Playwright page or None for Selenium

        Returns:
            bool: True if authentication successful
        """
        if not self.auth_config or not self.auth_config.email:
            print("[WARN] No authentication config or credentials provided", file=sys.stderr)
            return False

        if self.browser_type == "selenium":
            return self._authenticate_selenium()
        else:
            return self._authenticate_playwright(page)

    def _authenticate_selenium(self) -> bool:
        """Selenium-specific authentication with typing simulation"""
        try:
            print(f"[INFO] Navigating to login page: {self.auth_config.login_url}")
            self.driver.get(self.auth_config.login_url)
            time.sleep(1)  # Wait for form to load

            # Find and fill email
            from selenium.webdriver.common.keys import Keys
            email_input = self.driver.find_element(By.CSS_SELECTOR, self.auth_config.email_selector)
            email_input.clear()
            for char in self.auth_config.email:
                email_input.send_keys(char)
                time.sleep(self.auth_config.typing_delay / 1000)

            # Find and fill password
            password_input = self.driver.find_element(By.CSS_SELECTOR, self.auth_config.password_selector)
            password_input.clear()
            for char in self.auth_config.password:
                password_input.send_keys(char)
                time.sleep(self.auth_config.typing_delay / 1000)

            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, self.auth_config.submit_selector)
            submit_button.click()

            # Wait for navigation
            time.sleep(self.auth_config.post_login_wait)

            # Store cookies for session persistence
            self._session_cookies = self.driver.get_cookies()
            self._authenticated = True

            print("[OK] Authentication successful")
            return True

        except Exception as e:
            print(f"[ERROR] Authentication failed: {e}", file=sys.stderr)
            return False

    def _authenticate_playwright(self, page) -> bool:
        """Playwright-specific authentication with typing simulation"""
        try:
            print(f"[INFO] Navigating to login page: {self.auth_config.login_url}")
            page.goto(self.auth_config.login_url, wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Fill form with typing simulation
            page.type(self.auth_config.email_selector, self.auth_config.email,
                      delay=self.auth_config.typing_delay)
            page.type(self.auth_config.password_selector, self.auth_config.password,
                      delay=self.auth_config.typing_delay)

            # Submit and wait
            page.click(self.auth_config.submit_selector)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(int(self.auth_config.post_login_wait * 1000))

            self._authenticated = True
            print("[OK] Authentication successful")
            return True

        except Exception as e:
            print(f"[ERROR] Playwright authentication failed: {e}", file=sys.stderr)
            return False

    # =========================================================================
    # Screenshot Capture Methods
    # =========================================================================

    def capture_screenshot(
        self,
        page=None,
        viewport: Optional[ViewportConfig] = None,
        page_name: str = "page"
    ) -> ScreenshotResult:
        """
        Capture screenshot of current page

        Args:
            page: Playwright page or None for Selenium
            viewport: Viewport configuration (uses current if None)
            page_name: Name for the screenshot file

        Returns:
            ScreenshotResult with file path and metadata
        """
        viewport = viewport or self._current_viewport
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create output directory
        output_dir = Path(self.screenshot_config.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename: page-name_viewport_timestamp.png
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in page_name)
        filename = f"{safe_name}_{viewport.name}_{timestamp}.{self.screenshot_config.format}"
        file_path = output_dir / filename

        start_time = time.time()

        try:
            if self.browser_type == "selenium":
                self.driver.save_screenshot(str(file_path))
            else:
                screenshot_options = {
                    "path": str(file_path),
                    "full_page": self.screenshot_config.full_page,
                }
                if self.screenshot_config.format == "jpeg":
                    screenshot_options["quality"] = self.screenshot_config.quality
                page.screenshot(**screenshot_options)

            capture_time = time.time() - start_time

            return ScreenshotResult(
                viewport=viewport.name,
                file_path=str(file_path.absolute()),
                width=viewport.width,
                height=viewport.height,
                success=True,
                timestamp=datetime.now().isoformat(),
                capture_time=capture_time
            )

        except Exception as e:
            return ScreenshotResult(
                viewport=viewport.name,
                file_path="",
                width=viewport.width,
                height=viewport.height,
                success=False,
                timestamp=datetime.now().isoformat(),
                capture_time=0.0,
                error_message=str(e)
            )

    def capture_multi_viewport_screenshots(
        self,
        url: str,
        page_name: str = "page",
        page=None
    ) -> List[ScreenshotResult]:
        """
        Capture screenshots across multiple viewports

        Args:
            url: URL to capture
            page_name: Name for screenshot files
            page: Playwright page or None for Selenium

        Returns:
            List of ScreenshotResults for each viewport
        """
        results = []

        for viewport in self.screenshot_config.viewports:
            # Set viewport
            self.set_viewport(viewport)

            # Reload page to re-render with new viewport
            if self.browser_type == "selenium":
                self.driver.get(url)
                time.sleep(1)  # Wait for rerender
            elif page:
                page.set_viewport_size({"width": viewport.width, "height": viewport.height})
                page.reload()
                page.wait_for_load_state("networkidle")

            # Capture screenshot
            result = self.capture_screenshot(page=page, viewport=viewport, page_name=page_name)
            results.append(result)

        return results

    # =========================================================================
    # Enhanced Error Detection Methods
    # =========================================================================

    def _detect_error_boundary(self, page=None) -> bool:
        """
        Detect if React error boundary is visible

        Args:
            page: Playwright page or None for Selenium

        Returns:
            True if error boundary UI is detected
        """
        try:
            if self.browser_type == "selenium":
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
            else:
                body_text = page.evaluate("() => document.body.innerText")

            # Common error boundary messages
            error_patterns = [
                "Something went wrong",
                "An error occurred",
                "Application error",
                "Error boundary",
                "Minified React error"
            ]

            return any(pattern.lower() in body_text.lower() for pattern in error_patterns)

        except Exception:
            return False

    def _check_react_hydration_errors(self, page=None) -> List[Dict[str, Any]]:
        """
        Check for React hydration errors using page evaluation

        Args:
            page: Playwright page or None for Selenium

        Returns:
            List of detected hydration errors
        """
        js_check = """
        () => {
            const errors = [];

            // Check for React error overlay
            if (window.__REACT_ERROR_OVERLAY_GLOBAL_HOOK__) {
                errors.push({
                    source: 'React Error Overlay',
                    present: true
                });
            }

            // Check for Next.js hydration warning
            if (window.__NEXT_DATA__ && window.__NEXT_DATA__.err) {
                errors.push({
                    source: 'Next.js Error',
                    message: window.__NEXT_DATA__.err.message || 'Unknown error'
                });
            }

            // Check body text for error boundary
            const bodyText = document.body.innerText || '';
            if (bodyText.includes('Something went wrong') ||
                bodyText.includes('Minified React error')) {
                errors.push({
                    source: 'Error Boundary',
                    visible: true,
                    text: bodyText.substring(0, 500)
                });
            }

            return errors;
        }
        """

        try:
            if self.browser_type == "selenium":
                return self.driver.execute_script(js_check) or []
            else:
                return page.evaluate(js_check) or []
        except Exception:
            return []

    # =========================================================================
    # Browser Initialization Methods
    # =========================================================================

    def _init_selenium_driver(self) -> bool:
        """Initialize Selenium WebDriver with viewport settings"""
        if not SELENIUM_AVAILABLE:
            return False

        try:
            chrome_options = ChromeOptions()
            if self.headless:
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            # Use configured viewport size
            viewport = self._current_viewport
            chrome_options.add_argument(f"--window-size={viewport.width},{viewport.height}")

            # Enable console log capture
            chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            self.browser_type = "selenium"
            return True

        except Exception as e:
            print(f"[ERROR] Failed to initialize Chrome WebDriver: {e}", file=sys.stderr)
            print("[INFO] Install ChromeDriver: https://chromedriver.chromium.org/", file=sys.stderr)
            return False

    def _init_playwright_browser(self):
        """Initialize Playwright browser"""
        if not PLAYWRIGHT_AVAILABLE:
            return None

        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=self.headless)
            self.browser_type = "playwright"
            return browser, playwright
        except Exception as e:
            print(f"[ERROR] Failed to initialize Playwright: {e}", file=sys.stderr)
            return None

    def validate_url(
        self,
        url: str,
        wait_for_load: int = 3,
        viewport: Optional[ViewportConfig] = None,
        capture_screenshots: bool = None
    ) -> ValidationResult:
        """
        Validate a web page URL with enhanced error detection

        Args:
            url: URL to validate
            wait_for_load: Seconds to wait after page load for JavaScript execution
            viewport: Viewport configuration (uses default if None)
            capture_screenshots: Override screenshot config

        Returns:
            ValidationResult with all detected issues and screenshots
        """
        # Set viewport if specified
        if viewport:
            self.set_viewport(viewport)

        if SELENIUM_AVAILABLE:
            return self._validate_with_selenium(url, wait_for_load, capture_screenshots)
        elif PLAYWRIGHT_AVAILABLE:
            return self._validate_with_playwright(url, wait_for_load, capture_screenshots)
        else:
            return self._validate_basic(url)

    def _validate_with_selenium(
        self,
        url: str,
        wait_for_load: int,
        capture_screenshots: bool = None
    ) -> ValidationResult:
        """Validate using Selenium WebDriver with enhanced error detection"""
        console_errors = []
        console_warnings = []
        console_logs = []
        javascript_errors = []
        network_errors = []
        screenshots = []

        # Determine if screenshots should be captured
        should_screenshot = capture_screenshots if capture_screenshots is not None \
                           else self.screenshot_config.enabled

        start_time = time.time()

        try:
            if not self.driver and not self._init_selenium_driver():
                raise Exception("Failed to initialize Selenium WebDriver")

            # Navigate to URL
            self.driver.get(url)

            # Wait for page to load
            time.sleep(wait_for_load)

            # Get page title
            page_title = self.driver.title

            # Capture console logs
            logs = self.driver.get_log("browser")
            for log in logs:
                level = log.get("level", "INFO").lower()
                message = log.get("message", "")
                source = log.get("source", "unknown")

                console_log = ConsoleLog(
                    level=level,
                    message=message,
                    source=source,
                    timestamp=datetime.fromtimestamp(log.get("timestamp", 0) / 1000).isoformat(),
                )

                if level == "severe" or "error" in level:
                    console_errors.append(console_log)
                    if "SyntaxError" in message or "Uncaught" in message:
                        javascript_errors.append(message)
                elif level == "warning":
                    console_warnings.append(console_log)
                else:
                    console_logs.append(console_log)

            # Check for JavaScript errors using window.onerror
            js_errors = self.driver.execute_script(
                "return window.__jsErrors || [];"
            )
            javascript_errors.extend(js_errors)

            # Get performance metrics
            performance = self.driver.execute_script(
                """
                const perf = performance.timing;
                return {
                    loadTime: perf.loadEventEnd - perf.navigationStart,
                    domReady: perf.domContentLoadedEventEnd - perf.navigationStart,
                    responseTime: perf.responseEnd - perf.requestStart
                };
                """
            )

            load_time = time.time() - start_time

            # Check for network errors using Resource Timing API
            resources = self.driver.execute_script(
                """
                return performance.getEntriesByType('resource').map(r => ({
                    name: r.name,
                    duration: r.duration,
                    transferSize: r.transferSize,
                    failed: r.transferSize === 0 && r.duration > 0
                }));
                """
            )

            network_errors = [r for r in resources if r.get("failed")]

            # Check for error boundary
            error_boundary_visible = self._detect_error_boundary()

            # Check for React hydration errors
            hydration_errors = self._check_react_hydration_errors()
            if hydration_errors:
                for he in hydration_errors:
                    console_errors.append(ConsoleLog(
                        level="error",
                        message=f"React hydration error: {he.get('source', 'unknown')}",
                        source="page_evaluation",
                        category=ErrorCategory.REACT_HYDRATION,
                        is_react_hydration=True
                    ))

            # Capture screenshots if enabled
            has_errors = len(console_errors) > 0 or len(javascript_errors) > 0
            if should_screenshot:
                if self.screenshot_config.capture_on_success or \
                   (self.screenshot_config.capture_on_error and has_errors):
                    # Extract page name from URL
                    from urllib.parse import urlparse
                    page_name = urlparse(url).path.strip('/').replace('/', '_') or 'home'
                    screenshot = self.capture_screenshot(page_name=page_name)
                    if screenshot.success:
                        screenshots.append(screenshot)

            # Build error summary
            error_summary = self._build_error_summary(
                len(console_errors), len(console_warnings), len(javascript_errors), len(network_errors)
            )

            return ValidationResult(
                url=url,
                success=len(console_errors) == 0 and len(javascript_errors) == 0,
                load_time=load_time,
                console_errors=console_errors,
                console_warnings=console_warnings,
                console_logs=console_logs,
                network_errors=network_errors,
                javascript_errors=javascript_errors,
                html_issues=[],
                performance_metrics=performance,
                page_title=page_title,
                status_code=200,
                timestamp=datetime.now().isoformat(),
                error_summary=error_summary,
                screenshots=screenshots,
                authenticated=self._authenticated,
                error_boundary_visible=error_boundary_visible,
                viewport_tested=self._current_viewport.name,
            )

        except TimeoutException:
            return self._create_error_result(url, f"Page load timeout after {self.timeout}s")
        except WebDriverException as e:
            return self._create_error_result(url, f"WebDriver error: {str(e)}")
        except Exception as e:
            return self._create_error_result(url, f"Validation error: {str(e)}")

    def _validate_with_playwright(
        self,
        url: str,
        wait_for_load: int,
        capture_screenshots: bool = None
    ) -> ValidationResult:
        """Validate using Playwright with enhanced error detection"""
        console_errors = []
        console_warnings = []
        console_logs = []
        javascript_errors = []
        network_errors = []
        screenshots = []

        # Determine if screenshots should be captured
        should_screenshot = capture_screenshots if capture_screenshots is not None \
                           else self.screenshot_config.enabled

        start_time = time.time()
        browser_data = self._init_playwright_browser()

        if not browser_data:
            return self._validate_basic(url)

        browser, playwright = browser_data

        try:
            # Create context with viewport settings
            viewport = self._current_viewport
            context = browser.new_context(
                viewport={"width": viewport.width, "height": viewport.height},
                device_scale_factor=viewport.device_scale_factor,
                is_mobile=viewport.is_mobile,
                has_touch=viewport.has_touch,
            )
            page = context.new_page()

            # Capture console logs
            def handle_console(msg):
                level = msg.type
                message = msg.text

                console_log = ConsoleLog(level=level, message=message, source="console")

                if level == "error":
                    console_errors.append(console_log)
                    if "SyntaxError" in message or "Uncaught" in message:
                        javascript_errors.append(message)
                elif level == "warning":
                    console_warnings.append(console_log)
                else:
                    console_logs.append(console_log)

            page.on("console", handle_console)

            # Capture page errors
            def handle_page_error(error):
                javascript_errors.append(str(error))

            page.on("pageerror", handle_page_error)

            # Navigate and wait
            response = page.goto(url, timeout=self.timeout * 1000)
            page.wait_for_load_state("networkidle")
            time.sleep(wait_for_load)

            load_time = time.time() - start_time
            page_title = page.title()
            status_code = response.status if response else 0

            # Get performance metrics
            performance = page.evaluate(
                """() => {
                const perf = performance.timing;
                return {
                    loadTime: perf.loadEventEnd - perf.navigationStart,
                    domReady: perf.domContentLoadedEventEnd - perf.navigationStart,
                    responseTime: perf.responseEnd - perf.requestStart
                };
            }"""
            )

            # Check for error boundary
            error_boundary_visible = self._detect_error_boundary(page)

            # Check for React hydration errors
            hydration_errors = self._check_react_hydration_errors(page)
            if hydration_errors:
                for he in hydration_errors:
                    console_errors.append(ConsoleLog(
                        level="error",
                        message=f"React hydration error: {he.get('source', 'unknown')}",
                        source="page_evaluation",
                        category=ErrorCategory.REACT_HYDRATION,
                        is_react_hydration=True
                    ))

            # Capture screenshots if enabled
            has_errors = len(console_errors) > 0 or len(javascript_errors) > 0
            if should_screenshot:
                if self.screenshot_config.capture_on_success or \
                   (self.screenshot_config.capture_on_error and has_errors):
                    from urllib.parse import urlparse
                    page_name = urlparse(url).path.strip('/').replace('/', '_') or 'home'
                    screenshot = self.capture_screenshot(page=page, page_name=page_name)
                    if screenshot.success:
                        screenshots.append(screenshot)

            error_summary = self._build_error_summary(
                len(console_errors), len(console_warnings), len(javascript_errors), len(network_errors)
            )

            return ValidationResult(
                url=url,
                success=len(console_errors) == 0 and len(javascript_errors) == 0,
                load_time=load_time,
                console_errors=console_errors,
                console_warnings=console_warnings,
                console_logs=console_logs,
                network_errors=network_errors,
                javascript_errors=javascript_errors,
                html_issues=[],
                performance_metrics=performance,
                page_title=page_title,
                status_code=status_code,
                timestamp=datetime.now().isoformat(),
                error_summary=error_summary,
                screenshots=screenshots,
                authenticated=self._authenticated,
                error_boundary_visible=error_boundary_visible,
                viewport_tested=self._current_viewport.name,
            )

        except PlaywrightError as e:
            return self._create_error_result(url, f"Playwright error: {str(e)}")
        except Exception as e:
            return self._create_error_result(url, f"Validation error: {str(e)}")
        finally:
            browser.close()
            playwright.stop()

    def _validate_basic(self, url: str) -> ValidationResult:
        """Basic validation without browser automation"""
        start_time = time.time()

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WebPageValidator/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8")
                status_code = response.status
                load_time = time.time() - start_time

                # Basic checks
                javascript_errors = []
                html_issues = []

                # Check for common JavaScript error patterns in HTML
                if "SyntaxError" in content:
                    javascript_errors.append("Potential SyntaxError found in page content")
                if "Uncaught" in content:
                    javascript_errors.append("Potential Uncaught error found in page content")

                # Extract title
                import re

                title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
                page_title = title_match.group(1) if title_match else "No title"

                return ValidationResult(
                    url=url,
                    success=status_code == 200,
                    load_time=load_time,
                    console_errors=[],
                    console_warnings=[],
                    console_logs=[],
                    network_errors=[],
                    javascript_errors=javascript_errors,
                    html_issues=html_issues,
                    performance_metrics={"loadTime": load_time * 1000},
                    page_title=page_title,
                    status_code=status_code,
                    timestamp=datetime.now().isoformat(),
                    error_summary=f"Basic validation only (browser automation unavailable)",
                )

        except urllib.error.HTTPError as e:
            return self._create_error_result(url, f"HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            return self._create_error_result(url, f"URL error: {e.reason}")
        except Exception as e:
            return self._create_error_result(url, f"Request failed: {str(e)}")

    def _build_error_summary(self, errors: int, warnings: int, js_errors: int, network_errors: int) -> str:
        """Build human-readable error summary"""
        parts = []
        if errors > 0:
            parts.append(f"{errors} console error(s)")
        if warnings > 0:
            parts.append(f"{warnings} warning(s)")
        if js_errors > 0:
            parts.append(f"{js_errors} JavaScript error(s)")
        if network_errors > 0:
            parts.append(f"{network_errors} network error(s)")

        if not parts:
            return "No errors detected"
        return ", ".join(parts)

    def _create_error_result(self, url: str, error_msg: str) -> ValidationResult:
        """Create error result"""
        return ValidationResult(
            url=url,
            success=False,
            load_time=0.0,
            console_errors=[ConsoleLog(level="error", message=error_msg, source="validator")],
            console_warnings=[],
            console_logs=[],
            network_errors=[],
            javascript_errors=[],
            html_issues=[],
            performance_metrics={},
            page_title="",
            status_code=0,
            timestamp=datetime.now().isoformat(),
            error_summary=error_msg,
        )

    def close(self):
        """Cleanup browser resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # =========================================================================
    # Multi-Page Validation with Authentication
    # =========================================================================

    def validate_pages_with_auth(
        self,
        public_pages: List[Tuple[str, str]],
        protected_pages: List[Tuple[str, str]],
        viewports: Optional[List[ViewportConfig]] = None
    ) -> Dict[str, List[ValidationResult]]:
        """
        Validate multiple pages, handling authentication for protected pages

        Args:
            public_pages: List of (url, name) tuples for public pages
            protected_pages: List of (url, name) tuples requiring auth
            viewports: List of viewports to test (optional)

        Returns:
            Dict with 'public' and 'protected' keys containing ValidationResults
        """
        results = {"public": [], "protected": []}
        viewports = viewports or [self._current_viewport]

        # Initialize browser if needed
        if SELENIUM_AVAILABLE and not self.driver:
            self._init_selenium_driver()

        # Validate public pages first
        print("[INFO] Validating public pages...")
        for url, name in public_pages:
            for viewport in viewports:
                self.set_viewport(viewport)
                print(f"  Testing: {name} ({viewport.name})")
                result = self.validate_url(url)
                result.viewport_tested = viewport.name
                results["public"].append(result)

        # Authenticate if needed
        if protected_pages and self.auth_config:
            print("[INFO] Authenticating for protected pages...")
            if not self.authenticate():
                # Return error results for all protected pages
                print("[ERROR] Authentication failed, skipping protected pages")
                for url, name in protected_pages:
                    results["protected"].append(
                        self._create_error_result(url, "Authentication failed")
                    )
                return results

        # Validate protected pages
        print("[INFO] Validating protected pages...")
        for url, name in protected_pages:
            for viewport in viewports:
                self.set_viewport(viewport)
                print(f"  Testing: {name} ({viewport.name})")
                result = self.validate_url(url)
                result.viewport_tested = viewport.name
                result.authenticated = True
                results["protected"].append(result)

        return results

    def validate_all_viewports(
        self,
        url: str,
        page_name: str = "page",
        viewports: Optional[List[str]] = None
    ) -> List[ValidationResult]:
        """
        Validate a URL across all or specified viewports

        Args:
            url: URL to validate
            page_name: Name for the page (used in screenshots)
            viewports: List of viewport names or None for all

        Returns:
            List of ValidationResults for each viewport
        """
        results = []
        presets = self.get_viewport_presets()

        if viewports:
            # Use specified viewports
            viewport_configs = [presets[v] for v in viewports if v in presets]
        else:
            # Use default desktop and mobile
            viewport_configs = [
                ViewportConfig.desktop(),
                ViewportConfig.mobile(),
            ]

        for viewport in viewport_configs:
            self.set_viewport(viewport)
            result = self.validate_url(url)
            result.viewport_tested = viewport.name
            results.append(result)

        return results


def format_validation_report(result: ValidationResult, verbose: bool = False) -> str:
    """Format validation result as readable report with enhanced details"""
    lines = []
    lines.append("=" * 80)
    lines.append("WEB PAGE VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"URL: {result.url}")
    lines.append(f"Status: {'[OK] PASSED' if result.success else '[ERROR] FAILED'}")
    lines.append(f"Load Time: {result.load_time:.2f}s")
    lines.append(f"Page Title: {result.page_title}")
    lines.append(f"Timestamp: {result.timestamp}")
    if result.viewport_tested:
        lines.append(f"Viewport: {result.viewport_tested}")
    if result.authenticated:
        lines.append(f"Authenticated: Yes")
    lines.append("")

    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Console Errors: {len(result.console_errors)}")
    lines.append(f"Console Warnings: {len(result.console_warnings)}")
    lines.append(f"JavaScript Errors: {len(result.javascript_errors)}")
    lines.append(f"Network Errors: {len(result.network_errors)}")
    if result.has_react_hydration_error:
        lines.append(f"React Hydration Error: [CRITICAL] DETECTED")
    if result.error_boundary_visible:
        lines.append(f"Error Boundary: [WARN] VISIBLE")
    lines.append(f"Status: {result.error_summary}")
    lines.append("")

    # Screenshots
    if result.screenshots:
        lines.append("SCREENSHOTS")
        lines.append("-" * 80)
        for i, ss in enumerate(result.screenshots, 1):
            status = "[OK]" if ss.success else "[ERROR]"
            lines.append(f"{i}. {status} {ss.viewport} ({ss.width}x{ss.height})")
            if ss.success:
                lines.append(f"   File: {ss.file_path}")
            else:
                lines.append(f"   Error: {ss.error_message}")
        lines.append("")

    # Console Errors with categorization
    if result.console_errors:
        lines.append("CONSOLE ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.console_errors, 1):
            category_tag = f"[{error.category.value.upper()}]" if error.category else ""
            hydration_tag = "[HYDRATION]" if error.is_react_hydration else ""
            lines.append(f"{i}. [{error.level.upper()}] {category_tag} {hydration_tag}")
            lines.append(f"   Message: {error.message[:200]}{'...' if len(error.message) > 200 else ''}")
            if error.source and error.source != "unknown":
                lines.append(f"   Source: {error.source}")
            if error.stack_trace and verbose:
                lines.append(f"   Stack: {error.stack_trace[:300]}...")
            if error.line:
                lines.append(f"   Line: {error.line}, Column: {error.column}")
            lines.append(f"   Time: {error.timestamp}")
            lines.append("")

    # Console Warnings
    if result.console_warnings and verbose:
        lines.append("CONSOLE WARNINGS")
        lines.append("-" * 80)
        for i, warning in enumerate(result.console_warnings, 1):
            lines.append(f"{i}. [{warning.level.upper()}] {warning.message}")
            lines.append("")

    # JavaScript Errors
    if result.javascript_errors:
        lines.append("JAVASCRIPT ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.javascript_errors, 1):
            lines.append(f"{i}. {error}")
        lines.append("")

    # Network Errors
    if result.network_errors:
        lines.append("NETWORK ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.network_errors, 1):
            lines.append(f"{i}. {error.get('name', 'Unknown resource')}")
            lines.append(f"   Duration: {error.get('duration', 0):.2f}ms")
        lines.append("")

    # Performance Metrics
    if result.performance_metrics and verbose:
        lines.append("PERFORMANCE METRICS")
        lines.append("-" * 80)
        for key, value in result.performance_metrics.items():
            lines.append(f"{key}: {value}")
        lines.append("")

    # Recommendations
    if not result.success:
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        if result.javascript_errors:
            lines.append("1. Fix JavaScript syntax errors in source files")
            lines.append("2. Use Python raw strings (r'...') for JavaScript escape sequences")
            lines.append("3. Validate JavaScript code before deployment")
        if result.network_errors:
            lines.append("4. Check network requests and resource URLs")
            lines.append("5. Verify all static assets are accessible")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    """Main CLI interface with authentication, screenshot, and viewport support"""
    parser = argparse.ArgumentParser(
        description="Web Page Validator with Authentication, Screenshots, and Enhanced Error Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python web_page_validator.py http://127.0.0.1:5000

  # Validation with screenshots
  python web_page_validator.py http://127.0.0.1:5000 --screenshot

  # Validation with authentication
  python web_page_validator.py http://127.0.0.1:5000/dashboard \\
    --auth-url http://127.0.0.1:5000/auth/signin \\
    --auth-email test@example.com \\
    --auth-password TestPass123!

  # Multi-viewport validation with screenshots
  python web_page_validator.py http://127.0.0.1:5000 \\
    --viewport all --screenshot --verbose

  # Mobile-only validation
  python web_page_validator.py http://127.0.0.1:5000 --viewport mobile

Available viewports: desktop, desktop_small, mobile, mobile_small, tablet,
                     ipad_pro, android_pixel, android_samsung, android_tablet
        """,
    )

    # Basic arguments
    parser.add_argument("url", help="URL to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output including warnings")
    parser.add_argument("--output", "-o", help="Save report to file")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window (for debugging)")
    parser.add_argument("--timeout", type=int, default=30, help="Page load timeout in seconds (default: 30)")
    parser.add_argument("--wait", type=int, default=3, help="Wait time after page load in seconds (default: 3)")

    # Authentication arguments
    auth_group = parser.add_argument_group("Authentication")
    auth_group.add_argument("--auth-url", help="Login page URL")
    auth_group.add_argument("--auth-email", help="Login email (or set TEST_EMAIL env var)")
    auth_group.add_argument("--auth-password", help="Login password (or set TEST_PASSWORD env var)")
    auth_group.add_argument("--auth-email-selector", default='input[type="email"]',
                            help="CSS selector for email input")
    auth_group.add_argument("--auth-password-selector", default='input[type="password"]',
                            help="CSS selector for password input")
    auth_group.add_argument("--auth-submit-selector", default='button[type="submit"]',
                            help="CSS selector for submit button")

    # Screenshot arguments
    screenshot_group = parser.add_argument_group("Screenshots")
    screenshot_group.add_argument("--screenshot", action="store_true",
                                  help="Capture screenshots")
    screenshot_group.add_argument("--screenshot-dir", default=".claude/screenshots",
                                  help="Screenshot output directory (default: .claude/screenshots)")
    screenshot_group.add_argument("--screenshot-on-error", action="store_true",
                                  help="Only capture screenshots on validation failure")
    screenshot_group.add_argument("--full-page", action="store_true",
                                  help="Capture full scrollable page")

    # Viewport arguments
    viewport_group = parser.add_argument_group("Viewport")
    viewport_group.add_argument("--viewport", default="desktop",
                                help="Viewport preset: desktop, mobile, tablet, all, or specific name")
    viewport_group.add_argument("--viewport-width", type=int, help="Custom viewport width")
    viewport_group.add_argument("--viewport-height", type=int, help="Custom viewport height")

    args = parser.parse_args()

    # Build auth config if provided
    auth_config = None
    if args.auth_url:
        auth_config = AuthConfig(
            login_url=args.auth_url,
            email=args.auth_email or "",
            password=args.auth_password or "",
            email_selector=args.auth_email_selector,
            password_selector=args.auth_password_selector,
            submit_selector=args.auth_submit_selector,
        )

    # Build screenshot config
    screenshot_config = ScreenshotConfig(
        enabled=args.screenshot,
        output_directory=args.screenshot_dir,
        capture_on_error=args.screenshot_on_error or args.screenshot,
        capture_on_success=args.screenshot and not args.screenshot_on_error,
        full_page=args.full_page,
    )

    # Determine viewport(s)
    viewport_presets = {
        "desktop": ViewportConfig.desktop(),
        "desktop_small": ViewportConfig.desktop_small(),
        "mobile": ViewportConfig.mobile(),
        "mobile_small": ViewportConfig.mobile_small(),
        "tablet": ViewportConfig.tablet(),
        "ipad_pro": ViewportConfig.ipad_pro(),
        "android_pixel": ViewportConfig.android_pixel(),
        "android_samsung": ViewportConfig.android_samsung(),
        "android_tablet": ViewportConfig.android_tablet(),
    }

    # Handle custom viewport
    if args.viewport_width and args.viewport_height:
        default_viewport = ViewportConfig(
            name="custom",
            width=args.viewport_width,
            height=args.viewport_height
        )
    elif args.viewport in viewport_presets:
        default_viewport = viewport_presets[args.viewport]
    else:
        default_viewport = ViewportConfig.desktop()

    # Run validation
    print(f"[INFO] Validating {args.url}...")
    print(
        f"[INFO] Using {'Selenium' if SELENIUM_AVAILABLE else 'Playwright' if PLAYWRIGHT_AVAILABLE else 'basic HTTP'} validation"
    )
    print(f"[INFO] Viewport: {default_viewport.name} ({default_viewport.width}x{default_viewport.height})")
    if auth_config:
        print(f"[INFO] Authentication: {auth_config.login_url}")
    if screenshot_config.enabled:
        print(f"[INFO] Screenshots: {screenshot_config.output_directory}")
    print()

    with WebPageValidator(
        headless=not args.no_headless,
        timeout=args.timeout,
        auth_config=auth_config,
        screenshot_config=screenshot_config,
        default_viewport=default_viewport
    ) as validator:
        # Authenticate if needed
        if auth_config:
            validator.authenticate()

        # Handle "all" viewport option
        if args.viewport == "all":
            results = validator.validate_all_viewports(args.url)
            # Combine results into summary
            all_success = all(r.success for r in results)
            all_errors = []
            all_screenshots = []
            for r in results:
                all_errors.extend(r.console_errors)
                all_screenshots.extend(r.screenshots)
            # Use first result as base
            result = results[0] if results else validator.validate_url(args.url)
            result.console_errors = all_errors
            result.screenshots = all_screenshots
            result.success = all_success
            result.error_summary = f"Tested {len(results)} viewports, {sum(1 for r in results if r.success)} passed"
        else:
            result = validator.validate_url(args.url, wait_for_load=args.wait)

    # Output results
    if args.json:
        output = json.dumps(result.to_dict(), indent=2)
    else:
        output = format_validation_report(result, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[OK] Report saved to {args.output}")
    else:
        print(output)

    # Print screenshot info if any
    if result.screenshots:
        print("\n[INFO] Screenshots captured:")
        for ss in result.screenshots:
            if ss.success:
                print(f"  - {ss.file_path}")

    # Exit with error code if validation failed
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
