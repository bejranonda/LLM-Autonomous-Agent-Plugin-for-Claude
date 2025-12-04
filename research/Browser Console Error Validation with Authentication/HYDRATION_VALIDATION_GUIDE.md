# Hydration & Console Error Validation Guide

**Version:** 1.0
**Date:** December 2, 2025
**Purpose:** Reusable methodology for debugging React hydration mismatches and console errors in Next.js applications

## Overview

This guide provides a comprehensive methodology for validating React hydration behavior and capturing detailed console errors in Next.js applications. It's designed to be reusable across multiple projects and environments.

### What This Solves

- ✅ React Error #185 (hydration mismatch) debugging
- ✅ Console error capture with full details (line numbers, stack traces)
- ✅ Error boundary detection and reporting
- ✅ Network error correlation
- ✅ Multi-page validation across public and protected routes
- ✅ Authentication flow validation

---

## Quick Start

### 1. Run Basic Validation

```bash
# Public pages only
node scripts/validate-basic.js

# With authentication
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPass123!' \
  node scripts/validate-with-auth.js
```

### 2. Run Detailed Error Capture

```bash
# Captures full stack traces and error details
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPass123!' \
  node scripts/validate-with-auth-detailed.js
```

### 3. Check Reports

```bash
# Basic report
cat console-errors-report.json | jq .

# Detailed report with full error information
cat console-errors-detailed-report.json | jq .
```

---

## Methodology: 5-Step Error Capture Process

### Step 1: Browser Setup
- Launch Chromium/Chrome in headless mode
- Set viewport to standard size (1280x720)
- Configure navigation timeout (30 seconds)

### Step 2: Error Interception
Capture errors from multiple sources:
- **Console errors** - `console.error()` calls
- **Uncaught exceptions** - JavaScript errors
- **Network errors** - Failed HTTP requests
- **Page evaluation** - JavaScript executed in page context

### Step 3: Navigation & Hydration
1. Navigate to page
2. Wait for `networkidle2` (network activity settles)
3. Wait additional 3000ms for React hydration
4. Capture all errors that occurred during this period

### Step 4: Error Boundary Detection
- Check if error boundary is displayed ("Something went wrong")
- Indicates an error was caught and the page failed to render
- This is the key symptom of hydration failures

### Step 5: Report Generation
Generate JSON report with:
- Error type (console, exception, network, etc.)
- Error message and stack trace
- Page name and URL
- Timestamp
- Loadable scripts count

---

## Error Types Explained

### Type: `console.error`
**What:** Error logged via `console.error()`
**Cause:** Intentionally thrown/logged errors
**Example:** `JSHandle@error` (React error)
**Action:** Check full error message and stack trace

### Type: `uncaught.exception`
**What:** JavaScript exception not caught by error handler
**Cause:** Runtime errors (ReferenceError, TypeError, etc.)
**Example:** `Cannot read property 'x' of undefined`
**Action:** Fix the underlying JavaScript issue

### Type: `page.evaluation`
**What:** Result of JavaScript code executed in page context
**Cause:** Custom error detection in the page
**Example:** Detect if error boundary is visible
**Action:** Check error boundary output or error details array

### Type: `network.error`
**What:** Failed HTTP request (4xx or 5xx)
**Cause:** API failure, missing resource
**Example:** `GET /api/projects → 401 Unauthorized`
**Action:** Fix API endpoint or authentication

### Type: `http.error`
**What:** Page response status code >= 400
**Cause:** Server returned error status
**Example:** 500 Internal Server Error
**Action:** Check server logs

### Type: `navigation.error`
**What:** Error during page navigation
**Cause:** Navigation failed, page didn't load
**Example:** `ERR_CONNECTION_REFUSED`
**Action:** Check server is running, URL is correct

---

## Key Indicators of Hydration Mismatch

### Red Flags

1. **Error Boundary Visible**
   - Text: "Something went wrong"
   - Cause: React caught an error during hydration
   - Action: Check console for React #185

2. **JSHandle@error in console**
   - Reason: Puppeteer can't serialize Error object
   - Means: A JavaScript Error was thrown
   - Action: Use detailed script to get full error

3. **Different Scripts Loaded**
   - Compare script counts between server render and client
   - Cause: Dynamic imports or conditional loading

