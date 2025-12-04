#!/usr/bin/env node

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  chromiumPath: process.env.CHROMIUM_PATH || '/usr/bin/chromium-browser',
  navigationTimeout: 30000,
  hydrationWait: 3000,
  loginEmail: 'thai@autobahn.test',
  loginPassword: 'AutobahnDev2025!@#$%',
};

const results = {
  timestamp: new Date().toISOString(),
  baseUrl: CONFIG.baseUrl,
  criticalIssues: [],
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

async function captureErrors(page, pageUrl, pageName) {
  console.log(`\n[TEST] ${pageName} (${pageUrl})`);

  const pageErrors = [];
  let hasReactError185 = false;

  // Capture console errors with better detail
  page.on('console', (msg) => {
    const type = msg.type();
    const text = msg.text();

    if (type === 'error') {
      if (text.includes('#185') || text.includes('hydration')) {
        hasReactError185 = true;
      }

      pageErrors.push({
        type: 'console.error',
        message: text,
        timestamp: new Date().toISOString(),
      });
    }
  });

  // Capture exceptions
  page.on('pageerror', (err) => {
    const msg = err.message || err.toString();
    if (msg.includes('#185') || msg.includes('hydration')) {
      hasReactError185 = true;
    }

    pageErrors.push({
      type: 'exception',
      message: msg,
    });
  });

  try {
    const startTime = Date.now();
    const fullUrl = pageUrl.startsWith('http') ? pageUrl : `${CONFIG.baseUrl}${pageUrl}`;

    await page.goto(fullUrl, {
      waitUntil: 'networkidle2',
      timeout: CONFIG.navigationTimeout,
    });

    // Wait for React hydration
    await new Promise(resolve => setTimeout(resolve, CONFIG.hydrationWait));

    const loadTime = Date.now() - startTime;

    if (pageErrors.length === 0) {
      console.log(`  ✅ PASSED - No errors (${loadTime}ms)`);
      results.testsPassed.push(pageName);
      return true;
    } else {
      console.log(`  ❌ FAILED - ${pageErrors.length} error(s)`);

      pageErrors.forEach((err, index) => {
        const preview = err.message.substring(0, 100).replace(/\n/g, ' ');
        console.log(`     ${index + 1}. [${err.type}] ${preview}`);

        results.criticalIssues.push({
          page: pageUrl,
          pageName,
          type: err.type,
          message: err.message.substring(0, 300),
        });
      });

      if (hasReactError185) {
        console.log('     ⚠️  CRITICAL: React Error #185 detected!');
      }

      return false;
    }
  } catch (error) {
    console.log(`  ❌ ERROR - ${error.message}`);
    results.criticalIssues.push({
      page: pageUrl,
      pageName,
      type: 'navigation_error',
      message: error.message,
    });
    return false;
  }
}

async function runValidation() {
  console.log('🔍 Browser Console Error Validation (With Authentication)');
  console.log('═'.repeat(70));
  console.log(`Target URL: ${CONFIG.baseUrl}`);
  console.log(`Test User: ${CONFIG.loginEmail}`);
  console.log('═'.repeat(70));

  let browser;

  try {
    browser = await puppeteer.launch({
      executablePath: CONFIG.chromiumPath,
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-first-run',
        '--no-zygote',
        '--single-process',
      ],
    });

    // Test public pages
    console.log('\n📄 Public Pages:');
    const publicPages = [
      { path: '/', name: 'Home' },
      { path: '/auth/signin', name: 'Sign In' },
      { path: '/auth/signup', name: 'Sign Up' },
    ];

    for (const pageConfig of publicPages) {
      const page = await browser.newPage();
      await captureErrors(page, pageConfig.path, pageConfig.name);
      await page.close();
    }

    // Test protected pages with authentication
    console.log('\n🔐 Protected Pages (With Authentication):');
    const protectedPages = [
      { path: '/app', name: 'App' },
      { path: '/dashboard', name: 'Dashboard' },
      { path: '/settings', name: 'Settings' },
    ];

    const authPage = await browser.newPage();

    try {
      await loginToApp(authPage);

      for (const pageConfig of protectedPages) {
        // Create fresh page for each protected page to maintain session
        const page = await browser.newPage();

        // Copy cookies from auth page
        const cookies = await authPage.cookies();
        await page.setCookie(...cookies);

        await captureErrors(page, pageConfig.path, pageConfig.name);
        await page.close();
      }
    } finally {
      await authPage.close();
    }

    await browser.close();
  } catch (error) {
    console.error('\n❌ CRITICAL ERROR:', error.message);
    if (browser) {
      try {
        await browser.close();
      } catch (e) {
        // Ignore
      }
    }
    process.exit(1);
  }

  // Save report
  const reportPath = path.join(process.cwd(), 'console-errors-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  console.log(`\n📊 Report saved: ${reportPath}`);

  // Print summary
  console.log('\n' + '═'.repeat(70));
  console.log('📊 VALIDATION SUMMARY');
  console.log('═'.repeat(70));
  console.log(`Tests Passed: ${results.testsPassed.length}`);
  console.log(`Tests Failed: ${results.testsFailed.length}`);
  console.log(`Critical Issues: ${results.criticalIssues.length}`);

  if (results.criticalIssues.length > 0) {
    console.log(`\n⚠️  CRITICAL ISSUES FOUND:\n`);
    results.criticalIssues.forEach((issue, index) => {
      const msg = issue.message.substring(0, 80).replace(/\n/g, ' ');
      console.log(`${index + 1}. [${issue.pageName}] ${issue.type}`);
      console.log(`   ${msg}`);
    });
    console.log('\n❌ VALIDATION FAILED');
    process.exit(1);
  } else {
    console.log('\n✅ VALIDATION PASSED - No critical errors found!');
    process.exit(0);
  }
}

runValidation().catch((error) => {
  console.error('Validation script error:', error);
  process.exit(1);
});
