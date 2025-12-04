#!/usr/bin/env node

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  chromiumPath: process.env.CHROMIUM_PATH || '/usr/bin/chromium-browser',
  navigationTimeout: 30000,
  hydrationWait: 3000,
  loginEmail: process.env.TEST_EMAIL || 'thai@autobahn.test',
  loginPassword: process.env.TEST_PASSWORD || 'AutobahnDev2025!@#$%',
};

const results = {
  timestamp: new Date().toISOString(),
  baseUrl: CONFIG.baseUrl,
  errorDetails: [],
  testsPassed: [],
  testsFailed: [],
};

async function loginToApp(page) {
  console.log('  ↳ Logging in...');

  // Navigate to signin
  await page.goto(`${CONFIG.baseUrl}/auth/signin`, {
    waitUntil: 'networkidle2',
    timeout: CONFIG.navigationTimeout,
  });

  // Wait for form
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Fill in email
  await page.type('input[type="email"]', CONFIG.loginEmail, { delay: 50 });

  // Fill in password
  await page.type('input[type="password"]', CONFIG.loginPassword, { delay: 50 });

  // Submit form
  await Promise.all([
    page.click('button[type="submit"]'),
    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 15000 }).catch(() => {}),
  ]);

  // Wait for app to load
  await new Promise(resolve => setTimeout(resolve, 2000));
  console.log('  ↳ Login complete');
}

async function captureDetailedErrors(page, pageUrl, pageName) {
  console.log(`\n[TEST] ${pageName} (${pageUrl})`);

  const collectedErrors = [];

  // Intercept console messages with full details
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg);
    }
  });

  // Capture uncaught exceptions with full stack
  page.on('pageerror', (err) => {
    collectedErrors.push({
      type: 'uncaught.exception',
      message: err.message,
      stack: err.stack,
      timestamp: new Date().toISOString(),
      page: pageUrl,
      pageName: pageName,
    });
  });

  // Capture request failures
  page.on('requestfailed', (request) => {
    if (request.failure().errorText.includes('ERR')) {
      collectedErrors.push({
        type: 'network.error',
        message: `${request.method()} ${request.url()}`,
        error: request.failure().errorText,
        timestamp: new Date().toISOString(),
        page: pageUrl,
        pageName: pageName,
      });
    }
  });

  try {
    // Navigate to page
    const response = await page.goto(pageUrl, {
      waitUntil: 'networkidle2',
      timeout: CONFIG.navigationTimeout,
    });

    // Wait for hydration/rendering
    await new Promise(resolve => setTimeout(resolve, CONFIG.hydrationWait));

    // Try to extract error details from window object
    const errorInfo = await page.evaluate(() => {
      const errors = [];

      // Check for unhandled errors
      if (window.__reactHandledErrors) {
        errors.push({
          source: 'React Errors',
          details: window.__reactHandledErrors,
        });
      }

      // Check for error boundary
      const errorBoundary = document.body.innerText;
      if (errorBoundary.includes('Something went wrong')) {
        errors.push({
          source: 'Error Boundary',
          visible: true,
          text: errorBoundary.substring(0, 500),
        });
      }

      return errors;
    });

    // Add page-level error info ONLY if there are actual errors
    if (errorInfo && errorInfo.length > 0) {
      collectedErrors.push({
        type: 'page.evaluation',
        details: errorInfo,
        timestamp: new Date().toISOString(),
        page: pageUrl,
        pageName: pageName,
      });
    }

    // Process console errors that were captured during navigation
    if (consoleErrors.length > 0) {
      for (const msg of consoleErrors) {
        try {
          // Try to get the actual message text first
          let errorMessage = msg.text();

          // Try to extract from args if message is just JSHandle@error
          if (errorMessage.includes('JSHandle@error')) {
            const args = msg.args();
            if (args.length > 0) {
              try {
                // Try to convert the JSHandle to a string representation
                const remoteObject = args[0];
                const result = await remoteObject.evaluate(el => {
                  if (el && typeof el === 'object') {
                    return {
                      name: el.name,
                      message: el.message,
                      stack: el.stack,
                      toString: String(el),
                    };
                  }
                  return String(el);
                }).catch(() => null);

                if (result) {
                  errorMessage = JSON.stringify(result);
                }
              } catch (e) {
                // If we can't extract, use the text as is
              }
            }
          }

          collectedErrors.push({
            type: 'console.error',
            message: errorMessage,
            timestamp: new Date().toISOString(),
            page: pageUrl,
            pageName: pageName,
          });
        } catch (e) {
          collectedErrors.push({
            type: 'console.error',
            message: `Error processing console message: ${e.message}`,
            timestamp: new Date().toISOString(),
            page: pageUrl,
            pageName: pageName,
          });
        }
      }
    }

    // Check HTTP response
    const status = response ? response.status() : 'unknown';
    if (status >= 400) {
      collectedErrors.push({
        type: 'http.error',
        status: status,
        url: pageUrl,
        timestamp: new Date().toISOString(),
      });
    }

    // Wait a bit more for async errors
    await new Promise(resolve => setTimeout(resolve, 1000));

  } catch (err) {
    collectedErrors.push({
      type: 'navigation.error',
      message: err.message,
      stack: err.stack,
      page: pageUrl,
      pageName: pageName,
      timestamp: new Date().toISOString(),
    });
  }

  const status = collectedErrors.length === 0 ? '✅ PASSED' : `❌ FAILED (${collectedErrors.length} error(s))`;
  console.log(`  ${status}`);

  if (collectedErrors.length > 0) {
    collectedErrors.forEach((err, idx) => {
      console.log(`     ${idx + 1}. [${err.type}] ${err.message || err.error || 'Unknown error'}`);
      if (err.stack) {
        console.log(`        Stack: ${err.stack.split('\n')[0]}`);
      }
    });

    results.errorDetails.push(...collectedErrors);
    results.testsFailed.push(pageName);
  } else {
    results.testsPassed.push(pageName);
  }

  return collectedErrors.length === 0;
}

