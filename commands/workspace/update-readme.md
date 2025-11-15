---
name: workspace:update-readme
description: Smart README update that learns your style and reflects current project state
delegates-to: autonomous-agent:documentation-generator
---

# Workspace Update-README Command

## Command: `/autonomous-agent:workspace:update-readme`

**Intelligent README maintenance** - Analyzes current README to understand its style, structure, and content approach, then intelligently updates it based on project changes while preserving the established voice and organization.

**📝 Smart README Updates:**
- **Style Learning**: Understands current writing style and tone
- **Structure Preservation**: Maintains existing section organization
- **Content Synchronization**: Updates content to match current project state
- **User Feedback Integration**: Incorporates user suggestions
- **SEO Optimization**: Optimizes for GitHub search and discovery
- **Quality Maintenance**: Ensures clarity and completeness

## Usage

```bash
# Basic update (preserve style and structure)
/autonomous-agent:workspace:update-readme

# With user suggestions
/autonomous-agent:workspace:update-readme --suggestions "add installation video, improve examples"

# Change structure
/autonomous-agent:workspace:update-readme --restructure "move installation first, add troubleshooting section"

# Update specific sections only
/autonomous-agent:workspace:update-readme --sections "features,usage,examples"

# Complete rewrite (keep data, new style)
/autonomous-agent:workspace:update-readme --rewrite --style "concise and technical"
```

## How It Works

1. **Current README Analysis**
   - Analyzes existing style (formal, casual, technical, etc.)
   - Maps current structure and section organization
   - Identifies content patterns and conventions
   - Notes tone, voice, and audience level

2. **Project State Analysis**
   - Scans project for new features
   - Identifies changed functionality
   - Checks for outdated information
   - Reviews code comments and docstrings

3. **Update Strategy**
   - Plans sections to update
   - Determines what to add/remove/modify
   - Preserves user-provided style choices
   - Integrates user suggestions

4. **Implementation**
   - Updates content while maintaining style
   - Preserves formatting and structure
   - Adds new sections if needed
   - Validates links and examples

5. **Quality Check**
   - Verifies all links work
   - Tests code examples
   - Checks formatting
   - Validates completeness

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 README UPDATE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Style Preserved: Professional with examples
Structure: Maintained (8 sections)

Changes Made:
* Updated features list (+3 new features)
* Refreshed usage examples
* Added 2 new troubleshooting items
* Updated installation instructions

Quality: 94/100
+- All links verified [PASS]
+- Code examples tested [PASS]
+- Formatting consistent [PASS]

📄 Updated: README.md
⏱ Completed in 45 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration with Learning

Learns README patterns:
- Effective structures for project types
- Successful writing styles
- Common section organizations
- User preferences

---

**Version**: 1.0.0
**Delegates-to**: documentation-generator agent
**Preserves**: Style, tone, structure (unless told otherwise)
**Updates**: Content, examples, links, accuracy
