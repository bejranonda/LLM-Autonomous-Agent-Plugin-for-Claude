---
name: design:audit
description: Analyze and audit existing design without implementing changes - provides AI Slop Score, identifies generic patterns, and recommends improvements
delegates-to: autonomous-agent:frontend-design-enhancer
---

# Design Audit Command

**Command**: `/design:audit`

Analyze and audit existing frontend design without making changes. Identifies generic "AI slop" patterns, calculates AI Slop Score, and provides actionable recommendations. Use this to understand design issues before deciding whether to apply fixes.

## When to Use

**Use `/design:audit` for:**
- Analyzing existing design without changes
- Getting AI Slop Score and recommendations
- Understanding design problems before fixing
- Design review and critique
- Before/after comparison preparation

**Use `/design:enhance` for:**
- Full design enhancement with implementation
- Automatic fixes applied immediately
- Complete typography, color, animation overhaul
- Production-ready design improvements

## How It Works

**Analysis-Only Workflow** (No Implementation):
1. **Design Audit**: Calculate AI Slop Score (0-100)
2. **Pattern Detection**: Identify generic patterns
3. **Recommendations**: Suggest specific improvements
4. **Report Generation**: Detailed findings and action plan

**No Changes Made** - This command is read-only and safe to run on production code

## Usage

### Basic Audit
```bash
/design:audit "src/components/LandingPage.tsx"
/design:audit "dashboard design"
/design:audit "current website"
```

### Specific Component Audit
```bash
/design:audit "navigation menu"
/design:audit "product card design"
/design:audit "login form"
```

### Full Application Audit
```bash
/design:audit "entire React app"
/design:audit "marketing website"
/design:audit "admin dashboard"
```

## Output Format

**Terminal** (15-20 lines):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN AUDIT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Slop Score: 75/100 (High - Needs Improvement)

Generic Patterns Detected:
1. Typography: Inter font (30 points) - Very common AI default
2. Colors: Purple gradient (25 points) - Overused AI aesthetic
3. Background: Plain white (20 points) - No visual depth
4. Animations: None (0 points) - Static interface
5. Layout: Standard grid (0 points) - Acceptable

Top 3 Recommendations:
1. Replace Inter with distinctive pairing (e.g., Playfair Display + Source Sans)
2. Use intentional color scheme (ocean, sunset, forest, not purple)
3. Add layered backgrounds with gradients, textures, or patterns

Full Report: .claude/reports/design-audit-[timestamp].md
Time: 1m 15s
```

**File Report** (Comprehensive):
Saved to `.claude/reports/design-audit-[timestamp].md`:
- AI Slop Score breakdown by category
- All generic patterns detected with severity
- Detailed recommendations with code examples
- Before/after mockups (if applicable)
- Action plan prioritized by impact

## AI Slop Score Breakdown

**Score Components** (0-100, lower is better):

| Category | Points | Generic Pattern | Distinctive Alternative |
|----------|--------|----------------|------------------------|
| Typography | 30 | Inter, Roboto, Arial | Playfair Display, Space Grotesk, JetBrains Mono |
| Colors | 25 | Purple gradients | Ocean (cyan+teal), Sunset (orange+pink), Forest (green+brown) |
| Background | 20 | Plain white/solid | Layered gradients, textures, patterns, noise |
| Animations | 15 | None or generic | Page load sequences, purposeful micro-interactions |
| Layout | 10 | Standard grid | Asymmetric, broken grid, overlapping elements |

**Scoring**:
- **0-30**: Distinctive (Excellent)
- **31-50**: Above Average (Good)
- **51-70**: Average (Needs Work)
- **71-100**: Generic AI Slop (Poor)

## Audit Report Structure

### Section 1: Executive Summary
- AI Slop Score and grade
- Overall assessment
- Priority level (Low/Medium/High/Critical)

### Section 2: Typography Analysis
- Font families detected
- Font weight usage
- Type scale analysis
- Recommendations with examples

### Section 3: Color Analysis
- Color palette extraction
- Contrast ratio checks (WCAG AA/AAA)
- Generic pattern detection
- Intentional palette suggestions

### Section 4: Background Analysis
- Background treatment evaluation
- Depth and layering assessment
- Texture and pattern usage
- Enhancement recommendations

### Section 5: Animation Analysis
- Animation inventory
- Motion purpose evaluation
- Accessibility compliance
- Purposeful animation suggestions

### Section 6: Layout Analysis
- Grid structure evaluation
- Visual hierarchy assessment
- Innovation score
- Layout enhancement ideas

### Section 7: Action Plan
Prioritized recommendations:
1. **Quick Wins** (1-2 hours)
2. **Medium Impact** (3-5 hours)
3. **Major Overhaul** (1-2 days)

## Examples

### Example 1: Landing Page Audit
```bash
/design:audit "marketing landing page"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN AUDIT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Slop Score: 85/100 (Very High - Critical Issues)