async function main() {
  let browser;

  try {
    // Launch browser
    browser = await puppeteer.launch({
      executablePath: CONFIG.chromiumPath,
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-web-resources',
        '--disable-dev-shm-usage',
      ],
    });

    const page = await browser.newPage();

    // Set viewport
    await page.setViewport({ width: 1280, height: 720 });

    console.log('\n🔍 Browser Console Error Validation (With Authentication)');
    console.log('══════════════════════════════════════════════════════════════════════');
    console.log(`Target URL: ${CONFIG.baseUrl}`);
    console.log(`Test User: ${CONFIG.loginEmail}`);
    console.log('══════════════════════════════════════════════════════════════════════\n');

    console.log('📄 Public Pages:\n');

    // Test public pages
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/`, 'Home');
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/auth/signin`, 'Sign In');
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/auth/signup`, 'Sign Up');

    // Login for protected pages
    console.log('\n🔐 Protected Pages (With Authentication):');
    await loginToApp(page);

    // Test protected pages
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/app`, 'App');
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/dashboard`, 'Dashboard');
    await captureDetailedErrors(page, `${CONFIG.baseUrl}/settings`, 'Settings');

    // Save results
    const reportPath = path.join(process.cwd(), 'console-errors-detailed-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
    console.log(`\n📊 Detailed report saved: ${reportPath}`);

    // Print summary
    console.log('\n══════════════════════════════════════════════════════════════════════');
    console.log('📊 VALIDATION SUMMARY');
    console.log('══════════════════════════════════════════════════════════════════════');
    console.log(`Tests Passed: ${results.testsPassed.length}`);
    console.log(`Tests Failed: ${results.testsFailed.length}`);
    console.log(`Total Errors: ${results.errorDetails.length}\n`);

    if (results.errorDetails.length > 0) {
      console.log('⚠️  ERRORS FOUND:\n');
      results.errorDetails.forEach((error, idx) => {
        console.log(`${idx + 1}. [${error.type}] ${error.pageName || 'Unknown'}`);
        console.log(`   Message: ${error.message || error.error || 'N/A'}`);
        if (error.stack) {
          console.log(`   Stack: ${error.stack.split('\n').slice(0, 2).join('\n   ')}`);
        }
        console.log('');
      });
      console.log('❌ VALIDATION FAILED');
    } else {
      console.log('✅ VALIDATION PASSED - All pages loaded without errors');
    }

  } catch (error) {
    console.error('❌ Test error:', error.message);
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

main();
