---
description: Enhance frontend design by applying research-backed aesthetic principles from Claude's official design research - implements distributional convergence awareness, high-impact motion, distinctive typography, and altitude-appropriate guidance
category: design
---

# Frontend Design Enhancement Command

Transform functional but generic frontend designs into distinctive, polished user experiences that avoid "AI slop" aesthetics. Based on official research from ["Improving frontend design through Skills"](https://claude.com/blog/improving-frontend-design-through-skills) by Anthropic.

## Core Principles Applied

**Distributional Convergence**: Breaks away from statistically common "safe defaults" (Inter fonts, purple gradients, minimal animations) that dominate training data distributions.

**Altitude-Appropriate Guidance**: Balances specificity and flexibility - provides contextual principles with concrete examples without prescribing exact values.

**High-Impact Moments**: One well-orchestrated page load with staggered reveals > dozen random micro-animations.

## Workflow

1. **Design Audit** (frontend-design-enhancer agent):
   - Identify current fonts, colors, backgrounds, animations
   - Calculate AI Slop Score (0-100, lower is better)
   - Detect distributional defaults:
     - Generic fonts (Inter/Roboto/Open Sans/Lato)
     - Purple-on-white gradients (#a855f7 → #ffffff)
     - Plain backgrounds with no depth
     - Missing or random animations

2. **Typography Enhancement** (frontend-aesthetics skill):
   - **High-Contrast Pairings**: Display + monospace, serif + geometric sans
   - **Extreme Weight Variations**: 100-200 (ultra-thin) OR 800-900 (extra-bold) for headings
   - **Size Jumps**: 3x+ ratio (hero 4rem → body 1rem), not incremental 1.5x
   - Implement fluid typography with clamp()
   - Select from distinctive font categories (code-aesthetic, editorial, technical, playful, elegant)

3. **Color Scheme Design**:
   - Create intentional palette with mood (professional, energetic, calm, bold)
   - **Forbidden**: Purple-on-white (#a855f7 → #ffffff)
   - Draw inspiration from IDE themes and cultural aesthetics
   - Ensure WCAG AA contrast compliance (4.5:1 minimum)
   - Use CSS variables for cohesive system

4. **Background Treatment**:
   - Layer CSS gradients for depth (mesh gradients, radial glows)
   - Add subtle textures (noise, geometric grids)
   - Implement ambient backgrounds (waves, patterns)
   - **Avoid**: Plain white (#FFFFFF) or solid colors

5. **Animation Implementation** (web-artifacts-builder skill):
   - **Priority #1**: Well-orchestrated page load (highest impact)
   - **HTML Projects**: CSS-only animations (better performance)
   - **React Projects**: Framer Motion for complex choreography
   - Implement staggered reveals with Motion variants
   - Add purposeful micro-interactions (hover, click feedback)
   - **Always**: Respect `prefers-reduced-motion` (accessibility first)

6. **Validation** (quality-controller agent):
   - Verify AI Slop Score improved to < 30 (distinctive design)
   - Check accessibility standards (WCAG AA)
   - Test responsive behavior across breakpoints
   - Validate animation performance (GPU-accelerated properties)
   - Store design pattern for future learning

## Output

**Terminal (Concise)**:
```
[OK] Design enhanced with Claude research principles

AI Slop Score: 85 -> 15 (Improved by 70 points - Distinctive)

Improvements Applied:
- Typography: Inter (generic) -> Playfair Display 700 + Source Sans 3 300 (high-contrast)
  * Extreme weights: 700 (headings) vs 300 (body)
  * Size jumps: 4rem hero -> 1rem body (4x ratio)
- Colors: Purple-on-white (#a855f7 → #fff) -> Ocean blue + amber (professional mood)
  * Avoided distributional default
- Background: Plain white -> Layered gradient + subtle noise (depth)
- Animations: None -> Orchestrated page load with staggered reveals (Framer Motion)
  * High-impact moment prioritized

Files Modified: 4 (tailwind.config.js, index.html, App.tsx, index.css)
Pattern Stored: design-enhancement-editorial-professional
Next Steps: Test responsive behavior, validate accessibility
Time: 12 minutes
```

**File (Comprehensive)** - Saved to `.claude/reports/design-enhancement-[timestamp].md`:
- **Design Philosophy**: Distributional convergence awareness, altitude-appropriate guidance
- **Full Audit**: Before/after comparison with AI Slop Score breakdown
- **Typography**:
  - Font pairing rationale (high-contrast, extreme weights)
  - Implementation code (Tailwind config, Google Fonts imports)
  - Size scale with fluid clamp() values
- **Color System**:
  - Complete palette with HSL values and CSS variables
  - Mood/brand alignment explanation
  - Contrast ratio validation (WCAG AA compliance)
- **Background Patterns**:
  - Layering techniques (gradients, noise, textures)
  - CSS implementation code
- **Animation System**:
  - Framer Motion setup and configuration
  - Page transition variants
  - Staggered list animation patterns
  - Micro-interaction examples
  - Reduced motion accessibility
- **Accessibility Checklist**: Keyboard navigation, screen readers, reduced motion
- **Performance Metrics**: GPU-accelerated properties used, bundle size impact
- **Before/After Screenshots** (if available)

## Usage Examples

**Basic Enhancement**:
```bash
/design:enhance "Improve landing page aesthetics"
# Applies balanced design improvements across all aspects
```

**Project-Specific**:
```bash
/design:enhance "Make dashboard look professional with tech-ocean color scheme"
# Targets specific color mood

/design:enhance "Apply editorial design to blog with Playfair Display"
# Requests specific typography category

/design:enhance "React app needs distinctive design with Framer Motion"
# Specifies React + motion library
```

**Problem-Focused**:
```bash
/design:enhance "Fix generic AI appearance - looks like every tutorial"
# Addresses AI slop problem directly

/design:enhance "Too much purple gradient, needs unique identity"
# Tackles specific distributional default
```

## Technical Implementation

**Skills Loaded**:
- `autonomous-agent:frontend-aesthetics` - Core design principles and patterns
- `autonomous-agent:web-artifacts-builder` - React + Tailwind + Framer Motion patterns
- `autonomous-agent:gui-design-principles` - Foundational UI/UX principles
- `autonomous-agent:pattern-learning` - Learn from successful design patterns

**Agents Delegated**:
- `frontend-design-enhancer` (Group 3: Hand) - Executes design implementation
- `quality-controller` (Group 4: Guardian) - Validates accessibility and standards

**Auto-Fixes Applied**:
- Generic font replacement (Inter → distinctive alternatives)
- Purple gradient elimination (#a855f7 detection)
- Background depth addition (plain → layered)
- Animation implementation (static → purposeful motion)
- Contrast ratio corrections (WCAG AA compliance)

## Success Criteria

**Quantitative**:
- AI Slop Score < 30 (distinctive design)
- WCAG AA contrast: 4.5:1 minimum for text
- Typography size jumps: 3x+ ratio between levels
- Font weights: 100-200 or 800-900 for headings (extreme variation)

**Qualitative**:
- Distinctive fonts (NOT Inter/Roboto/Open Sans/Lato)
- Intentional color scheme (NOT purple-on-white #a855f7 → #ffffff)
- Layered backgrounds (NOT plain white #FFFFFF)
- High-impact animations (orchestrated page load, NOT random micro-animations)
- Altitude-appropriate implementation (contextual, NOT overly prescriptive)

**Learning**:
- Design pattern stored in `.claude-patterns/`
- Font pairing effectiveness tracked
- Color scheme mood success recorded
- Animation impact measured for future optimizations