Generic Patterns Detected:
1. Typography: Inter font everywhere (30 points)
   → Recommendation: Playfair Display (headings) + Source Sans 3 (body)

2. Colors: Purple (#A855F7) to blue (#3B82F6) gradient (25 points)
   → Recommendation: Ocean theme (Cyan #06B6D4 + Teal #14B8A6)

3. Background: Plain white #FFFFFF (20 points)
   → Recommendation: Layered radial gradient with geometric grid overlay

4. Animations: None detected (10 points)
   → Recommendation: Page load fade + staggered section reveals

5. Layout: Standard 12-column grid (0 points)
   → Acceptable, but could add asymmetric hero section

Design Grade: D (Poor)
Priority: HIGH - Immediate attention needed

Full Report: .claude/reports/design-audit-landing-20250115.md
Time: 1m 22s
```

### Example 2: Dashboard Audit
```bash
/design:audit "admin dashboard"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN AUDIT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Slop Score: 45/100 (Average - Room for Improvement)

Generic Patterns Detected:
1. Typography: Roboto font (15 points) - Partial credit, overused but acceptable
2. Colors: Intentional blue palette (0 points) - Good contrast, professional
3. Background: White cards on gray (5 points) - Basic but functional
4. Animations: Hover states only (10 points) - Could add micro-interactions
5. Layout: Sidebar + grid (0 points) - Standard but effective

Design Grade: B- (Above Average)
Priority: MEDIUM - Enhancement optional

Strengths:
- Good color contrast (WCAG AAA compliant)
- Consistent spacing and alignment
- Clear information hierarchy

Improvement Opportunities:
1. Consider distinctive monospace font for data tables
2. Add subtle background patterns to reduce flatness
3. Implement loading state animations for better UX

Full Report: .claude/reports/design-audit-dashboard-20250115.md
Time: 58s
```

### Example 3: Component Audit
```bash
/design:audit "product card component"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN AUDIT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Slop Score: 55/100 (Average - Needs Improvement)

Component: Product Card

Generic Patterns Detected:
1. Typography: Inter 14px/16px/20px (20 points)
   → Use varied scale: 12px/16px/24px with different weights

2. Colors: Default Tailwind blue (10 points)
   → Apply consistent brand colors with intentional palette

3. Hover Animation: Scale 1.05 (5 points)
   → Generic, consider glow effect or shadow elevation instead

Specific Recommendations:
1. Font Scale: Increase title from 20px to 28px (more dramatic)
2. Weight Contrast: Use font-weight 900 for price, 300 for description
3. Hover State: Replace scale with shadow-lg + subtle border glow
4. Card Background: Add subtle gradient or texture

Design Grade: C+ (Average)
Priority: MEDIUM

Full Report: .claude/reports/design-audit-product-card-20250115.md
Time: 42s
```

## Comparison with /design:enhance

| Feature | /design:audit | /design:enhance |
|---------|---------------|-----------------|
| Analysis | ✅ Comprehensive | ✅ Comprehensive |
| AI Slop Score | ✅ Calculated | ✅ Calculated |
| Recommendations | ✅ Detailed | ✅ Implemented |
| Code Changes | ❌ None | ✅ Applied |
| File Report | ✅ Yes | ✅ Yes |
| Safe for Production | ✅ Read-only | ⚠️ Makes changes |
| Time | 1-3 min | 5-15 min |
| Best For | Analysis first | Full enhancement |

## Workflow Integration

**Recommended Workflow**:
1. Run `/design:audit` first to understand issues
2. Review recommendations in report
3. Decide which improvements to apply
4. Run `/design:enhance` to implement changes
5. Compare before/after AI Slop Scores

**Example**:
```bash
# Step 1: Audit current design
/design:audit "landing page"
# AI Slop Score: 85/100 - Review recommendations

# Step 2: Apply fixes
/design:enhance "landing page"
# AI Slop Score: 25/100 - Improvement: 60 points
```

## Pattern Learning

Audit patterns stored for optimization:
```json
{
  "task_type": "design_audit",
  "component_type": "landing_page",
  "ai_slop_score": 85,
  "generic_patterns": ["inter_font", "purple_gradient", "plain_background"],
  "time_taken": "1m 22s"
}
```

Learns:
- Common generic patterns by component type
- Effective recommendations by project type
- AI Slop Score baselines for different designs

---

**Version**: 1.0.0
**Integration**: Works with frontend-design-enhancer agent (audit mode)
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: Read tool for file analysis
