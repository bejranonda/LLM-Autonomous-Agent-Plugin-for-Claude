# Common Hydration Issues & Solutions

Reference guide for the most common hydration-related problems and their fixes.

## Issue 1: "Something went wrong" Error Boundary Visible

### Symptoms
- Page shows error boundary UI
- Error message: "Something went wrong"
- Browser console shows React error #185

### Root Cause Analysis

1. **useSession() called during render**
   - NextAuth's `useSession()` status changes server→client
   - Server: `status = 'loading'`
   - Client: `status = 'authenticated'` or `'unauthenticated'`
   - Component renders different HTML → hydration mismatch

2. **Zustand stores with localStorage**
   - Server: stores are empty (no localStorage)
   - Client: stores hydrate from localStorage
   - State mismatch causes different HTML

3. **useReducedMotion or media queries**
   - Server: can't read media queries (default false)
   - Client: reads actual preference (could be true)
   - Animation CSS differs → hydration mismatch

### Solution

**Option A: Use HydrationBoundary (Recommended)**

```typescript
// src/components/hydration-boundary.tsx
'use client';

import { ReactNode, useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';

export function HydrationBoundary({ children }: { children: ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);
  const { status } = useSession();

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Only render when hydration is complete AND authenticated
  const isReady = isMounted && status === 'authenticated';

  if (!isReady) {
    return <div className="min-h-screen bg-bg-primary" suppressHydrationWarning />;
  }

  return <>{children}</>;
}
```

**Usage:**
```typescript
// pages/app/page.tsx
export default function AppPage() {
  return (
    <HydrationBoundary>
      <ProtectedRoute>
        <AppContent />
      </ProtectedRoute>
    </HydrationBoundary>
  );
}
```

**Option B: useSession Guard in Child Component**

```typescript
// Prevent useSession from running during render
export function SafeComponent() {
  const [isMounted, setIsMounted] = useState(false);
  const { status } = useSession();

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted || status === 'loading') {
    return <div className="min-h-screen" />;
  }

  if (status === 'unauthenticated') {
    return <div>Not authenticated</div>;
  }

  return <div>Authenticated content</div>;
}
```

**Option C: Suppress Hydration Warning (Temporary)**

```typescript
// Only as last resort - doesn't fix the issue, just hides the warning
<div suppressHydrationWarning>
  {/* Content that might have hydration mismatch */}
</div>
```

### Prevention Checklist

- [ ] Wrap page in HydrationBoundary
- [ ] Don't use useSession() during render
- [ ] Don't access localStorage during render
- [ ] Use useReducedMotionSafe instead of useReducedMotion
- [ ] Add suppressHydrationWarning to placeholder divs

---

## Issue 2: JSHandle@error in Puppeteer Tests

### Symptoms
- Puppeteer validation shows `JSHandle@error`
- Can't see actual error message
- Error happens during test but not visible in code

### Root Cause

Puppeteer can't serialize Error objects to JSON:
```javascript
// This fails:
msg.args().forEach(arg => {
  arg.jsonValue() // ← Error object can't be serialized
});
```

### Solution

Extract error from the page using `evaluate()`:

```javascript
// In validation script
const errorInfo = await page.evaluate(() => {
  // Access window object directly
  if (window.__lastError) {
    return {
      message: window.__lastError.message,
      stack: window.__lastError.stack
    };
  }

  // Or check error boundary
  const errorBoundary = document.querySelector('[role="alert"]');
  if (errorBoundary) {
    return {
      type: 'error-boundary',
      text: errorBoundary.innerText
    };
  }
});
```

Or use the detailed validation script provided in this toolkit.

---

## Issue 3: useReducedMotion Mismatch

### Symptoms
- Pages with animations show different HTML on server vs client
- No visual error, but hydration mismatch occurs
- Usually subtle (animations just fail)

### Root Cause

Framer Motion's `useReducedMotion()` hook reads browser's media query:
- Server: No media query available → defaults to false
- Client: Reads actual system preference (could be true)
- Components render different styles

