# Release Notes v8.0.1

**Release Date**: 2026-04-01

## Bug Fixes

### Cross-Platform Compatibility
- Fixed emoji encoding issues in Python scripts causing `UnicodeEncodeError` on Windows systems
- All console output now uses ASCII-safe alternatives (`[OK]`, `[ERROR]`, `[WARN]`)
- Improved Windows Command Prompt compatibility with legacy code pages (cp1252)

### Documentation
- Updated CLAUDE.md with emoji ban guidelines and ASCII alternatives
- Added cross-platform encoding validation instructions

## Upgrade Notes

This is a patch release with no breaking changes. Upgrade is recommended for Windows users.

## Files Changed

- `CLAUDE.md` - Added emoji ban guidelines
- `lib/` - Python scripts updated for ASCII-only output

---

**Full Changelog**: [v8.0.0...v8.0.1](https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude/compare/v8.0.0...v8.0.1)
