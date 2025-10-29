---
name: workspace:update-about
description: Update GitHub repository About section with current project info and SEO optimization

delegates-to: documentation-generator

# Workspace Update-About Command

## Command: `/workspace:update-about`

**GitHub About section optimization** - Updates the repository's About section (description, topics, website) on GitHub with current project information and optimizes for search and discovery.

**🏷️ About Section Management:**
- **Description Update**: Concise, accurate project description
- **Topic Optimization**: Relevant tags for discoverability
- **Website Link**: Updates project website if available
- **SEO Optimization**: Optimizes for GitHub search
- **Keyword Strategy**: Uses effective keywords
- **Consistency**: Matches README and documentation

## Usage

```bash
# Basic update (analyzes and updates)
/workspace:update-about

# With custom description
/workspace:update-about --description "AI-powered autonomous development plugin for Claude Code"

# Add/update topics
/workspace:update-about --add-topics "ai,automation,claude,agents"

# SEO focus
/workspace:update-about --seo-optimize

# Complete refresh
/workspace:update-about --refresh-all
```

## How It Works

1. **Current State Analysis**
   - Reads current About section via GitHub API
   - Analyzes current description and topics
   - Reviews project for accurate information

2. **Content Generation**
   - Generates concise description (max 350 chars)
   - Identifies relevant topics/tags
   - Optimizes for GitHub search
   - Ensures accuracy and clarity

3. **SEO Optimization**
   - Includes key searchable terms
   - Uses popular relevant topics
   - Balances specificity and discoverability
   - Follows GitHub best practices

4. **Update Execution**
   - Updates via GitHub API (requires token)
   - Validates changes
   - Preserves manual customizations if requested

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️  ABOUT SECTION UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description (Updated):
"Autonomous AI agents for Claude Code with pattern learning,
quality control, and full-stack validation. Zero-config,
intelligent development automation."

Topics (Added 3):
artificial-intelligence, automation, code-quality,
pattern-learning, autonomous-agents, claude-code

SEO Score: 92/100
├─ Keywords: 8 high-value terms ✓
├─ Topic relevance: 95% ✓
└─ Discoverability: High ✓

✓ Updated on GitHub successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Requirements

- GitHub personal access token with repo permissions
- Set in environment variable: `GITHUB_TOKEN`
- Repository must be on GitHub (GitLab support coming)

## Best Practices

### Description Guidelines
- Keep under 350 characters
- Lead with main benefit/purpose
- Include key features/differentiators
- Use searchable keywords naturally
- Avoid jargon unless necessary

### Topic Selection
- Use 5-10 relevant topics
- Mix general and specific terms
- Include language/framework tags
- Add domain-specific terms
- Check GitHub's suggested topics

### SEO Optimization
- Include primary keywords in description
- Use popular, relevant topics
- Match common search terms
- Balance specificity and breadth
- Monitor GitHub search results

---

**Version**: 1.0.0
**Delegates-to**: documentation-generator agent
**Requires**: GitHub API access (GITHUB_TOKEN)
**Platform**: GitHub (GitLab support planned)
**SEO**: Optimized for GitHub discovery
