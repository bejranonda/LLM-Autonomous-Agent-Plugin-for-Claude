# Migration Guide: v7.16.5 → v7.17.0

**Date**: 2025-11-20
**Version**: 7.17.0
**Breaking Changes**: Research commands removed

---

## What Changed

### Removed Components

**Commands** (3 removed):
- ❌ `/research:structured` - Comprehensive multi-step research
- ❌ `/research:compare` - A vs B comparison research
- ❌ `/research:quick` - Fast web search with synthesis

**Agents** (3 removed):
- ❌ `research-strategist` - Research planning agent
- ❌ `research-executor` - Research analysis agent
- ❌ `research-validator` - Research quality validation agent

**Skills** (2 removed):
- ❌ `research-methodology` - Research techniques and best practices
- ❌ `source-verification` - Citation validation and source credibility

---

## Why Were Research Commands Removed?

### Primary Reason: High Token Cost

Even with v2.1.0 optimizations, research commands consumed significant tokens:

| Command | Token Cost | Time |
|---------|------------|------|
| `/research:structured` | 0-33k agent tokens + WebFetch | 15-30 min |
| `/research:compare` | 0-12k agent tokens + WebFetch | 8-15 min |
| `/research:quick` | 0 agent tokens + WebFetch | 1-5 min |

**WebFetch costs** (main token consumer):
- Fetching 15-25 web pages with content extraction
- Each page: 500-2000 tokens depending on content
- Total WebFetch: 7.5k-50k tokens per research task

**Total cost per structured research**: 10k-80k+ tokens

### Secondary Reasons

1. **Not core functionality** - This plugin focuses on code analysis, quality control, and autonomous development
2. **Better alternatives exist** - Manual exploration with Claude Code's native WebSearch is more flexible
3. **User feedback** - High token consumption was a concern
4. **Maintenance burden** - Research commands required significant upkeep

---

## How to Do Research Without These Commands

### Option 1: Use Claude Code WebSearch Directly (Recommended)

**Just ask questions naturally** - Claude Code will use WebSearch when appropriate:

```
User: "What's the latest React version and what are the new features?"

Claude: I'll search for that information.
[Uses WebSearch tool automatically]
[Analyzes results and presents findings]
```

**Benefits**:
- More flexible and conversational
- Claude decides when to search vs use knowledge
- Can iterate based on your follow-up questions
- You control token usage by depth of exploration

### Option 2: Manual Iterative Research

**Step-by-step approach**:

1. **Ask for search queries**:
   ```
   User: "I need to research React vs Vue. What should I search for?"
   Claude: Here are targeted search queries: [provides 5-8 queries]
   ```

2. **Search manually or ask Claude**:
   ```
   User: "Search for 'React vs Vue performance 2025'"
   Claude: [Uses WebSearch, shows top results]
   ```

3. **Explore specific results**:
   ```
   User: "Fetch the first result and summarize"
   Claude: [Uses WebFetch, provides summary]
   ```

4. **Iterate and refine**:
   ```
   User: "Based on that, what else should I look into?"
   Claude: [Suggests refined searches]
   ```

**Benefits**:
- Full control over token usage
- Can stop when you have enough info
- More engaging and educational
- Cheaper overall

### Option 3: External Research Tools

For comprehensive research needs:

- **Perplexity AI** - Excellent for research with citations
- **ChatGPT** (with browsing) - Good for multi-step research
- **Google Scholar** - For academic research
- **GitHub Copilot** - For code-related research

Then bring findings back to Claude Code for implementation.

---

## Impact on Existing Workflows

### If You Used `/research:structured`

**Before**:
```bash
/research:structured "Compare authentication libraries for Node.js"
# Waited 20-30 minutes
# Got comprehensive report
```

**After**:
```
User: "I need to compare authentication libraries for Node.js. Can you help me research this?"

Claude: I'll help you research authentication libraries for Node.js. Let me search for current options and comparisons.
[Searches, analyzes, presents findings]

User: "Tell me more about Passport.js vs Auth0"

Claude: [Searches specific comparison, provides detailed analysis]

User: "Which would you recommend for my Express app?"

Claude: Based on your requirements... [provides recommendation]
```

**Token savings**: 20-50k tokens (you control depth)

### If You Used `/research:compare`

