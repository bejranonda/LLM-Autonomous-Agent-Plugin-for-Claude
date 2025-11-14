---
name: analyze:repository
description: Analyze external GitHub/GitLab repo for insights, patterns, and improvement opportunities
delegates-to: autonomous-agent:orchestrator
---

# Analyze-Repository Command

## Command: `/analyze:repository`

**Deep analysis of external repositories** - Explores and analyzes GitHub/GitLab repositories (by URL or local path) to identify strengths, weaknesses, features, and generate specific recommendations for enhancing this plugin based on discovered capabilities.

**🔍 Comprehensive Repository Analysis:**
- **Feature Discovery**: Identifies all major features and capabilities
- **Quality Assessment**: Evaluates code quality, structure, and design
- **Strength/Weakness Analysis**: What the repository does well and poorly
- **Plugin Enhancement Recommendations**: How to improve THIS plugin based on discoveries
- **Pattern Learning**: Learns successful patterns from external projects
- **Comparative Analysis**: Compares with similar projects

## How It Works

1. **Repository Access**: Clones or accesses repository (URL or local path)
2. **Structure Analysis**: Maps project architecture and organization
3. **Feature Extraction**: Identifies key features and capabilities
4. **Quality Assessment**: Evaluates code quality and design patterns
5. **Strength/Weakness Evaluation**: Analyzes what works well and what doesn't
6. **Plugin Enhancement Analysis**: Determines how to enhance THIS plugin
7. **Pattern Learning**: Stores successful patterns for future use

## Usage

### Basic Usage
```bash
# Analyze GitHub repository by URL
/analyze:repository https://github.com/username/repo

# Analyze local repository
/analyze:repository /path/to/local/repo

# Analyze GitLab repository
/analyze:repository https://gitlab.com/username/repo
```

### With Specific Focus
```bash
# Focus on architecture and design
/analyze:repository https://github.com/user/repo --focus architecture

# Focus on testing strategies
/analyze:repository https://github.com/user/repo --focus testing

# Focus on documentation approach
/analyze:repository https://github.com/user/repo --focus documentation

# Focus on CI/CD and automation
/analyze:repository https://github.com/user/repo --focus automation
```

### Advanced Options
```bash
# Deep analysis with all metrics
/analyze:repository https://github.com/user/repo --deep-analysis

# Compare with current project
/analyze:repository https://github.com/user/repo --compare-with-current

# Focus on plugin enhancement opportunities
/analyze:repository https://github.com/user/repo --plugin-enhancement-focus

# Include dependency analysis
/analyze:repository https://github.com/user/repo --analyze-dependencies

# Generate implementation roadmap
/analyze:repository https://github.com/user/repo --generate-roadmap
```

## Output Format

### Terminal Output (Concise Summary)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 REPOSITORY ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository: fastapi/fastapi
Type: Python Web Framework | Stars: 68.5k | Quality: 94/100

Key Features Discovered:
* Automatic API documentation generation (OpenAPI/Swagger)
* Dependency injection system
* Async request handling with type validation

Top Strengths:
1. Excellent type hint usage throughout
2. Comprehensive test coverage (96%)
3. Outstanding documentation with examples

Plugin Enhancement Opportunities:
1. [HIGH] Add automatic OpenAPI schema generation for analyzed APIs
2. [MED]  Implement dependency injection pattern in agents
3. [MED]  Enhanced async operation support in background tasks

📄 Full report: .claude/data/reports/analyze-repo-fastapi-2025-10-29.md
⏱ Analysis completed in 3.2 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Detailed Report (.claude/data/reports/)