### Solution

Create a safe wrapper:

```typescript
// src/hooks/use-reduced-motion-safe.ts
'use client';

import { useEffect, useState } from 'react';
import { useReducedMotion } from 'framer-motion';

export function useReducedMotionSafe(): boolean {
  const [isMounted, setIsMounted] = useState(false);
  const actualPreference = useReducedMotion();

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Return false on server and during hydration
  // After hydration, return actual preference
  return isMounted ? (actualPreference ?? false) : false;
}
```

**Usage:**
```typescript
// Replace useReducedMotion with useReducedMotionSafe
const shouldReduceMotion = useReducedMotionSafe();  // ← Use this
// const shouldReduceMotion = useReducedMotion();     // ← Not this
```

---

## Issue 4: Zustand Store Persist Hydration

### Symptoms
- Empty state on server, populated state on client
- State values different between renders
- localStorage data doesn't match server data

### Root Cause

Zustand persist middleware hydrates from localStorage automatically:
- Server: Store has initial state
- Client: Store reads localStorage (different data)
- HTML differs because state differs

### Solution

Add `skipHydration: true` to prevent automatic hydration:

```typescript
// src/lib/stores/my-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useMyStore = create<MyStore>()(
  persist(
    (set) => ({
      // store definition
    }),
    {
      name: 'my-store',
      skipHydration: true  // ← Add this
    }
  )
);
```

Then manually rehydrate in a useEffect:

```typescript
// In your component or main layout
useEffect(() => {
  useMyStore.persist.rehydrate();
}, []);
```

---

## Issue 5: Dynamic Imports Causing Hydration Mismatch

### Symptoms
- Different scripts loaded on server vs client
- Optional features conditionally loaded
- Hydration failure with specific conditionals

### Root Cause

Dynamic imports with `next/dynamic` can be loaded differently:
- Server: May not load optional component
- Client: Loads optional component
- HTML structure differs

### Solution

Use `ssr: false` for client-only components:

```typescript
// ✗ Wrong - might load differently on server vs client
const OptionalComponent = dynamic(() => import('./Optional'));

// ✓ Correct - explicitly client-only
const OptionalComponent = dynamic(() => import('./Optional'), {
  ssr: false  // ← Add this
});
```

Or wrap in HydrationBoundary:

```typescript
<HydrationBoundary>
  <DynamicComponent />
</HydrationBoundary>
```

---

## Issue 6: Window/Document Object Access

### Symptoms
- Script error about `window` being undefined
- Code tries to access browser APIs during render
- Server can't execute code needing browser

### Root Cause

`window` and `document` don't exist on the server:
```javascript
// ✗ Fails on server
if (window.localStorage) { ... }  // window is undefined

// ✓ Correct - with guard
if (typeof window !== 'undefined' && window.localStorage) { ... }
```

### Solution

Always guard browser API access:

```typescript
// Safe patterns:

// Pattern 1: useEffect (only runs on client)
useEffect(() => {
  const value = localStorage.getItem('key');
}, []);

// Pattern 2: Conditional render
const isClient = typeof window !== 'undefined';
if (!isClient) return null;
const value = localStorage.getItem('key');

// Pattern 3: Guard at call site
if (typeof window === 'undefined') return;
window.scrollTo(0, 0);
```

---

## Issue 7: Missing or Incorrect Suppressions

### Symptoms
- React warns about hydration mismatch in console
- Warning can be suppressed but not fixed
- Placeholder divs have wrong dimensions

### Root Cause

Placeholder div during hydration must match actual div:
```typescript
// ✗ Wrong - sizes don't match
<ClientOnly>
  {/* Server shows this: */}
  <div className="min-h-screen" />  {/* Screen height */}
  {/* Client shows this: */}
  <div className="h-96" />  {/* 24rem height */}
</ClientOnly>
```

### Solution

Match placeholder to actual content:

```typescript
// ✓ Correct - same dimensions
<ClientOnly>
  {/* Always shows same placeholder */}
  <div className="min-h-screen bg-primary" suppressHydrationWarning />
</ClientOnly>
```

