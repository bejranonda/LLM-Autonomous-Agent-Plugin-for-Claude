# 🚨 EMERGENCY COMMAND RESPONSE TEMPLATE

**INSTRUCTIONS**: Add this template to the TOP of any slash command file that is generating empty text blocks.

---

## 🚨 CRITICAL: RESPONSE SAFETY REQUIREMENTS

**SYSTEM-WIDE FAILURE PREVENTION**: When generating ANY response content for this command, you MUST ensure:

1. **NEVER generate empty text blocks** - All content blocks must have non-empty text
2. **NEVER use Unicode box characters** (═, ║, ╔, ╗, ┌, ┐, └, ┘, │, ─) - Use safe ASCII alternatives
3. **ALWAYS provide fallback content** for any section that might be empty
4. **VALIDATE all content blocks** before finalizing response
5. **NEVER leave sections empty** - Provide default values for missing data
6. **ENSURE ALL arrays and lists have content** - Never return empty lists/arrays

**SAFE RESPONSE PATTERN**:
- Use ASCII characters: `+`, `-`, `|`, `=` instead of Unicode box drawing
- Ensure every section has meaningful content
- Provide default values for missing data
- Include fallback text for empty results
- Always include actionable next steps

**RESPONSE VALIDATION CHECKLIST**:
- [ ] No content blocks have empty or whitespace-only text
- [ ] No Unicode box characters in response
- [ ] All sections have actual content
- [ ] Lists/arrays are not empty (provide default items)
- [ ] Scores/numbers have actual values (use 0 as default)
- [ ] Recommendations are included even if basic

**CRITICAL FAILURE EXAMPLES TO AVOID**:
```json
{
  "content": [
    {"type": "text", "text": ""},           // ❌ EMPTY TEXT BLOCK
    {"type": "text", "text": "   "},        // ❌ WHITESPACE ONLY
    {"type": "text", "text": "═══"}         // ❌ UNICODE CHARACTERS
  ]
}
```

**SAFE RESPONSE EXAMPLES**:
```json
{
  "content": [
    {"type": "text", "text": "Results:"},    // ✅ NON-EMPTY TEXT
    {"type": "text", "text": "+ Section content"} // ✅ ASCII CHARACTERS
  ]
}
```

**FAILURE TO COMPLY**: Will cause `cache_control cannot be set for empty text blocks` errors and break ALL Claude functionality for the user.

---

## How to Apply This Template

1. **Copy the entire template above**
2. **Paste it immediately after the `---` YAML frontmatter** in any command file
3. **Customize the specific safety requirements** for that command
4. **Test the command to ensure no empty text blocks are generated**

**Commands Known to Need This Fix**:
- `/learn:init` - Fixed
- `/analyze:quality` - Fixed
- Any command with complex output formatting
- Commands with Unicode box characters
- Commands that might return empty results

---

**Status**: EMERGENCY FIX - PREVENTS SYSTEM-WIDE CLAUDE FAILURE
**Impact**: CRITICAL - Restores plugin functionality for all users