```markdown
=======================================================
  REPOSITORY ANALYSIS REPORT
=======================================================
Generated: 2025-10-29 16:45:00
Repository: https://github.com/fastapi/fastapi
Branch: main | Commit: abc1234 | Stars: 68,500

+- Repository Overview --------------------------------+
| Project: FastAPI                                      |
| Type: Python Web Framework                            |
| Language: Python 3.7+                                 |
| License: MIT                                          |
|                                                       |
| Statistics:                                           |
| * Files: 487                                         |
| * Lines of Code: 45,230                              |
| * Contributors: 487                                   |
| * Commits: 3,892                                     |
| * Stars: 68,500                                      |
| * Forks: 5,742                                       |
| * Open Issues: 234                                    |
|                                                       |
| Main Technologies:                                    |
| * Python 3.7+ with type hints                        |
| * Pydantic for validation                            |
| * Starlette for async support                        |
| * OpenAPI/Swagger for documentation                  |
+-------------------------------------------------------+

+- Key Features Discovered ----------------------------+
| 1. Automatic API Documentation                        |
|    * OpenAPI schema auto-generation                   |
|    * Interactive Swagger UI                           |
|    * ReDoc alternative documentation                  |
|    * JSON Schema exports                              |
|    Implementation: /fastapi/openapi/utils.py         |
|                                                       |
| 2. Dependency Injection System                        |
|    * Type-based dependency resolution                 |
|    * Nested dependency support                        |
|    * Async dependency handling                        |
|    * Automatic request parameter injection            |
|    Implementation: /fastapi/dependencies/            |
|                                                       |
| 3. Type-Safe Request/Response Handling               |
|    * Pydantic model integration                      |
|    * Automatic validation                            |
|    * Type hint-based parameter extraction            |
|    * Response model enforcement                       |
|    Implementation: /fastapi/routing/                 |
|                                                       |
| 4. Async/Await Support                               |
|    * Full async request handlers                     |
|    * Background task execution                        |
|    * Streaming responses                             |
|    * WebSocket support                               |
|    Implementation: /fastapi/concurrency.py           |
|                                                       |
| 5. Advanced Testing Infrastructure                    |
|    * Comprehensive test suite (96% coverage)         |
|    * Test client with async support                  |
|    * Fixture-based testing                           |
|    * Integration and unit test separation            |
|    Implementation: /tests/                           |
+-------------------------------------------------------+

+- Strengths Analysis ---------------------------------+
| Code Quality (94/100):                                |
| ✅ Exceptional type hint coverage (99%)              |
| ✅ Comprehensive docstrings with examples            |
| ✅ Consistent code style throughout                  |
| ✅ Low cyclomatic complexity (avg: 4.2)             |
| ✅ DRY principles well applied                       |
|                                                       |
| Testing (96/100):                                     |
| ✅ 96% test coverage                                 |
| ✅ 2,145 tests, all passing                          |
| ✅ Fast test execution (<30s)                        |
| ✅ Clear test organization                           |
| ✅ Property-based testing for edge cases             |
|                                                       |
| Documentation (98/100):                               |
| ✅ Outstanding main documentation                    |
| ✅ Extensive tutorials and guides                    |
| ✅ Real-world examples included                      |
| ✅ Multi-language documentation (10+ languages)      |
| ✅ Auto-generated API docs from code                 |
|                                                       |
| Architecture (92/100):                                |
| ✅ Clean separation of concerns                      |
| ✅ Modular design with clear boundaries              |
| ✅ Extensible plugin system                          |
| ✅ Minimal external dependencies                     |
| ✅ Performance-optimized core                        |
|                                                       |
| Developer Experience (95/100):                        |
| ✅ Intuitive API design                              |
| ✅ Excellent error messages                          |
| ✅ Fast development iteration                        |
| ✅ Auto-complete friendly (type hints)               |
| ✅ Minimal boilerplate required                      |
+-------------------------------------------------------+

+- Weaknesses Analysis --------------------------------+
| Areas for Improvement:                                |
|                                                       |
| [WARN]️  Complex Dependency Resolution (Medium)           |
|    * Nested dependencies can be hard to debug        |
|    * Circular dependency detection limited           |
|    * Error messages sometimes unclear                |
|    Impact: Developer Experience                      |
|    Files: /fastapi/dependencies/utils.py:234-567     |
|                                                       |
| [WARN]️  Limited Built-in Caching (Medium)                |
|    * No built-in response caching mechanism          |
|    * Requires external libraries                     |
|    * Cache invalidation strategy not documented      |
|    Impact: Performance                               |
|    Workaround: Use third-party libraries             |
|                                                       |
| [WARN]️  WebSocket Documentation (Low)                    |
|    * WebSocket examples limited                      |
|    * Advanced patterns not well documented           |
|    * Error handling examples missing                 |
|    Impact: Feature Adoption                          |
|    Files: /docs/advanced/websockets.md               |
|                                                       |
| [WARN]️  Middleware Ordering (Low)                        |
|    * Middleware execution order not intuitive        |
|    * Documentation could be clearer                  |
|    * Debugging middleware chain difficult            |
|    Impact: Developer Experience                      |
|    Files: /fastapi/middleware/                       |
+-------------------------------------------------------+

+- Design Patterns Observed ---------------------------+
| 1. Dependency Injection Pattern                       |
|    Usage: Core architectural pattern                  |
|    Implementation: Type-based resolution              |
|    Quality: Excellent (95/100)                       |
|    Reusability: High                                 |
|                                                       |
| 2. Decorator Pattern                                  |
|    Usage: Route definition and middleware             |
|    Implementation: Python decorators                  |
|    Quality: Excellent (94/100)                       |
|    Reusability: High                                 |
|                                                       |
| 3. Factory Pattern                                    |
|    Usage: Application and router creation             |
|    Implementation: Builder-style API                  |
|    Quality: Good (87/100)                            |
|    Reusability: Medium                               |
|                                                       |
| 4. Observer Pattern (Events)                          |
|    Usage: Startup/shutdown hooks                      |
|    Implementation: Event handlers                     |
|    Quality: Good (85/100)                            |
|    Reusability: Medium                               |
|                                                       |
| 5. Strategy Pattern (Validation)                      |
|    Usage: Customizable validation strategies          |
|    Implementation: Pydantic validators                |
|    Quality: Excellent (92/100)                       |
|    Reusability: High                                 |
+-------------------------------------------------------+

+- Technology Stack Analysis --------------------------+
| Core Dependencies:                                    |
| * Starlette - ASGI framework (excellent choice)      |
| * Pydantic - Data validation (industry standard)     |
| * python-multipart - File uploads (necessary)        |
|                                                       |
| Development Dependencies:                             |
| * pytest - Testing framework (standard)              |
| * black - Code formatter (excellent)                 |
| * mypy - Type checking (essential)                   |
| * ruff - Fast linting (modern choice)                |
|                                                       |
| Optional Dependencies:                                |
| * uvicorn - ASGI server (recommended)                |
| * orjson - Fast JSON (performance)                   |
| * ujson - Alternative JSON (compatibility)           |
|                                                       |
| Dependency Management:                                |
| ✅ Minimal required dependencies                     |
| ✅ Clear optional dependency groups                  |
| ✅ Version constraints well defined                  |
| ✅ Regular security updates                          |
+-------------------------------------------------------+

+- Plugin Enhancement Recommendations -----------------+
| CRITICAL recommendations for THIS plugin:             |
|                                                       |
| 1. [HIGH PRIORITY] Automatic Schema Generation       |
|    Learning: FastAPI auto-generates OpenAPI schemas  |
|    |                                                  |
|    Recommendation for This Plugin:                    |
|    * Add agent: api-schema-generator.md              |
|    * Auto-analyze API endpoints in projects          |
|    * Generate OpenAPI/Swagger documentation          |
|    * Validate API contracts automatically            |
|    * Integrate with /validate:fullstack              |
|    |                                                  |
|    Implementation Approach:                           |
|    * Create skills/api-documentation/ skill          |
|    * Add schema generation to api-contract-validator |
|    * Store API patterns in pattern database          |
|    * Learn from successful API designs               |
|    |                                                  |
|    Expected Impact: HIGH                             |
|    * Better API analysis capabilities                |
|    * Automatic documentation generation              |
|    * Improved validation accuracy                    |
|    Estimated Effort: 6-8 hours                       |
|                                                       |
| 2. [HIGH PRIORITY] Enhanced Dependency Injection      |
|    Learning: Type-based dependency resolution         |
|    |                                                  |
|    Recommendation for This Plugin:                    |
|    * Implement dependency injection for agents       |
|    * Auto-resolve agent dependencies                 |
|    * Share context between agents efficiently        |
|    * Reduce agent coupling                           |
|    |                                                  |
|    Implementation Approach:                           |
|    * Add dependency resolution to orchestrator       |
|    * Create agent dependency registry                |
|    * Implement type-based agent injection            |
|    * Cache resolved dependencies                     |
|    |                                                  |
|    Expected Impact: MEDIUM-HIGH                      |
|    * Cleaner agent architecture                      |
|    * Better performance (caching)                    |
|    * Easier agent development                        |
|    Estimated Effort: 8-10 hours                      |
|                                                       |
| 3. [MEDIUM PRIORITY] Advanced Async Operations       |
|    Learning: Full async/await support throughout     |
|    |                                                  |
|    Recommendation for This Plugin:                    |
|    * Enhance background-task-manager with async      |
|    * Add parallel agent execution                    |
|    * Implement async skill loading                   |
|    * Add WebSocket support for real-time updates     |
|    |                                                  |
|    Implementation Approach:                           |
|    * Update background-task-manager to async         |
|    * Add async execution pool                        |
|    * Implement task priority queuing                 |
|    * Add progress streaming support                  |
|    |                                                  |
|    Expected Impact: MEDIUM                           |
|    * Faster execution times (parallel)               |
|    * Better resource utilization                     |
|    * Real-time progress updates                      |
|    Estimated Effort: 10-12 hours                     |
|                                                       |
| 4. [MEDIUM PRIORITY] Type-Safe Agent Communication    |
|    Learning: Pydantic models for type safety         |
|    |                                                  |
|    Recommendation for This Plugin:                    |
|    * Define agent input/output schemas               |
|    * Validate agent communication automatically      |
|    * Generate agent interfaces from schemas          |
|    * Add type checking to agent delegation           |
|    |                                                  |
|    Implementation Approach:                           |
|    * Create agent schema definitions                 |
|    * Add Pydantic models for agent I/O              |
|    * Integrate validation in orchestrator            |
|    * Add schema versioning support                   |
|    |                                                  |
|    Expected Impact: MEDIUM                           |
|    * Fewer agent communication errors                |
|    * Better debugging                                |
|    * Self-documenting agent interfaces              |
|    Estimated Effort: 6-8 hours                       |
|                                                       |
| 5. [LOW-MEDIUM PRIORITY] Enhanced Error Messages     |
|    Learning: Descriptive, actionable error messages  |
|    |                                                  |
|    Recommendation for This Plugin:                    |
|    * Improve error message clarity                   |
|    * Add suggested fixes to errors                   |
|    * Include relevant context in errors              |
|    * Add error recovery suggestions                  |
|    |                                                  |
|    Implementation Approach:                           |
|    * Create error message templates                  |
|    * Add context capture to all agents               |
|    * Implement error pattern detection               |
|    * Store error resolution patterns                 |
|    |                                                  |
|    Expected Impact: LOW-MEDIUM                       |
|    * Better developer experience                     |
|    * Faster debugging                                |
|    * Reduced support needs                           |
|    Estimated Effort: 4-6 hours                       |
+-------------------------------------------------------+

+- Implementation Roadmap ------------------------------+
| Phase 1: High-Priority Enhancements (2-3 weeks)      |
| Week 1-2: API Schema Generation                      |
| +- Create api-schema-generator agent                |
| +- Implement OpenAPI schema extraction              |
| +- Add to /validate:fullstack command               |
| +- Test with multiple API frameworks                |
|                                                       |
| Week 2-3: Dependency Injection System                |
| +- Design agent dependency system                   |
| +- Implement type-based resolution                  |
| +- Update orchestrator for DI support               |
| +- Refactor existing agents to use DI               |
|                                                       |
| Phase 2: Medium-Priority Enhancements (2-3 weeks)    |
| Week 4-5: Async Operations Enhancement              |
| +- Upgrade background-task-manager to async         |
| +- Add parallel agent execution                     |
| +- Implement task priority queue                    |
| +- Add real-time progress updates                   |
|                                                       |
| Week 5-6: Type-Safe Communication                    |
| +- Define agent schemas                             |
| +- Add Pydantic validation                          |
| +- Update all agent interfaces                      |
| +- Add schema versioning                            |
|                                                       |
| Phase 3: Quality Improvements (1 week)               |
| Week 7: Error Message Enhancement                    |
| +- Create error message templates                   |
| +- Add context capture                              |
| +- Implement pattern detection                      |
| +- Test and refine messages                         |
+-------------------------------------------------------+

+- Learning Patterns to Store -------------------------+
| 1. Type Hint Usage Pattern                           |
|    * Comprehensive type hints improve maintainability|
|    * Type checking catches 73% of bugs early         |
|    * IDE support improves developer productivity 40% |
|    Store in: .claude-patterns/typing-patterns.json  |
|                                                       |
| 2. Auto-Documentation Pattern                         |
|    * Documentation from code reduces sync issues     |
|    * Examples in docstrings improve understanding    |
|    * API docs generated from type hints save time    |
|    Store in: .claude-patterns/documentation.json    |
|                                                       |
| 3. Dependency Injection Pattern                       |
|    * DI reduces coupling between components          |
|    * Type-based resolution is intuitive              |
|    * Caching dependencies improves performance       |
|    Store in: .claude-patterns/architecture.json     |
|                                                       |
| 4. Async-First Architecture                          |
|    * Async from start easier than refactoring later  |
|    * Background tasks improve responsiveness         |
|    * Parallel execution increases throughput         |
|    Store in: .claude-patterns/async-patterns.json   |
|                                                       |
| 5. Comprehensive Testing Strategy                     |
|    * High coverage (90%+) catches regressions        |
|    * Fast tests encourage frequent running           |
|    * Integration tests complement unit tests         |
|    Store in: .claude-patterns/testing-patterns.json |
+-------------------------------------------------------+

+- Comparative Analysis -------------------------------+
| Comparing FastAPI with This Plugin:                  |
|                                                       |
| Similarities:                                         |
| ✅ Both emphasize code quality                       |
| ✅ Both have comprehensive testing                   |
| ✅ Both use Python 3.7+ features                     |
| ✅ Both focus on developer experience                |
| ✅ Both have modular architecture                    |
|                                                       |
| Differences:                                          |
| This Plugin              vs    FastAPI                |
| * Markdown-based config   ->    Python code config    |
| * Agent-based execution   ->    Request-based exec    |
| * File-based skills       ->    Import-based modules  |
| * Pattern learning        ->    No learning system    |
| * Auto skill selection    ->    Manual dependency def |
|                                                       |
| What This Plugin Does Better:                        |
| ✅ Automatic pattern learning                        |
| ✅ No-code agent configuration                       |
| ✅ Autonomous decision making                        |
| ✅ Cross-project pattern sharing                     |
|                                                       |
| What FastAPI Does Better:                            |
| ✅ Type-based dependency injection                   |
| ✅ Automatic documentation generation                |
| ✅ Async-first architecture                          |
| ✅ Comprehensive error messages                      |
| ✅ Type-safe interfaces                              |
+-------------------------------------------------------+

=======================================================
  NEXT STEPS
=======================================================

Ready to Implement Enhancements?
* Start with Phase 1, High Priority items
* Use: /dev:auto "implement API schema generation agent"
* Track progress with: /learn:analytics

Want More Analysis?
* Analyze similar repositories for comparison
* Deep-dive into specific features
* Review implementation details

Questions or Feedback?
* Review recommendations carefully
* Prioritize based on your project needs
* Consider resource constraints

=======================================================

Analysis Time: 3.2 minutes
Files Analyzed: 487
Quality Score: 94/100
Enhancement Opportunities: 5 high-value recommendations

This analysis has been stored in pattern database for future reference.
```