4. **Loaded Scripts Count Changes**
   - Example: Home page has 14 scripts, Auth pages have 26
   - Indicates: Different code is being loaded per route

### Success Indicators

- No error boundary visible
- No console.error messages
- HTTP response status 200
- Consistent script loading count per route

---

## Configuration Guide

### Environment Variables

```bash
# Required
BASE_URL=http://localhost:3000        # Server URL to test

# Optional
CHROMIUM_PATH=/usr/bin/chromium-browser  # Path to Chromium binary
TEST_EMAIL=test@example.com             # Email for login (if needed)
TEST_PASSWORD=TestPassword123!          # Password for login (if needed)
```

### Script Configuration

Edit the `CONFIG` object in validation scripts:

```javascript
const CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  chromiumPath: process.env.CHROMIUM_PATH || '/usr/bin/chromium-browser',
  navigationTimeout: 30000,      // Max time to wait for page load
  hydrationWait: 3000,           // Time to wait for React hydration
  loginEmail: 'test@example.com',
  loginPassword: 'TestPass123!',
};
```

### Timeout Adjustment

- **Slow networks:** Increase `navigationTimeout` to 45000-60000ms
- **Fast machines:** Can decrease to 15000ms
- **Hydration:** 3000ms usually sufficient, increase if app is slow

---

## Available Scripts

### 1. `validate-basic.js` (Not provided, but concept)
- Tests public pages only
- No authentication required
- Fast, lightweight

### 2. `validate-with-auth.js` (Original)
- Tests public AND protected pages
- Requires login credentials
- Simple error reporting

### 3. `validate-with-auth-detailed.js` (Enhanced)
- Full error capture with stack traces
- Error boundary detection
- Network error tracking
- Detailed JSON report
- **Recommended for debugging**

---

## Interpreting Results

### Success Case
```json
{
  "testsPassed": 6,
  "testsFailed": 0,
  "errorDetails": []
}
```
✅ All pages loaded without errors

### Failure Case
```json
{
  "testsPassed": 5,
  "testsFailed": 1,
  "errorDetails": [
    {
      "type": "console.error",
      "message": "React error #185",
      "page": "/app",
      "pageName": "App"
    },
    {
      "type": "page.evaluation",
      "details": [
        {
          "source": "Error Boundary",
          "visible": true,
          "text": "Something went wrong..."
        }
      ]
    }
  ]
}
```

**Analysis:**
- App page failed (/app)
- React error #185 (hydration mismatch)
- Error boundary is visible (error was caught)
- Other 5 pages passed (public pages OK, other protected pages OK)

---

## Debugging Workflow

### Step 1: Run Detailed Validation
```bash
npm run validate:detailed
```

### Step 2: Check Error Report
```bash
cat console-errors-detailed-report.json | jq '.errorDetails[] | select(.pageName == "App")'
```

### Step 3: Identify Error Pattern
- **All pages failed?** → Check server/auth setup
- **Only /app failed?** → Hydration issue specific to that page
- **Only certain auth pages failed?** → Auth state mismatch

### Step 4: Fix Based on Type
| Error Type | Fix Strategy |
|------------|--------------|
| console.error | Check error message, debug specific component |
| page.evaluation + Error Boundary | React error, check hydration boundary implementation |
| network.error | Check API endpoint, auth token, CORS |
| http.error | Check server response, database connection |

### Step 5: Re-validate
```bash
npm run validate:detailed
```

---

## Common Issues & Solutions

### Issue: "Something went wrong" (Error Boundary Visible)

**Cause:** React caught an error during hydration
**Solution:**

1. Check if `/app` page uses hydration-sensitive state
2. Look for `useSession()` calls during render
3. Check for Zustand store access before hydration complete
4. Implement HydrationBoundary:
   ```typescript
   <HydrationBoundary>
     <ProtectedRoute>
       {/* Page content */}
     </ProtectedRoute>
   </HydrationBoundary>
   ```

### Issue: Network Errors on API Calls

**Cause:** Auth token missing, API not available, CORS issues
**Solution:**

1. Verify API endpoint is responding: `curl -I http://localhost:3000/api/health`
2. Check auth token is being sent in headers
3. Verify server is running: `pm2 status`

