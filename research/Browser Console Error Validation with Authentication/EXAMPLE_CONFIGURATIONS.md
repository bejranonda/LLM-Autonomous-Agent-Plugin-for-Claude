# Example Configurations for Different Scenarios

## Scenario 1: Local Development

### Setup
```bash
# Start your dev server
npm run dev

# In another terminal, run validation
BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPassword123!' \
  node research/debug/validate-app-errors.js
```

### Expected Output
```
✅ Most pages should PASS
❌ Pages with hydration issues should FAIL

Example: App page shows "Something went wrong" error boundary
```

### Config in package.json
```json
{
  "scripts": {
    "validate:dev": "BASE_URL=http://localhost:3000 CHROMIUM_PATH=/usr/bin/chromium-browser TEST_EMAIL='test@example.com' TEST_PASSWORD='TestPassword123!' node research/debug/validate-app-errors.js",
    "dev": "next dev",
    "dev:validate": "npm run dev & sleep 5 && npm run validate:dev"
  }
}
```

---

## Scenario 2: Production Server (VPS/Cloud)

### Setup
```bash
# SSH into server
ssh user@your-server.com

# Run validation against production
BASE_URL=https://yourapp.com \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPassword123!' \
  node research/debug/validate-app-errors.js

# Save report for later review
cp console-errors-detailed-report.json reports/prod-$(date +%Y%m%d_%H%M%S).json
```

### Config for Deployment
```bash
# .env.production
BASE_URL=https://yourapp.com
CHROMIUM_PATH=/usr/bin/chromium-browser

# Run validation as part of deployment
./scripts/post-deploy.sh:
#!/bin/bash
BASE_URL=${PRODUCTION_URL} \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  node research/debug/validate-app-errors.js

if [ $? -ne 0 ]; then
  echo "Validation failed! Rolling back..."
  git revert HEAD
  exit 1
fi
```

---

## Scenario 3: Docker Environment

### Dockerfile
```dockerfile
FROM node:18-alpine

RUN apk add --no-cache \
  chromium \
  chromium-libs

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Run validation
CMD ["node", "research/debug/validate-app-errors.js"]
```

### docker-compose.yml
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      BASE_URL: http://localhost:3000
      CHROMIUM_PATH: /usr/bin/chromium

  validate:
    build: .
    environment:
      BASE_URL: http://app:3000
      CHROMIUM_PATH: /usr/bin/chromium
      TEST_EMAIL: test@example.com
      TEST_PASSWORD: TestPassword123!
    depends_on:
      - app
```

### Run
```bash
docker-compose up --abort-on-container-exit
```

---

## Scenario 4: GitHub Actions CI/CD

### .github/workflows/validate.yml
```yaml
name: Validate Hydration & Errors

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Start server
        run: npm run start &
        env:
          NODE_ENV: production

      - name: Wait for server
        run: |
          timeout 30 bash -c 'until curl -f http://localhost:3000; do sleep 1; done'

      - name: Install Chromium
        run: |
          apt-get update
          apt-get install -y chromium-browser

      - name: Validate hydration & errors
        run: |
          BASE_URL=http://localhost:3000 \
            CHROMIUM_PATH=/usr/bin/chromium-browser \
            TEST_EMAIL='test@example.com' \
            TEST_PASSWORD='TestPassword123!' \
            node research/debug/validate-app-errors.js
        env:
          CI: true

      - name: Upload error report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: hydration-report
          path: console-errors-detailed-report.json

      - name: Comment on PR
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('console-errors-detailed-report.json', 'utf8'));
            const errors = report.errorDetails.length;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `❌ Hydration validation failed: ${errors} error(s) detected\n\nSee attached report for details.`
            });
```

### Usage
Push to your repository, actions run automatically

---

## Scenario 5: Manual Testing in Teams

### Setup Document
Save as `VALIDATION_CHECKLIST.md`:

```markdown
# Pre-Release Validation Checklist

## Before Release
- [ ] Run local validation: `npm run validate:dev`
- [ ] Check report: `cat console-errors-detailed-report.json | jq .`
- [ ] All pages should show PASSED
- [ ] No "Something went wrong" error boundaries

## Steps
1. Start dev server: `npm run dev`
2. Wait for "ready on..." message
3. Open new terminal
4. Run: `npm run validate:dev`
5. Wait for report (usually 1-2 minutes)
6. Check console-errors-detailed-report.json
7. If FAILED, click links in report to test pages manually
8. Fix issues and re-run validation

## Troubleshooting
- Chromium not found? Install: `apt-get install chromium-browser`
- Port in use? Kill: `lsof -i :3000 | kill -9`
- Validation timeout? Increase navigationTimeout to 60000
```

---

## Scenario 6: Monitoring Over Time

### Setup
```bash
#!/bin/bash
# scripts/continuous-validation.sh

INTERVAL=3600  # Run every hour
REPORT_DIR=reports/validation

mkdir -p $REPORT_DIR

