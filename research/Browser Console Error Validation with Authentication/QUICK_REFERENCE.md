# Hydration Error Validation - Quick Reference

## One-Liner Validation

```bash
# Clone this and update BASE_URL, CHROMIUM_PATH, credentials
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPass123!' \
  node validate-app-errors.js
```

## What to Look For

| Indicator | Meaning | Action |
|-----------|---------|--------|
| `✅ PASSED` | Page loaded without errors | Page is healthy |
| `❌ FAILED` | Error detected during page load | Debug using error report |
| `JSHandle@error` | React threw an Error (can't see details) | Check browser DevTools |
| `Error Boundary` visible | React crashed, error boundary caught it | Check hydration setup |
| `console.error` | JavaScript error in console | Check stack trace |
| `network.error` | API call failed | Check server, auth, CORS |

## Understanding Error Details

### React Hydration Error (#185)
```json
{
  "type": "console.error",
  "message": "Minified React error #185",
  "pageName": "App"
}
```
**Meaning:** Server-rendered HTML doesn't match what React expects
**Fix:** Add HydrationBoundary, fix useSession timing, check store hydration

### Error Boundary Visible
```json
{
  "type": "page.evaluation",
  "details": [{
    "source": "Error Boundary",
    "visible": true,
    "text": "Something went wrong..."
  }]
}
```
**Meaning:** Page crashed, error boundary caught it
**Fix:** Check which component threw the error, add error logging

### Network Error
```json
{
  "type": "network.error",
  "message": "GET /api/projects",
  "error": "ERR_FAILED"
}
```
**Meaning:** API endpoint failed
**Fix:** Check server is running, auth token is sent, endpoint exists

## Report Files

After running validation:

- **console-errors-detailed-report.json** - Full error details with stack traces
- **console-errors-report.json** - Simple summary (if using basic script)

View with:
```bash
cat console-errors-detailed-report.json | jq .
```

## Common Fixes

### React #185 (Hydration Mismatch)
```typescript
// Wrap page content with HydrationBoundary
<HydrationBoundary>
  <ProtectedRoute>
    {/* page content */}
  </ProtectedRoute>
</HydrationBoundary>
```

### useSession() Timing
```typescript
// Don't use session data during render
// Use inside useEffect or after hydration boundary
const { status } = useSession();

useEffect(() => {
  if (status === 'authenticated') {
    // Now safe to use session data
  }
}, [status]);
```

### Zustand Store Hydration
```typescript
// Add skipHydration: true to persist middleware
persist(
  (set, get) => ({ /* store */ }),
  {
    skipHydration: true  // ← Add this
  }
)
```

## Debugging Workflow

1. **Run validation**
   ```bash
   BASE_URL=... node validate-app-errors.js
   ```

2. **Check report**
   ```bash
   cat console-errors-detailed-report.json | jq '.errorDetails[] | select(.pageName == "App")'
   ```

3. **Identify error type**
   - `console.error` → Check React error message
   - `page.evaluation` → Check error boundary output
   - `network.error` → Check server/API

4. **Apply fix** (see Common Fixes above)

5. **Re-validate**
   ```bash
   BASE_URL=... node validate-app-errors.js
   ```

## Setup for New Project

```bash
# 1. Copy files to new project
cp HYDRATION_VALIDATION_GUIDE.md /new-project/research/debug/
cp validate-app-errors.js /new-project/research/debug/

# 2. Update credentials in validate-app-errors.js
# Edit: CONFIG.loginEmail, CONFIG.loginPassword

# 3. Create npm script in package.json
"scripts": {
  "validate:errors": "node research/debug/validate-app-errors.js"
}

# 4. Set environment variables
export BASE_URL=http://localhost:3000
export CHROMIUM_PATH=/usr/bin/chromium-browser

# 5. Run validation
npm run validate:errors
```

## Interpreting JSON Report

**errorDetails array:**
- Each object = 1 error detected
- `type` = error category
- `message` = error message
- `page`/`pageName` = which page had the error
- `stack` (if present) = JavaScript stack trace
- `details` (if present) = additional error info

**testsPassed array:**
- List of pages that loaded without errors

**testsFailed array:**
- List of pages that had errors

## CI/CD Integration

### GitHub Actions
```yaml
- name: Validate React Hydration
  run: |
    npm run build
    BASE_URL=http://localhost:3000 \
      npm run validate:errors
  if: always()  # Run even if tests fail

- name: Upload Error Report
  uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: hydration-error-report
    path: console-errors-detailed-report.json
```

### GitLab CI
```yaml
validate_hydration:
  script:
    - npm run build
    - BASE_URL=http://localhost:3000 npm run validate:errors
  artifacts:
    paths:
      - console-errors-detailed-report.json
    when: always
```

## Tips & Tricks

### Faster Validation
```bash
# Reduce hydration wait time
sed -i 's/hydrationWait: 3000/hydrationWait: 1000/' validate-app-errors.js
```

### Skip Auth Pages
```bash
# Edit script to comment out protected page tests
# Remove: await captureDetailedErrors(page, `${CONFIG.baseUrl}/app`, 'App');
```

### Validate Production
```bash
BASE_URL=https://yourapp.com \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  node validate-app-errors.js
```

### Parse Just Failures
```bash
cat console-errors-detailed-report.json | \
  jq '.errorDetails[] | select(.type == "console.error")'
```

---

**For detailed information, see HYDRATION_VALIDATION_GUIDE.md**