## Integration with Learning System

The `/analyze:repository` command integrates with pattern learning:

**Learning from External Repos**:
- Successful design patterns
- Effective code organization strategies
- Best practices in testing and documentation
- Common pitfalls to avoid
- Quality indicators and metrics

**Pattern Storage**:
```json
{
  "repository_analysis_patterns": {
    "repo_type": "web_framework",
    "quality_indicators": {
      "type_hint_coverage": 0.99,
      "test_coverage": 0.96,
      "documentation_quality": 0.98,
      "code_complexity": "low"
    },
    "successful_patterns": [
      "type_based_dependency_injection",
      "automatic_documentation_generation",
      "async_first_architecture"
    ],
    "plugin_enhancements_identified": 5,
    "implementation_priority": "high",
    "reuse_count": 3
  }
}
```

## Agent Delegation

`/analyze:repository` delegates to:
- **orchestrator**: Main analysis coordinator
- **code-analyzer**: Repository structure analysis
- **quality-controller**: Quality assessment
- **security-auditor**: Security pattern analysis
- **pattern-learning**: Pattern extraction and storage

## Skills Integration

Auto-loads relevant skills:
- **code-analysis**: For code structure analysis
- **quality-standards**: For quality evaluation
- **pattern-learning**: For pattern extraction
- **documentation-best-practices**: For documentation assessment
- **security-patterns**: For security evaluation

