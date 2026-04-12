# Release Notes v8.3.0 - Dashboard Rewrite & Code Health

**Version**: 8.3.0
**Release Date**: 2026-04-12
**Type**: Minor Release (Rewrite & Cleanup)

## Overview

Version 8.3.0 rewrites the broken dashboard from scratch, reducing it from 6835 non-functional lines to 534 working lines. The dashboard now starts cleanly, serves 11 API endpoints, and renders a 4-tab dark-theme UI with Chart.js. All dependencies on deleted modules have been eliminated.

## Key Changes

### Dashboard Rewrite (lib/dashboard.py)

**Before**: 6835 lines, SyntaxError on import, Flask app commented out, 3655 lines of inline HTML, imports of deleted modules causing ImportError.

**After**: 534 lines, zero local imports, Flask app factory pattern, CDN-based Chart.js, 11 working API endpoints.

| Metric | Before | After |
|--------|--------|-------|
| Total lines | 6835 | 534 |
| API endpoints | 30+ (broken) | 11 (working) |
| Local module deps | 5+ | 0 |
| HTML template | 3655 inline | 190 CDN-based |
| Data classes | 2400 lines | 10 functions |

### New API Endpoints

All endpoints read from `.claude-patterns/*.json` with a 5-second cache:

- `GET /` - Dashboard HTML
- `GET /api/overview` - Task/pattern metrics
- `GET /api/quality-trends` - Quality assessment history
- `GET /api/skills` - Skill effectiveness data
- `GET /api/agents` - Agent performance metrics
- `GET /api/recent-activity` - Recent task records
- `GET /api/current-model` - Current model info
- `GET /api/model-quality-scores` - Model comparison scores
- `GET /api/debugging-performance` - Debugging metrics
- `GET /api/tokens/overview` - Token analytics
- `GET /api/kpi/overview` - KPI summary

### Dashboard UI

4-tab interface:
- **Overview**: Metric cards + quality timeline chart
- **Quality**: Model scores + debugging performance table
- **Skills**: Effectiveness bar chart + usage history table
- **Agents**: Activity log with pass/fail badges

Dark theme, responsive, auto-refresh every 30 seconds.

## CLI Compatibility

Same interface as before:
```bash
python lib/dashboard.py --port 5000 --patterns-dir .claude-patterns --no-browser
```

`dashboard_launcher.py` continues to work with the rewritten dashboard.

## Upgrade Notes

No configuration changes required. The dashboard reads the same JSON files from `.claude-patterns/` as before.