**Before**:
```bash
/research:compare "TypeScript vs JavaScript for new project"
# 8-15 minutes
# Decision matrix with scores
```

**After**:
```
User: "Should I use TypeScript or JavaScript for my new project? It's a React web app."

Claude: Let me search for current comparisons and best practices.
[Searches, analyzes context]

Based on the search results and your project type (React web app), here's my analysis:

**TypeScript Advantages**:
- Better IDE support and autocomplete
- Catch errors before runtime
- Easier refactoring for growing codebases

**JavaScript Advantages**:
- Faster initial setup
- No build step required
- Smaller bundle sizes

**Recommendation**: TypeScript, because...
```

**Token savings**: 10-20k tokens

### If You Used `/research:quick`

**Before**:
```bash
/research:quick "Latest Next.js version"
# 1-5 minutes
# Quick answer with sources
```

**After**:
```
User: "What's the latest Next.js version?"

Claude: [Searches automatically]
The latest Next.js version is 15.1.0 (released January 2025). Key new features include...
```

**No change in experience**, actually simpler!

---

## Updated Plugin Focus (v7.17.0)

The plugin now focuses exclusively on its core strengths:

### Code Quality & Analysis
- ✅ `/analyze:project` - Project-wide analysis
- ✅ `/analyze:quality` - Quality control with auto-fix
- ✅ `/analyze:static` - 40+ linter integration
- ✅ `/analyze:dependencies` - CVE vulnerability scanning

### Development Workflows
- ✅ `/dev:auto` - Autonomous development
- ✅ `/dev:commit` - Intelligent commit management
- ✅ `/dev:release` - Automated release workflow
- ✅ `/dev:pr-review` - PR review with auto-fix

### Validation & Testing
- ✅ `/validate:fullstack` - Full-stack validation
- ✅ `/validate:web` - Web page validation
- ✅ `/validate:plugin` - Plugin validation
- ✅ `/validate:all` - Comprehensive audit

### Learning & Monitoring
- ✅ `/learn:init` - Initialize pattern learning
- ✅ `/learn:performance` - Performance analytics
- ✅ `/monitor:dashboard` - Real-time monitoring

### Workspace Management
- ✅ `/workspace:organize` - File organization
- ✅ `/workspace:update-readme` - Smart README updates
- ✅ `/workspace:reports` - Report management

---

## Benefits of Removal

1. **Lower token costs** - Research was the highest token consumer
2. **Simpler plugin** - Easier to maintain and understand
3. **Better user experience** - Natural conversation > slash commands
4. **Focused purpose** - Core autonomous development features
5. **More flexible** - Users control research depth and tokens

---

## Frequently Asked Questions

### Q: Can I still use WebSearch in Claude Code?
**A**: Yes! WebSearch is a built-in Claude Code feature. Just ask questions naturally, and Claude will search when needed.

### Q: Will research commands come back?
**A**: Unlikely. The token cost vs benefit ratio wasn't favorable. Manual research with Claude is more flexible and cost-effective.

### Q: What if I need comprehensive research?
**A**: Use external tools (Perplexity, ChatGPT with browsing) for research, then bring findings to Claude Code for implementation.

### Q: Can I create my own research command?
**A**: Yes! You can create custom slash commands. See the [plugin documentation](https://docs.anthropic.com/claude/docs/claude-code-plugins) for details.

### Q: Will this affect pattern learning?
**A**: No. Pattern learning, skill selection, and autonomous behavior are unchanged.

---

## Version History

- **v7.16.5** - Research commands with v2.1.0 optimizations (70-90% token reduction)
- **v7.17.0** - Research commands removed, plugin refocused on core development features

---

## Summary

**What you lose**:
- 3 specialized research commands
- Automated research workflows
- Research-specific agents and skills

**What you gain**:
- Significantly lower token costs
- More flexible conversational research
- Simpler, more focused plugin
- Better control over research depth

**Bottom line**: Research is still possible (and often better) through natural conversation with Claude Code. The removal simplifies the plugin and reduces token usage while maintaining functionality through a more flexible approach.

---

**Questions or concerns?**
- Open an issue: https://github.com/anthropics/claude-code/issues
- Plugin repo: [Your plugin repository URL]

**Version**: 7.17.0
**Date**: 2025-11-20
**Migration Status**: ✅ Complete - No action required from users