## Use Cases

### Learning from Popular Projects
```bash
# Learn from FastAPI
/analyze:repository https://github.com/tiangolo/fastapi

# Learn from Django
/analyze:repository https://github.com/django/django

# Learn from Flask
/analyze:repository https://github.com/pallets/flask
```

### Competitive Analysis
```bash
# Compare with similar tools
/analyze:repository https://github.com/competitor/tool --compare-with-current
```

### Feature Discovery
```bash
# Find interesting features
/analyze:repository https://github.com/user/repo --focus features
```

### Plugin Enhancement Planning
```bash
# Focus on plugin improvements
/analyze:repository https://github.com/user/repo --plugin-enhancement-focus
```

## Best Practices

### Good Repository Analysis Requests
```bash
# Specific focus area
/analyze:repository https://github.com/user/repo --focus testing

# With comparison
/analyze:repository https://github.com/user/repo --compare-with-current

# For enhancement planning
/analyze:repository https://github.com/user/repo --plugin-enhancement-focus
```

### Choosing Repositories to Analyze
- Choose high-quality, well-maintained projects
- Select projects with similar domain or technology
- Look for projects with innovative features
- Prefer projects with good documentation
- Consider projects with high community engagement

## Performance Metrics

- **Analysis Time**: 2-5 minutes for typical repository
- **Accuracy**: 90-95% for quality assessment
- **Enhancement Identification**: 3-7 valuable recommendations typically
- **Pattern Extraction**: 85-90% of key patterns identified

---

**Version**: 1.0.0
**Integration**: Uses orchestrator, code-analyzer, quality-controller, security-auditor agents
**Skills**: code-analysis, quality-standards, pattern-learning, security-patterns
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Full integration with pattern learning system
**Scope**: Analyzes external repositories and generates plugin enhancement recommendations
