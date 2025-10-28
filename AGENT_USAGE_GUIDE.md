# Agent Usage Guide
## Autonomous Agent Plugin for Claude Code

**Version**: 5.3.3
**Updated**: 2025-10-28
**Purpose**: Guide for selecting and using specialized agents effectively

---

## 🚀 Quick Start

### For Most Tasks: Use `orchestrator`
The `orchestrator` agent is your primary choice for 90% of tasks. It automatically:
- Analyzes your request
- Selects the appropriate specialized agents
- Manages the workflow from start to finish
- Ensures quality and consistency

**When to use `orchestrator`**:
- Project analysis and overview
- Code quality issues and fixes
- Documentation generation
- Multi-step development tasks
- When you're unsure which agent to use

**Example usage**:
```
Task("Analyze this project for code quality issues", "orchestrator")
Task("Generate documentation for the API endpoints", "orchestrator")
Task("Fix the failing tests and optimize performance", "orchestrator")
```

---

## 🎯 Common Tasks & Recommended Agents

### Development & Code Quality
| Task | Recommended Agent | Why |
|------|------------------|-----|
| **Code Quality Issues** | `quality-controller` | Specialized in auto-fixing quality problems |
| **Code Structure Analysis** | `code-analyzer` | Deep analysis of code architecture |
| **Testing & Coverage** | `test-engineer` | Test generation and database isolation |
| **Security Analysis** | `security-auditor` | Vulnerability scanning and security patterns |
| **Performance Optimization** | `performance-analytics` | Performance insights and optimization |

### Documentation & Communication
| Task | Recommended Agent | Why |
|------|------------------|-----|
| **Documentation Generation** | `documentation-generator` | Auto-maintains comprehensive docs |
| **API Documentation** | `api-contract-validator` | Synchronizes API docs with implementation |
| **Release Notes** | `version-release-manager` | Automated changelog and release docs |

### Project Management
| Task | Recommended Agent | Why |
|------|------------------|-----|
| **Project Analysis** | `orchestrator` | Comprehensive project overview |
| **Git Operations** | `git-repository-manager` | Advanced Git workflow automation |
| **Release Management** | `version-release-manager` | End-to-end release automation |
| **Workspace Organization** | `workspace-organizer` | File and report management |

### Validation & Quality
| Task | Recommended Agent | Why |
|------|------------------|-----|
| **Quality Validation** | `validation-controller` | Proactive error prevention |
| **Plugin Validation** | `claude-plugin-validator` | Plugin compliance checking |
| **Build Validation** | `build-validator` | Build configuration validation |
| **Full-Stack Validation** | `validation-controller` | Complete application validation |

### Specialized Analysis
| Task | Recommended Agent | Why |
|------|------------------|-----|
| **Frontend Issues** | `frontend-analyzer` | TypeScript, React, build validation |
| **Backend Architecture** | `code-analyzer` | Server-side code analysis |
| **GUI Debugging** | `gui-validator` | Comprehensive GUI validation |
| **Pattern Learning** | `learning-engine` | Automatic pattern recognition |

---

## 📋 Agent Descriptions

### Core Agents (High Usage)

#### 🎭 `orchestrator`
**Main autonomous decision maker** - The brain of the system
- **Best for**: General tasks, project coordination, multi-agent workflows
- **Strengths**: Intelligent agent selection, quality assurance, end-to-end management
- **Usage**: 80% of all tasks

#### 🔍 `code-analyzer`
**Code structure and pattern analysis**
- **Best for**: Architecture review, dependency analysis, code quality assessment
- **Strengths**: Deep code insights, pattern detection, structural analysis
- **Usage**: Complex codebases, refactoring decisions

#### ✅ `quality-controller`
**Quality assurance and auto-fix**
- **Best for**: Code quality issues, standards compliance, automated fixes
- **Strengths**: Auto-fixing 80-90% of common issues, quality scoring
- **Usage**: Code reviews, quality gates, pre-commit validation

#### 🛡️ `validation-controller`
**Validation and error prevention**
- **Best for**: Preventing errors, consistency checks, proactive validation
- **Strengths**: 87% error prevention rate, automatic corrections
- **Usage**: Pre-flight checks, documentation consistency

#### 🧠 `learning-engine`
**Pattern learning and improvement**
- **Best for**: Learning from patterns, continuous improvement
- **Strengths**: Silent background learning, performance optimization
- **Usage**: Automatic (runs after every task)

