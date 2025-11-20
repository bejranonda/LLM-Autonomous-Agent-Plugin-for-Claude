---
name: research:quick
description: Fast research for quick answers without full planning and validation - ideal for straightforward lookups and simple comparisons
delegates-to: autonomous-agent:research-executor
---

# Quick Research Command

**Command**: `/research:quick`

Fast, lightweight research for quick answers and straightforward lookups. Skips the full planning and validation phases, going straight to execution for rapid results.

## When to Use

**Use `/research:quick` for:**
- Simple factual lookups
- Quick comparisons (2-3 options)
- Checking latest versions/releases
- Finding specific documentation
- Fast technical references

**Use `/research:structured` for:**
- Complex multi-faceted research
- Thorough comparison with trade-offs
- Research requiring validation
- Academic/professional research
- Long-form investigation

## How It Works

**Streamlined Workflow** (1 step vs 3 steps):
1. **Execution Only** (autonomous-agent:research-executor): Search, gather, synthesize
   - No planning phase (saves 5-10 minutes)
   - No validation phase (saves 5-10 minutes)
   - Direct search and synthesis

**Time Savings**: 5-15 minutes vs 25-45 minutes for `/research:structured`

## Usage

### Basic Quick Research
```bash
/research:quick "Latest React version"
/research:quick "Python async vs threading"
/research:quick "Best VS Code extensions for Python"
```

### Quick Comparisons
```bash
/research:quick "TypeScript vs JavaScript for new project"
/research:quick "PostgreSQL vs MySQL performance"
/research:quick "REST vs GraphQL quick comparison"
```

### Documentation Lookups
```bash
/research:quick "How to use React useEffect hook"
/research:quick "Docker compose networking setup"
/research:quick "Git rebase vs merge when to use"
```

### Version/Release Checks
```bash
/research:quick "Node.js LTS version 2025"
/research:quick "Latest stable Rust release"
/research:quick "Python 3.12 new features"
```

## Output Format

**Terminal** (10 lines max):
```
[OK] Quick Research: [Topic]

Answer:
[Concise 2-3 sentence answer]

Key Points:
1. [Point 1]
2. [Point 2]
3. [Point 3]

Sources: [2-5 sources]
Time: 45 seconds
```

**No File Report** - Results shown in terminal only for speed

## Comparison with /research:structured

| Feature | /research:quick | /research:structured |
|---------|-----------------|---------------------|
| Planning Phase | ❌ Skipped | ✅ Included |
| Execution | ✅ Direct search | ✅ Systematic search |
| Validation | ❌ Skipped | ✅ Full validation |
| Citations | Basic | Comprehensive |
| Quality Score | No | Yes (0-100) |
| File Report | No | Yes |
| Time | 1-5 min | 20-45 min |
| Best For | Quick answers | Deep research |

## Examples

### Example 1: Version Check
```bash
/research:quick "Latest Next.js version and features"
```

**Output**:
```
[OK] Quick Research: Latest Next.js version

Answer:
Next.js 14.1.0 (released Jan 2025) introduces Turbopack
stable, improved server actions, and partial
prerendering for dynamic routes.

Key Points:
1. Turbopack now stable (5x faster than Webpack)
2. Server Actions enhanced with better error handling
3. Partial Prerendering for hybrid static/dynamic pages

Sources: nextjs.org, vercel.com/blog
Time: 38 seconds
```

### Example 2: Quick Comparison
```bash
/research:quick "Vite vs Webpack for React project 2025"
```

**Output**:
```
[OK] Quick Research: Vite vs Webpack comparison

Answer:
Vite offers faster dev server (instant HMR) and simpler
config, while Webpack provides more plugin ecosystem
and better production optimization control.

Key Points:
1. Vite: Better DX, 10x faster dev server, modern default
2. Webpack: Mature ecosystem, more control, complex config
3. Recommendation: Vite for new projects, Webpack for legacy

Sources: vitejs.dev, webpack.js.org, blog.logrocket.com
Time: 52 seconds
```

### Example 3: How-To Lookup
```bash
/research:quick "How to deploy Next.js to Vercel"
```

**Output**:
```
[OK] Quick Research: Next.js deployment to Vercel

Answer:
Connect GitHub repo to Vercel, configure build settings
(auto-detected for Next.js), deploy with zero config.
Automatic previews for all branches.

Key Points:
1. Push to GitHub → Import to Vercel → Auto-deploy
2. Zero configuration needed (Next.js detected)
3. Environment variables set in Vercel dashboard
4. Custom domains supported with SSL

Sources: vercel.com/docs, nextjs.org/docs/deployment
Time: 41 seconds
```

## Pattern Learning

Quick research patterns are stored separately:
```json
{
  "task_type": "research_quick",
  "topic": "version check",
  "sources_used": ["official_docs", "release_notes"],
  "time_taken": "45s",
  "user_satisfaction": "high"
}
```

Over time, the system learns:
- Which sources work best for quick lookups
- Optimal search query patterns
- Most reliable documentation sites
- Fastest path to accurate answers

## Integration

**Agents Used**:
- autonomous-agent:research-executor (direct execution, no planning/validation)

**Skills Auto-Loaded**:
- research-methodology (search patterns only)

**Pattern Storage**:
- Stores in `.claude-patterns/` for future optimization
- Learns fast-path strategies for similar quick lookups

## Best Practices

**Good Use Cases**:
- ✅ "What is X?"
- ✅ "X vs Y quick comparison"
- ✅ "Latest version of X"
- ✅ "How to do X in Y"
- ✅ "Best practices for X"

**Bad Use Cases** (use `/research:structured` instead):
- ❌ Complex architectural decisions
- ❌ Research requiring citations
- ❌ Professional/academic research
- ❌ Multi-faceted investigations
- ❌ Research needing validation

---

**Version**: 1.0.0
**Integration**: Works with research-executor agent
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: WebSearch, WebFetch tools