while true; do
  echo "Running validation at $(date)..."

  BASE_URL=http://localhost:3000 \
    CHROMIUM_PATH=/usr/bin/chromium-browser \
    node research/debug/validate-app-errors.js

  # Save timestamped report
  cp console-errors-detailed-report.json \
    $REPORT_DIR/$(date +%Y%m%d_%H%M%S).json

  # Keep only last 100 reports
  ls -1t $REPORT_DIR/*.json | tail -n +101 | xargs rm -f

  # Wait for next run
  sleep $INTERVAL
done
```

### Run
```bash
# Start background monitoring
./scripts/continuous-validation.sh &

# Check reports
ls -lht reports/validation/ | head -10
```

---

## Scenario 7: Cross-Browser Testing

### Multiple Browsers
```bash
#!/bin/bash
# scripts/validate-all-browsers.sh

BROWSERS=(/usr/bin/chromium-browser /usr/bin/google-chrome /usr/bin/firefox)

for browser in "${BROWSERS[@]}"; do
  if [ -f "$browser" ]; then
    echo "Testing with: $browser"

    BASE_URL=http://localhost:3000 \
      CHROMIUM_PATH=$browser \
      node research/debug/validate-app-errors.js

    # Save browser-specific report
    cp console-errors-detailed-report.json \
      console-errors-$(basename $browser).json
  fi
done
```

---

## Scenario 8: Integration with Test Suite

### In Jest/Vitest
```javascript
// tests/hydration.test.ts
import { execSync } from 'child_process';
import * as fs from 'fs';

describe('Hydration Validation', () => {
  it('should have no console errors', () => {
    try {
      execSync(
        'node research/debug/validate-app-errors.js',
        {
          env: {
            ...process.env,
            BASE_URL: 'http://localhost:3000',
            CHROMIUM_PATH: '/usr/bin/chromium-browser',
          },
          stdio: 'inherit'
        }
      );
    } catch (error) {
      const report = JSON.parse(
        fs.readFileSync('console-errors-detailed-report.json', 'utf8')
      );
      throw new Error(`Hydration validation failed: ${JSON.stringify(report.errorDetails)}`);
    }
  });
});
```

---

## Scenario 9: Slack Notifications

### Setup
```bash
#!/bin/bash
# scripts/validate-and-notify.sh

BASE_URL=http://localhost:3000 \
  CHROMIUM_PATH=/usr/bin/chromium-browser \
  TEST_EMAIL='test@example.com' \
  TEST_PASSWORD='TestPassword123!' \
  node research/debug/validate-app-errors.js

# Check result
REPORT=$(cat console-errors-detailed-report.json)
ERROR_COUNT=$(echo $REPORT | jq '.errorDetails | length')

if [ $ERROR_COUNT -gt 0 ]; then
  # Send Slack notification
  curl -X POST $SLACK_WEBHOOK_URL \
    -H 'Content-type: application/json' \
    -d "{
      \"text\": \"⚠️  Hydration Validation Failed\",
      \"blocks\": [
        {
          \"type\": \"section\",
          \"text\": {
            \"type\": \"mrkdwn\",
            \"text\": \"*Hydration Validation Failed*\n\`\`\`$REPORT\`\`\`\"
          }
        }
      ]
    }"
fi
```

### Add to package.json
```json
{
  "scripts": {
    "validate:notify": "bash scripts/validate-and-notify.sh"
  }
}
```

---

## Scenario 10: Custom Error Analysis

### Analysis Script
```javascript
// scripts/analyze-errors.js
const fs = require('fs');

const report = JSON.parse(
  fs.readFileSync('console-errors-detailed-report.json', 'utf8')
);

// Group by error type
const byType = {};
report.errorDetails.forEach(err => {
  byType[err.type] = (byType[err.type] || 0) + 1;
});

// Group by page
const byPage = {};
report.errorDetails.forEach(err => {
  byPage[err.pageName] = (byPage[err.pageName] || 0) + 1;
});

console.log('Errors by Type:', byType);
console.log('Errors by Page:', byPage);
console.log('Failed Pages:', report.testsFailed);
console.log('Passed Pages:', report.testsPassed);
```

### Run
```bash
node scripts/analyze-errors.js
```

---

## Choose Your Scenario

| Scenario | Use Case | Priority |
|----------|----------|----------|
| Local Development | Day-to-day coding | 🔴 High |
| Production Server | Deploy to VPS/Cloud | 🔴 High |
| Docker | Container deployments | 🟡 Medium |
| GitHub Actions | Automated CI/CD | 🔴 High |
| Team Checklist | Before releases | 🔴 High |
| Monitoring Over Time | Catch regressions | 🟡 Medium |
| Cross-Browser | Browser compatibility | 🟡 Medium |
| Test Integration | Part of test suite | 🟡 Medium |
| Slack Notifications | Team alerts | 🟢 Low |
| Custom Analysis | Deep investigation | 🟢 Low |

---

For more information, see **HYDRATION_VALIDATION_GUIDE.md** and **QUICK_REFERENCE.md**
