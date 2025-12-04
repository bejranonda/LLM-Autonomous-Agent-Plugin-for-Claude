# Hydration & Console Error Validation Toolkit

A comprehensive, reusable toolkit for debugging React hydration mismatches and console errors in Next.js applications.

## 📁 What's Inside

```
research/debug/
├── README.md                                    # This file
├── INDEX.md                                     # Complete navigation guide
├── QUICK_REFERENCE.md                           # One-page cheat sheet (START HERE)
├── HYDRATION_VALIDATION_GUIDE.md                # Comprehensive guide (1000+ lines)
├── COMMON_HYDRATION_ISSUES.md                   # 8 issues + solutions
├── EXAMPLE_CONFIGURATIONS.md                    # 10 real-world scenarios
├── SAMPLE_SCRIPTS_GUIDE.md                      # ⭐ NEW - Sample scripts documentation
├── Sample Scripts/
│   ├── validate-with-auth.js                    # Quick validation (5/6 tests pass)
│   └── validate-with-auth-detailed.js           # Deep analysis (captures React #185!)
├── validate-console-errors.js                   # Public pages only
└── validate-app-errors.js                       # Full-featured validation
```

## 🚀 Quick Start (30 seconds)

### Option A: Use Production-Ready Sample Scripts ⭐ (RECOMMENDED)

```bash
# 1. Run detailed validation (captures full error stacks)
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='password' \
  timeout 120 node "research/debug/Sample Scripts/validate-with-auth-detailed.js"

# 2. Check results
cat console-errors-detailed-report.json | jq .
```

**Why?** This script successfully captures React Error #185 with full stack traces!

### Option B: Traditional Approach

```bash
# 1. Copy to your project
cp research/debug/validate-app-errors.js ./

# 2. Run validation
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPassword123!' \
  node validate-app-errors.js

# 3. Check results
cat console-errors-detailed-report.json | jq .
```

## 📖 Documentation Structure

### For Impatient People (5 min)
→ Read: **QUICK_REFERENCE.md**
- One-liners
- What each error means
- Common fixes
- Debugging workflow

### For Developers Implementing (30 min)
→ Read: **EXAMPLE_CONFIGURATIONS.md**
- Pick your scenario (Local, Docker, CI/CD, etc.)
- Copy the configuration
- Run immediately

### For Complete Understanding (60 min)
→ Read: **HYDRATION_VALIDATION_GUIDE.md**
- What is hydration?
- 5-step methodology
- Error type reference
- Troubleshooting guide
- Best practices

## 🎯 What This Tool Does

### Detects