Add `suppressHydrationWarning` to known-safe elements:

```typescript
// These might legitimately differ on server vs client:
<motion.div suppressHydrationWarning>
<Button suppressHydrationWarning>
<div suppressHydrationWarning>
```

---

## Issue 8: Next.js Router Timing

### Symptoms
- `useRouter()` hook causes hydration issues
- Router.push() called during render
- Redirect happens at wrong time

### Root Cause

Router state changes between server and client:
- Server: Router not ready
- Client: Router becomes ready
- Different rendering based on router state

### Solution

Defer router usage to useEffect:

```typescript
'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export function SafeComponent() {
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    setIsReady(true);
    // Safe to use router here
  }, []);

  if (!isReady) {
    return <div className="min-h-screen" />;
  }

  return <YourContent />;
}
```

---

## Checklist: Fixing Hydration Issues

Use this checklist when debugging hydration problems:

- [ ] **Error Boundary Visible?**
  - Add HydrationBoundary wrapper
  - Check useSession() usage

- [ ] **useSession() During Render?**
  - Move to useEffect
  - Guard with isMounted flag
  - Use HydrationBoundary

- [ ] **Zustand Store Issue?**
  - Add skipHydration: true
  - Manually rehydrate in useEffect
  - Check localStorage access patterns

- [ ] **Media Query/Animation Issue?**
  - Replace useReducedMotion with useReducedMotionSafe
  - Defer animation checks to useEffect
  - Suppress non-critical warnings

- [ ] **Window/Document Access?**
  - Add typeof window !== 'undefined' guards
  - Move to useEffect
  - Use dynamic imports with ssr: false

- [ ] **Dynamic Imports?**
  - Use ssr: false for client-only components
  - Wrap in HydrationBoundary
  - Check conditional loading logic

- [ ] **Placeholder Dimensions?**
  - Match placeholder to actual content
  - Add suppressHydrationWarning
  - Verify CSS classes match

- [ ] **Router/Navigation Issue?**
  - Defer router usage to useEffect
  - Guard with isReady state
  - Check redirect logic

---

## Quick Decision Tree

```
Hydration Error?
├─ Error Boundary Visible?
│  └─ YES → Add HydrationBoundary (Issue 1)
├─ useSession() in component?
│  └─ YES → Move to useEffect or HydrationBoundary (Issue 1)
├─ Zustand store with persist?
│  └─ YES → Add skipHydration: true (Issue 4)
├─ useReducedMotion() used?
│  └─ YES → Use useReducedMotionSafe (Issue 3)
├─ window.X accessed in render?
│  └─ YES → Add typeof window guard (Issue 6)
├─ Dynamic imports?
│  └─ YES → Add ssr: false (Issue 5)
├─ Placeholder div in ClientOnly?
│  └─ YES → Match dimensions and add suppressHydrationWarning (Issue 7)
└─ useRouter() in render?
   └─ YES → Defer to useEffect (Issue 8)
```

---

## Testing Your Fix

After applying a fix:

1. **Rebuild project**
   ```bash
   npm run build
   ```

2. **Restart server**
   ```bash
   npm run dev
   ```

3. **Run validation**
   ```bash
   npm run validate:errors
   ```

4. **Check report**
   ```bash
   cat console-errors-detailed-report.json | jq '.errorDetails[] | select(.pageName == "App")'
   ```

5. **Verify in browser**
   - Open page in browser
   - Check DevTools console
   - No React errors should appear

---

## Additional Resources

- [React #185 Documentation](https://react.dev/errors/185)
- [Next.js Hydration Docs](https://nextjs.org/docs/messages/react-hydration-error)
- [Zustand Persist Middleware](https://docs.pmnd.rs/zustand/integrations/persisting-store-data)
- [NextAuth Session Handling](https://next-auth.js.org/getting-started/introduction)

---

**Created:** December 2, 2025
**Last Updated:** December 2, 2025
