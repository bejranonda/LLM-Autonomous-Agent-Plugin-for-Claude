---
name: research:compare
description: Specialized A vs B comparison research with decision matrix, trade-off analysis, and clear recommendations - optimized for choosing between two options
delegates-to: autonomous-agent:research-executor
---

# Compare Research Command

**Command**: `/research:compare`

Specialized research command optimized for comparing two options (A vs B). Produces structured comparison with decision matrix, trade-off analysis, and clear recommendation. Perfect for technology choices, framework selection, and product decisions.

## When to Use

**Use `/research:compare` for:**
- Comparing exactly 2 options (A vs B)
- Technology/framework selection decisions
- Product/service comparisons
- Tool/library choices
- Platform comparisons

**Use `/research:structured` for:**
- Comparing 3+ options
- Open-ended research
- Complex multi-faceted topics
- Research without clear alternatives

**Use `/research:quick` for:**
- Simple factual lookups
- Quick reference checks
- Latest version queries

## How It Works

**Comparison-Optimized Workflow**:
1. **Define Criteria**: Identify key decision factors
2. **Research Both Options**: Gather data on A and B
3. **Build Decision Matrix**: Score each option on criteria
4. **Trade-off Analysis**: Identify strengths/weaknesses
5. **Recommendation**: Clear choice with reasoning

**Time**: 10-20 minutes (faster than `/research:structured` for 2-option comparisons)

## Usage

### Technology Comparisons
```bash
/research:compare "React vs Vue for e-commerce project"
/research:compare "PostgreSQL vs MongoDB for analytics app"
/research:compare "TypeScript vs JavaScript for new codebase"
```

### Framework Comparisons
```bash
/research:compare "Next.js vs Remix for SSR"
/research:compare "Express vs Fastify for Node.js API"
/research:compare "Tailwind CSS vs styled-components"
```

### Tool Comparisons
```bash
/research:compare "Webpack vs Vite for React build"
/research:compare "Jest vs Vitest for testing"
/research:compare "Docker vs Podman for containers"
```

### Platform Comparisons
```bash
/research:compare "AWS vs GCP for startup hosting"
/research:compare "Vercel vs Netlify for Next.js deployment"
/research:compare "GitHub Actions vs GitLab CI"
```

### Protocol/Standard Comparisons
```bash
/research:compare "I2C vs SPI for Raspberry Pi sensors"
/research:compare "REST vs GraphQL for mobile API"
/research:compare "WebSocket vs Server-Sent Events"
```

## Output Format

**Terminal** (15-20 lines):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON RESEARCH: A vs B
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision Matrix (scored 0-10):

Criteria        | Option A | Option B | Winner
----------------|----------|----------|--------
Performance     |    8     |    9     | B
Developer DX    |    9     |    7     | A
Ecosystem       |    10    |    6     | A
Learning Curve  |    7     |    9     | B
Cost            |    8     |    8     | Tie
----------------|----------|----------|--------
Total Score     |   42/50  |   39/50  | A

Recommendation: Option A
Reason: [2-3 sentence reasoning]

Key Trade-offs:
• A: Better ecosystem but steeper learning curve
• B: Faster performance but smaller community

Full Report: .claude/reports/compare-A-vs-B-[timestamp].md
Time: 12 minutes
```

**File Report** (Comprehensive):
Saved to `.claude/reports/compare-[A]-vs-[B]-[timestamp].md`:
- Executive summary with recommendation
- Detailed decision matrix with scoring
- Feature-by-feature comparison table
- Strengths and weaknesses for each option
- Use case recommendations (when to use A vs B)
- Migration considerations (if switching)
- Cost analysis (if applicable)
- Community and support comparison
- Future outlook and roadmap
- Sources and citations

## Decision Matrix Categories

**Common Comparison Criteria**:

### Technical Criteria
- **Performance**: Speed, efficiency, benchmarks
- **Scalability**: Handling growth, load capacity
- **Reliability**: Stability, uptime, error rates
- **Security**: Vulnerabilities, best practices
- **Compatibility**: Platform support, integrations

### Developer Experience
- **Learning Curve**: Time to productivity
- **Documentation**: Quality, completeness
- **Developer Tools**: IDE support, debugging
- **API Design**: Ease of use, consistency
- **Type Safety**: TypeScript support, type inference

### Ecosystem & Community
- **Community Size**: Active users, contributors
- **Library Ecosystem**: Available packages, plugins
- **Corporate Backing**: Funding, maintenance
- **Adoption Rate**: Industry usage, trends
- **Long-term Viability**: Future outlook

### Operational Criteria
- **Cost**: Licensing, hosting, maintenance
- **Deployment**: Ease of deployment, CI/CD
- **Monitoring**: Observability, debugging
- **Maintenance**: Update frequency, breaking changes
- **Support**: Commercial support, SLAs

## Examples

### Example 1: Framework Comparison
```bash
/research:compare "Next.js vs Remix for new React project"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON RESEARCH: Next.js vs Remix
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision Matrix (scored 0-10):