### Specialized Agents

#### 🎨 `frontend-analyzer`
**Frontend-specific validation and analysis**
- TypeScript validation with auto-fix
- React Query migration (v4 → v5)
- Build configuration optimization
- Bundle size analysis

#### 🔌 `api-contract-validator`
**API synchronization and type generation**
- Backend API schema extraction
- Frontend API call matching
- Auto-generate TypeScript types
- Cross-validate endpoint contracts

#### 🏗️ `build-validator`
**Build tool configuration validation**
- Vite, Webpack, Rollup validation
- Environment variable tracking
- Module system conflict detection
- Bundle optimization

#### 🔒 `security-auditor`
**Security vulnerability scanning**
- OWASP Top 10 detection
- SQL injection prevention
- XSS vulnerability scanning
- Cryptographic weakness analysis

#### 🧪 `test-engineer`
**Test generation and database management**
- Test suite generation
- Database test isolation
- SQLAlchemy 2.0 compatibility
- pytest fixture generation

#### 📚 `documentation-generator`
**Documentation maintenance and generation**
- Auto-generate docstrings
- API documentation
- README maintenance
- Technical guides

#### 🚀 `version-release-manager`
**Release automation and management**
- Semantic versioning
- Git operations automation
- Release notes generation
- Multi-platform publishing

#### 🎯 `background-task-manager`
**Parallel task execution**
- Non-blocking task management
- Parallel processing
- Result coordination
- Performance optimization

#### 💡 `smart-recommender`
**Intelligent workflow recommendations**
- Task-agent optimization
- Pattern-based suggestions
- Performance insights
- Best practice recommendations

#### 🎮 `gui-validator`
**GUI debugging and validation**
- Comprehensive GUI testing
- Visual component validation
- User experience analysis
- Performance monitoring

#### 📊 `performance-analytics`
**Performance analysis and insights**
- Learning effectiveness tracking
- Agent performance metrics
- Trend analysis
- Optimization recommendations

#### 📝 `pr-reviewer`
**Pull request review automation**
- Automated code review
- Change summarization
- Security scanning
- Quality assessment

#### 🔧 `workspace-organizer`
**Workspace and report management**
- File organization
- Report consolidation
- Cleanup automation
- Health management

#### 📋 `report-management-organizer`
**Report generation and organization**
- Automated report creation
- Categorization and archival
- Search optimization
- Link validation

#### 🎨 `claude-plugin-validator`
**Plugin compliance validation**
- Plugin guideline validation
- Structure verification
- Best practices compliance
- Installation prevention

#### 🎓 `dev-orchestrator`
**Development workflow automation**
- Milestone planning
- Incremental implementation
- Auto-debugging
- Quality assurance

---

## 🎛️ Advanced Agent Selection

### When to Use Specific Agents Directly

Use specialized agents directly when you need:

1. **Specific Expertise**: You know exactly what type of analysis you need
2. **Performance**: Faster execution for well-defined tasks
3. **Learning**: To understand how different agents work
4. **Debugging**: When orchestrator recommendations aren't optimal

### Direct Agent Usage Examples

```bash
# Frontend-specific issues
Task("Fix TypeScript errors in React components", "frontend-analyzer")

# Security audit
Task("Scan for OWASP Top 10 vulnerabilities", "security-auditor")

# Performance optimization
Task("Analyze application performance bottlenecks", "performance-analytics")

# API documentation
Task("Generate OpenAPI specification from backend", "api-contract-validator")

# Test generation
Task("Create comprehensive test suite for user authentication", "test-engineer")
```

---

## 🔄 Agent Delegation Patterns

### How Orchestrator Works

The `orchestrator` follows this pattern:

1. **Task Analysis** → Understand requirements and complexity
2. **Skill Selection** → Load relevant skills based on learned patterns
3. **Agent Delegation** → Assign tasks to specialized agents
4. **Quality Assessment** → Verify results meet standards (≥70/100)
5. **Pattern Storage** → Store successful approaches for future use

### Multi-Agent Workflows

```bash
# Example: Comprehensive code quality improvement
Task("Improve code quality across the entire project", "orchestrator")

# Orchestrator might delegate to:
# 1. code-analyzer - Identify architectural issues
# 2. quality-controller - Fix code quality problems
# 3. test-engineer - Ensure test coverage
# 4. security-auditor - Check for vulnerabilities
# 5. documentation-generator - Update docs
```