### Issue: Timeouts During Navigation

**Cause:** Page takes too long to load, server is slow
**Solution:**

1. Increase `navigationTimeout`: `navigationTimeout: 60000`
2. Check server performance: `pm2 logs`
3. Check network: `npm run dev 2>&1 | grep -E "compiled|error"`

### Issue: Login Not Working in Tests

**Cause:** Wrong credentials, form selectors changed
**Solution:**

1. Verify credentials work manually
2. Check form input selectors: `input[type="email"]`, `input[type="password"]`
3. Add delays between form actions (already included)

---

## Extension Guide

### Adding Custom Validations

```javascript
// In validate-with-auth-detailed.js, add to captureDetailedErrors():

// Custom check: Look for specific error text
const hasHydrationError = await page.evaluate(() => {
  const bodyText = document.body.innerText;
  return bodyText.includes('Minified React error #185');
});

if (hasHydrationError) {
  collectedErrors.push({
    type: 'react.hydration',
    message: 'React Error #185 detected',
    severity: 'critical',
  });
}
```

### Adding New Pages

```javascript
// In main() function, add more test pages:

console.log('\n📊 Additional Pages:');
await captureDetailedErrors(page, `${CONFIG.baseUrl}/projects`, 'Projects');
await captureDetailedErrors(page, `${CONFIG.baseUrl}/blog`, 'Blog');
await captureDetailedErrors(page, `${CONFIG.baseUrl}/docs`, 'Documentation');
```

### Custom Report Format

```javascript
// After captureDetailedErrors(), format report differently:

const errorsByType = results.errorDetails.reduce((acc, err) => {
  if (!acc[err.type]) acc[err.type] = [];
  acc[err.type].push(err);
  return acc;
}, {});

console.log('\n📊 Errors by Type:');
Object.entries(errorsByType).forEach(([type, errors]) => {
  console.log(`${type}: ${errors.length} error(s)`);
});
```

---

## Performance Tips

### Speed Up Validation

```bash
# Reduce hydration wait time for faster machines
HYDRATION_WAIT=1000 node scripts/validate-with-auth-detailed.js

# Skip certain pages
# (modify script to skip non-critical pages)
```

### Reduce Browser Overhead

```javascript
// In browser launch options:
args: [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-web-resources',      // Skip loading web resources
  '--disable-dev-shm-usage',      // Reduce memory usage
  '--disable-gpu',                // No GPU needed for headless
],
```

---

## Troubleshooting

### Chromium Not Found

```bash
# Check path
which chromium-browser
# or
which chrome
# or
which chromium

# Then set CHROMIUM_PATH
export CHROMIUM_PATH=/path/to/chromium
```

### Port Already in Use

```bash
# Kill existing process
lsof -i :3000
kill -9 <PID>

# Or use different port
BASE_URL=http://localhost:3001 node scripts/validate-with-auth-detailed.js
```

### Report Not Generated

```bash
# Check file permissions
ls -la console-errors-detailed-report.json

# Check working directory
pwd

# Run with explicit path
node /full/path/to/script.js
```

---

## Best Practices

1. **Run validation before deploying**
   ```bash
   npm run build && npm run validate:detailed
   ```

2. **Keep reports for comparison**
   ```bash
   cp console-errors-detailed-report.json reports/$(date +%Y%m%d_%H%M%S).json
   ```

3. **Set up in CI/CD**
   ```yaml
   - name: Validate hydration
     run: npm run validate:detailed
     if: always()  # Run even if tests fail
   ```

4. **Monitor error trends**
   - Track errors over time
   - Look for new error types
   - Alert on error count increase

5. **Document all errors**
   - Keep error reports in git
   - Link to GitHub issues
   - Update solutions as you find them

---

## References

- [React Error #185 Documentation](https://react.dev/errors/185)
- [Next.js Hydration Documentation](https://nextjs.org/docs/messages/react-hydration-error)
- [Puppeteer API Reference](https://pptr.dev/)
- [Chromium Headless Mode](https://developer.chrome.com/articles/new-headless/)

---

## Support & Questions

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review error details in `console-errors-detailed-report.json`
3. Check server logs: `pm2 logs`
4. Compare with successful validation runs

---

**Last Updated:** December 2, 2025
**Maintainer:** Development Team