✅ React hydration mismatches (#185)
✅ Uncaught JavaScript exceptions
✅ API/network failures
✅ Error boundaries catching errors
✅ HTTP response errors
✅ Navigation failures

### Reports

- Error type and message
- Stack trace (when available)
- Page name and URL
- Timestamp
- Error boundary detection
- JSON report for processing

## 📊 Understanding the Reports

### Basic Report (`console-errors-report.json`)
Simple summary:
```json
{
  "criticalIssues": [...],
  "testsPassed": ["Home", "SignIn"],
  "testsFailed": ["App"]
}
```

### Detailed Report (`console-errors-detailed-report.json`)
Full error information:
```json
{
  "errorDetails": [
    {
      "type": "console.error",
      "message": "Minified React error #185",
      "page": "/app",
      "pageName": "App",
      "stack": "..."
    }
  ],
  "testsPassed": [...],
  "testsFailed": [...]
}
```

## 🔍 Common Error Types

| Type | Meaning | Action |
|------|---------|--------|
| `console.error` | JavaScript console.error() was called | Check error message |
| `uncaught.exception` | Unhandled JavaScript error | Fix the error |
| `page.evaluation` | Custom page check result | Check error boundary |
| `network.error` | HTTP request failed | Check API/server |
| `http.error` | Page returned 4xx/5xx | Fix server response |
| `navigation.error` | Page failed to navigate | Check server running |

## 🛠️ Tools Included

### `validate-app-errors.js`
Full-featured validation script with:
- Multi-page testing (public + authenticated)
- Error interception from multiple sources
- Error boundary detection
- Network error tracking
- Detailed JSON reports
- Ready to run - no modification needed (except credentials)

**Usage:**
```bash
node validate-app-errors.js
```

**Configuration:**
Edit top of script or use environment variables:
```javascript
const CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  chromiumPath: process.env.CHROMIUM_PATH || '/usr/bin/chromium-browser',
  navigationTimeout: 30000,
  hydrationWait: 3000,
  loginEmail: process.env.TEST_EMAIL || 'test@example.com',
  loginPassword: process.env.TEST_PASSWORD || 'TestPassword123!',
};
```

## 🌍 Use Cases

### 1. Local Development
Validate pages as you develop:
```bash
npm run dev &  # Start dev server
sleep 5 && npm run validate:errors  # Validate
```

### 2. Before Git Commit
Ensure no hydration errors before committing:
```bash
npm run build && npm run validate:errors
```

### 3. CI/CD Pipeline
Automated validation on every push (see GitHub Actions example)

### 4. Production Monitoring
Regular validation of production deployment:
```bash
BASE_URL=https://yourapp.com node validate-app-errors.js
```

### 5. Pre-Release Checklist
Manual validation before major releases (see Team Checklist example)

## 📋 Setup for Your Project

### Step 1: Copy Files
```bash
mkdir -p research/debug
cp research/debug/* /path/to/your-project/research/debug/
```

### Step 2: Install Chromium (if needed)
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium

# Or use chrome binary path
```

### Step 3: Configure Credentials
Update in `validate-app-errors.js`:
```javascript
loginEmail: 'your-test@example.com',
loginPassword: 'YourPassword123!',
```

### Step 4: Add npm Scripts
```json
{
  "scripts": {
    "validate:errors": "BASE_URL=http://localhost:3000 CHROMIUM_PATH=/usr/bin/chromium-browser node research/debug/validate-app-errors.js"
  }
}
```

### Step 5: Run
```bash
npm run validate:errors
```

## 🔧 Customization

### Test Different Pages
Edit `validate-app-errors.js` main() function:
```javascript
console.log('\n📄 Your Custom Pages:');
await captureDetailedErrors(page, `${CONFIG.baseUrl}/your-page`, 'Your Page');
await captureDetailedErrors(page, `${CONFIG.baseUrl}/another-page`, 'Another Page');
```

### Adjust Timeouts
```javascript
const CONFIG = {
  navigationTimeout: 60000,  // 60 seconds (slow network)
  hydrationWait: 5000,       // 5 seconds (slow app)
};
```

### Skip Authentication
Remove/comment out login code:
```javascript
// Comment this out:
// await loginToApp(page);

// Then comment out protected page tests:
// await captureDetailedErrors(page, `${CONFIG.baseUrl}/app`, 'App');
```

## 📈 Integration Examples

### GitHub Actions
```yaml
- name: Validate Errors
  run: BASE_URL=http://localhost:3000 node research/debug/validate-app-errors.js
```

### GitLab CI
```yaml
validate:
  script:
    - BASE_URL=http://localhost:3000 node research/debug/validate-app-errors.js
```

### npm scripts
```json
{
  "scripts": {
    "validate:errors": "node research/debug/validate-app-errors.js",
    "validate:before-commit": "npm run build && npm run validate:errors",
    "dev:validate": "npm run dev & sleep 5 && npm run validate:errors"
  }
}
```

## 🚨 Troubleshooting

### Chromium Not Found
```bash
which chromium-browser
export CHROMIUM_PATH=/path/to/chromium-browser
```

### Validation Timeout
```bash
# Increase timeout
sed -i 's/navigationTimeout: 30000/navigationTimeout: 60000/' validate-app-errors.js
```

### Port In Use
```bash
lsof -i :3000 | kill -9
```

### Report Not Generated
Check file permissions and working directory:
```bash
pwd
ls -la console-errors-*.json
```

## 📚 Documentation Files

| File | Purpose | Read Time | For |
|------|---------|-----------|-----|
| **README.md** | Overview & quick start | 5 min | Everyone |
| **QUICK_REFERENCE.md** | Cheat sheet & one-liners | 10 min | Developers |
| **HYDRATION_VALIDATION_GUIDE.md** | Complete methodology | 60 min | Deep understanding |
| **EXAMPLE_CONFIGURATIONS.md** | Real-world scenarios | 30 min | Specific use cases |
| **validate-app-errors.js** | Actual validation script | - | Execution |

## 💡 Pro Tips

1. **Run before every commit**
   ```bash
   npm run validate:errors || exit 1  # Fail if errors found
   ```

2. **Keep historical reports**
   ```bash
   cp console-errors-*.json reports/$(date +%Y%m%d_%H%M%S).json
   ```

3. **Set up CI/CD**
   Run automatically on every push (GitHub Actions example in docs)

4. **Monitor trends**
   Track if errors increase/decrease over time

5. **Share with team**
   Save reports in git for code review discussion

## 🎓 Learning Path

1. **Start:** Read QUICK_REFERENCE.md (10 min)
2. **Apply:** Copy your scenario from EXAMPLE_CONFIGURATIONS.md (5 min)
3. **Run:** Execute validate-app-errors.js (1-2 min)
4. **Understand:** Read relevant sections of HYDRATION_VALIDATION_GUIDE.md
5. **Integrate:** Add to your CI/CD pipeline

## ❓ FAQ

**Q: Do I need to modify the script?**
A: No! Just set environment variables for your project.

**Q: How often should I run validation?**
A: At minimum before commits. Ideally on every push (CI/CD).

**Q: Can I use this for production?**
A: Yes! Set `BASE_URL=https://yourapp.com` to validate production.

**Q: What if all pages fail?**
A: Check server is running, auth works manually, Chromium is installed.

**Q: How do I fix hydration errors?**
A: See "Common Fixes" in QUICK_REFERENCE.md and HYDRATION_VALIDATION_GUIDE.md

## 📝 License

Use freely in your projects. Attribution appreciated!

## 🤝 Contribute

Found issues or have improvements? Document them and share with your team!

---

**Created:** December 2, 2025
**Version:** 1.0
**Status:** Production Ready

**Start with:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