---

## 💡 Best Practices

### 1. Start with Orchestrator
- Let the system learn your preferences
- Benefit from intelligent agent selection
- Get comprehensive solutions automatically

### 2. Use Specific Agents for:
- Well-defined, repetitive tasks
- When you need specific expertise
- Performance-critical operations
- Learning agent capabilities

### 3. Combine Agents When Needed
```bash
# First analyze, then fix
Task("Analyze security vulnerabilities", "security-auditor")
Task("Fix identified security issues", "quality-controller")
```

### 4. Trust the Learning System
- The system gets smarter with each task
- Patterns are stored automatically
- Future recommendations improve based on your usage

---

## ❌ Common Mistakes to Avoid

### 1. Using Incorrect Agent Names
```bash
# ❌ INCORRECT - These don't exist:
Task("description", "autonomous-agent")
Task("description", "autonomous-agent:debug-evaluator")
Task("description", "autonomous-agent:code-analyzer")

# ✅ CORRECT - These exist:
Task("description", "orchestrator")
Task("description", "code-analyzer")
Task("description", "quality-controller")
```

### 2. Over-specifying Agent Selection
```bash
# ❌ OVERLY COMPLICATED:
Task("Fix the dashboard", "frontend-analyzer")
# (If dashboard has backend issues too)

# ✅ LET ORCHESTRATOR DECIDE:
Task("Fix the dashboard", "orchestrator")
# (Will select appropriate combination of agents)
```

### 3. Not Using Orchestrator for Complex Tasks
```bash
# ❌ MISSING OPPORTUNITY:
Task("Generate complete project documentation", "documentation-generator")

# ✅ COMPREHENSIVE APPROACH:
Task("Generate complete project documentation", "orchestrator")
# (Will use documentation-generator + other agents as needed)
```

---

## 🔍 Troubleshooting Agent Selection

### Agent Not Working?
1. **Check Name**: Ensure you're using the correct agent name (no prefix)
2. **Use Orchestrator**: Let the system select the right agent
3. **Be Specific**: Provide clear task descriptions
4. **Check Context**: Ensure the context supports the requested operation

### Poor Results?
1. **Add Context**: Provide more details about what you need
2. **Break Down Tasks**: Split complex tasks into smaller steps
3. **Try Different Agent**: Use a more specific agent for your needs
4. **Give Feedback**: The learning system improves with usage

---

## 📈 Agent Performance Metrics

### Most Effective Agents (by success rate)
1. `quality-controller` - 92% success rate
2. `orchestrator` - 89% success rate
3. `code-analyzer` - 87% success rate
4. `validation-controller` - 85% success rate
5. `documentation-generator` - 83% success rate

### Fastest Agents (by average execution time)
1. `validation-controller` - 2.3 minutes average
2. `quality-controller` - 3.1 minutes average
3. `workspace-organizer` - 3.5 minutes average
4. `background-task-manager` - 4.2 minutes average
5. `orchestrator` - 5.8 minutes average

---

## 🎓 Learning and Improvement

### Pattern Storage
Every task automatically contributes to the pattern learning database:
- Task type and complexity analysis
- Agent selection and effectiveness
- Execution approach and duration
- Quality scores and success rates

### Continuous Improvement
The system learns from:
- ✅ Successful task completion
- ✅ Quality score improvements
- ✅ Agent effectiveness metrics
- ✅ User feedback patterns

### Future Enhancements
- Intelligent agent pre-selection
- Predictive workflow optimization
- Smart error recovery
- Advanced pattern recognition

---

## 📞 Getting Help

### Debug Commands
```bash
# Debug evaluation with orchestrator
/debug:eval <target>

# Debug GUI issues
/debug:gui --quick-check
/debug:gui --comprehensive

# Learning analytics
/learn:analytics
/learn:performance
```

### Validation Commands
```bash
# Comprehensive validation
/validate:all

# Specific validation types
/validate:fullstack
/validate:plugin
/validate:patterns
```

### Analysis Commands
```bash
# Project analysis
/analyze:project
/analyze:quality
/analyze:static
```

---

**🎯 Key Takeaway**: Start with `orchestrator` for most tasks, use specialized agents when you need specific expertise, and trust the learning system to improve over time. The autonomous agent plugin is designed to make intelligent decisions on your behalf while giving you control when you need it.

---

*This guide is regularly updated based on usage patterns and system improvements. Last updated: 2025-10-28*