Criteria           | Next.js | Remix | Winner
-------------------|---------|-------|--------
Performance        |    8    |   9   | Remix
Developer DX       |    9    |   8   | Next.js
Ecosystem          |    10   |   7   | Next.js
Learning Curve     |    8    |   7   | Next.js
Deployment Options |    10   |   8   | Next.js
Data Loading       |    7    |   10  | Remix
Type Safety        |    9    |   9   | Tie
Community Size     |    10   |   6   | Next.js
-------------------|---------|-------|--------
Total Score        |  71/80  | 64/80 | Next.js

Recommendation: Next.js for most projects
Reason: Larger ecosystem, better deployment options (Vercel),
and gentler learning curve. Choose Remix if data loading
patterns and nested routes are critical requirements.

Key Trade-offs:
• Next.js: More mature, better DX, easier deployment
• Remix: Superior data loading, better performance, nested routing

Use Next.js when:
- Building with Vercel deployment
- Need extensive plugin ecosystem
- Team new to React frameworks
- Want incremental adoption (can start with SSG)

Use Remix when:
- Data loading is complex and critical
- Need nested route layouts
- Prefer Web Platform primitives
- Performance is top priority

Full Report: .claude/reports/compare-nextjs-vs-remix-20250115.md
Sources: 12 (official docs, benchmarks, developer surveys)
Time: 14m 23s
```

### Example 2: Database Comparison
```bash
/research:compare "PostgreSQL vs MongoDB for analytics dashboard"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON RESEARCH: PostgreSQL vs MongoDB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context: Analytics Dashboard Application

Decision Matrix (scored 0-10):

Criteria              | PostgreSQL | MongoDB | Winner
----------------------|------------|---------|--------
Query Performance     |     9      |    7    | PostgreSQL
Aggregation Pipelines |     7      |    9    | MongoDB
ACID Compliance       |    10      |    6    | PostgreSQL
Schema Flexibility    |     6      |   10    | MongoDB
Scaling Strategy      |     7      |    9    | MongoDB
Complex Joins         |    10      |    5    | PostgreSQL
Time-series Data      |     8      |    7    | PostgreSQL
Cost (hosting)        |     8      |    8    | Tie
----------------------|------------|---------|--------
Total Score           |   65/80    |  61/80  | PostgreSQL

Recommendation: PostgreSQL (with TimescaleDB extension)
Reason: Analytics dashboards benefit from complex joins,
ACID guarantees, and SQL's analytical functions. PostgreSQL
with TimescaleDB extension provides excellent time-series
performance while maintaining relational integrity.

Key Trade-offs:
• PostgreSQL: Better for complex queries, joins, ACID, less flexible schema
• MongoDB: Better for flexible schema, horizontal scaling, but weaker joins

Performance Benchmarks:
- Complex aggregations: PostgreSQL 40% faster (windowing functions)
- Simple document retrieval: MongoDB 15% faster
- Multi-table joins: PostgreSQL significantly faster

Cost Analysis:
- PostgreSQL: Self-hosted ~$50/mo, Managed (AWS RDS) ~$200/mo
- MongoDB: Self-hosted ~$50/mo, Atlas ~$250/mo
- Winner: Comparable costs

Migration Considerations:
- If switching FROM MongoDB: Schema design needed, denormalization → normalization
- If switching FROM PostgreSQL: Convert JOINs to aggregation pipeline

Full Report: .claude/reports/compare-postgresql-vs-mongodb-20250115.md
Sources: 18 (official docs, benchmarks, case studies, DB-engines)
Time: 16m 47s
```

### Example 3: Protocol Comparison
```bash
/research:compare "I2C vs SPI for Raspberry Pi sensor array"
```

**Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON RESEARCH: I2C vs SPI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context: Raspberry Pi with multiple sensors

Decision Matrix (scored 0-10):

Criteria            | I2C  | SPI  | Winner
--------------------|------|------|--------
Speed               |  6   |  10  | SPI
Wire Count          |  10  |   5  | I2C (2 vs 4+)
Multi-device        |  10  |   6  | I2C (bus)
Complexity          |  8   |   6  | I2C
Distance            |  7   |   5  | I2C
Power Consumption   |  8   |   7  | I2C
Device Support      |  9   |   8  | I2C
--------------------|------|------|--------
Total Score         | 58/70| 47/70| I2C

Recommendation: I2C for this use case
Reason: Sensor arrays benefit from I2C's bus topology
(connect multiple sensors with 2 wires). SPI's speed
advantage (10MHz vs 400kHz) not critical for sensor
polling (typically 1-10Hz sampling rate).

Technical Specs:
I2C:
- Speed: 100kHz (standard), 400kHz (fast), 3.4MHz (high-speed)
- Wires: 2 (SDA, SCL) + power/ground
- Addressing: 7-bit (128 devices) or 10-bit (1024 devices)
- Pull-up resistors: Required (2.2k-10k ohm)

SPI:
- Speed: 10MHz+ (up to 100MHz+)
- Wires: 4 (MISO, MOSI, SCK, CS) per device + power/ground
- Chip Select: 1 pin per device (limit: GPIO pins)
- No pull-ups: Push-pull outputs

Use I2C when:
- Connecting 3+ sensors (shared bus)
- Wire count matters (long distances, tight spaces)
- Sensor sampling rate < 1kHz
- Power efficiency important

Use SPI when:
- High-speed data transfer needed (ADC, display)
- Connecting 1-2 devices only
- Full-duplex communication required
- Deterministic timing critical

Wiring Example (I2C):
```
Raspberry Pi GPIO:
- Pin 3 (GPIO 2) → SDA (all sensors)
- Pin 5 (GPIO 3) → SCL (all sensors)
- Add 2.2k pull-up resistors on both lines
```

Full Report: .claude/reports/compare-i2c-vs-spi-20250115.md
Sources: 8 (datasheets, Raspberry Pi docs, electronics forums)
Time: 11m 52s
```

## Comparison Table Structure

**Feature-by-Feature Comparison** (in file report):

```markdown
| Feature | Option A | Option B | Analysis |
|---------|----------|----------|----------|
| [Feature 1] | [A's approach] | [B's approach] | [Which is better and why] |
| [Feature 2] | [A's approach] | [B's approach] | [Which is better and why] |
...
```

**Strengths & Weaknesses**:

```markdown
## Option A

### Strengths ✅
1. [Strength 1 with evidence]
2. [Strength 2 with evidence]
3. [Strength 3 with evidence]

### Weaknesses ❌
1. [Weakness 1 with impact]
2. [Weakness 2 with impact]
3. [Weakness 3 with impact]

## Option B

### Strengths ✅
1. [Strength 1 with evidence]
2. [Strength 2 with evidence]
3. [Strength 3 with evidence]

### Weaknesses ❌
1. [Weakness 1 with impact]
2. [Weakness 2 with impact]
3. [Weakness 3 with impact]
```

## Recommendation Logic

**Decision Tree**:

```
1. Calculate total scores from decision matrix
2. Identify clear winner (score difference > 10%)
3. If close (<10% difference):
   - Identify context-specific criteria
   - Provide conditional recommendations
   - List use-case-specific guidance
4. Provide clear action items
```

**Recommendation Format**:
```
Recommendation: [Option A/B/Conditional]

Primary Reason: [1-2 sentences]

Context Considerations:
- Choose A if: [specific conditions]
- Choose B if: [specific conditions]

Action Items:
1. [Next step 1]
2. [Next step 2]
3. [Next step 3]
```

## Pattern Learning

Comparison patterns stored for optimization:
```json
{
  "task_type": "research_compare",
  "options": ["Next.js", "Remix"],
  "category": "web_framework",
  "recommendation": "Next.js",
  "score_difference": 7,
  "key_criteria": ["ecosystem", "deployment", "learning_curve"],
  "sources_count": 12,
  "time_taken": "14m 23s"
}
```

Learns:
- Effective comparison criteria by category
- Common decision factors for each domain
- Reliable sources for specific comparisons
- Typical score patterns and distributions

## Integration

**Agents Used**:
- research-executor (with comparison-optimized workflow)
- research-strategist (defines comparison criteria)

**Skills Auto-Loaded**:
- research-methodology (comparison patterns)

**Pattern Storage**:
- Stores comparison outcomes in `.claude-patterns/`
- Learns effective criteria for technology categories
- Improves scoring accuracy over time

## Best Practices

**Good Comparison Queries**:
- ✅ "A vs B for [specific use case]"
- ✅ "[Technology A] vs [Technology B]"
- ✅ "Should I use A or B for [project]"

**Bad Comparison Queries** (use `/research:structured` instead):
- ❌ "Best framework for web development" (too open-ended)
- ❌ "Compare 5 databases" (use structured research for 3+)
- ❌ "Pros and cons of A" (single option, not comparison)

**Improving Comparison Quality**:
1. Provide context: "for [use case]"
2. Mention constraints: "low budget", "high performance"
3. Specify priorities: "prioritize developer experience"

**Example with Context**:
```bash
# Generic (less useful)
/research:compare "React vs Vue"

# With context (more useful)
/research:compare "React vs Vue for e-commerce SPA with TypeScript"
```

---

**Version**: 1.0.0
**Integration**: Works with research-strategist and research-executor agents
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: WebSearch, WebFetch tools
