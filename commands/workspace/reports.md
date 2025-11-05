---
name: workspace:reports
description: Organize and consolidate scattered reports into clean directory structure
delegates-to: autonomous-agent:orchestrator
---


# Organize Reports Command

## Command: `/workspace:reports`

Automated report organization and management system that categorizes, archives, and optimizes all validation, quality, and analysis reports with intelligent cleanup and searchable storage.

## How It Works

1. **Report Discovery**: Scans repository for all report files and analyzes content
2. **Intelligent Categorization**: Classifies reports by type, importance, and relevance
3. **Organized Storage**: Moves reports to structured directory hierarchy
4. **Automated Archival**: Archives old reports based on retention policies
5. **Duplicate Management**: Identifies and merges duplicate or redundant reports
6. **Search Indexing**: Creates searchable metadata index for all reports
7. **Cleanup Optimization**: Removes obsolete files and optimizes storage

## Usage

### Basic Organization
```bash
# Organize all reports with default settings
/workspace:reports

# Quick organization (current reports only)
/organize-reports --quick

# Deep organization (includes archival and compression)
/organize-reports --deep
```

### Advanced Organization Options
```bash
# Custom organization with specific rules
/organize-reports \
  --archive-policy 90days \
  --compress-old \
  --remove-duplicates \
  --create-index

# Organize specific report types
/organize-reports --type validation
/organize-reports --type quality,performance

# Organize by date range
/organize-reports --date-range "2024-01-01..2024-01-31"
/organize-reports --older-than 30days
```

### Dry Run and Preview
```bash
# Preview organization without making changes
/organize-reports --dry-run

# Show detailed analysis before organizing
/organize-reports --analyze

# Interactive mode with confirmation prompts
/organize-reports --interactive
```

## Organization Structure

### Target Directory Structure
```
.reports/
├── current/                    # Active reports (last 30 days)
│   ├── validation/            # Plugin validation reports
│   │   ├── plugin-validation-2024-01-15.md
│   │   ├── claude-plugin-validation-2024-01-14.md
│   │   └── installation-validation-2024-01-13.md
│   ├── quality/               # Quality assessment reports
│   │   ├── code-quality-2024-01-15.md
│   │   ├── standards-compliance-2024-01-14.md
│   │   └── best-practices-2024-01-13.md
│   ├── performance/           # Performance analysis reports
│   │   ├── execution-time-analysis-2024-01-15.md
│   │   └── resource-usage-2024-01-14.md
│   ├── security/              # Security scan reports
│   │   ├── vulnerability-scan-2024-01-15.md
│   │   └── dependency-security-2024-01-14.md
│   ├── testing/               # Test execution reports
│   │   ├── test-coverage-2024-01-15.md
│   │   └── test-results-2024-01-14.md
│   └── summary/               # Executive summary reports
│       ├── weekly-summary-2024-01-15.md
│       └── monthly-report-2024-01-01.md
├── recent/                     # Recent reports (30-90 days)
│   ├── 2024-01/               # Monthly organization
│   │   ├── validation/
│   │   ├── quality/
│   │   └── performance/
│   └── 2023-12/
├── archive/                    # Archived reports (90+ days)
│   ├── 2023/                  # Yearly organization
│   │   ├── Q1/               # Quarterly organization
│   │   │   ├── validation/
│   │   │   ├── quality/
│   │   │   └── performance/
│   │   ├── Q2/
│   │   ├── Q3/
│   │   └── Q4/
│   └── 2022/
├── templates/                  # Report templates
│   ├── validation-template.md
│   ├── quality-template.md
│   └── performance-template.md
├── metrics/                    # Aggregated metrics and trends
│   ├── quality-trends.json
│   ├── performance-metrics.json
│   └── validation-history.json
└── index/                      # Search indices and metadata
    ├── reports-index.json
    ├── search-index.json
    └── metadata-db.json
```

## Command Line Options

### Organization Mode
```bash
--quick                   # Quick organization (current reports only)
--deep                    # Deep organization (includes archival, compression)
--analyze                 # Analyze reports without organizing
--dry-run                 # Preview changes without executing
--interactive             # Interactive mode with confirmations
```

### Report Selection
```bash
--type <types>           # Specific report types to organize
                         # Values: validation,quality,performance,security,
                         #         testing,documentation,summary
                         # Default: all

--date-range <range>     # Date range for reports (YYYY-MM-DD..YYYY-MM-DD)
--older-than <period>    # Reports older than period (e.g., 30days, 3months)
--newer-than <period>    # Reports newer than period
--pattern <pattern>      # File pattern matching (glob)
```

### Archival Options
```bash
--archive-policy <policy> # Archival retention policy
                           # Values: 30days, 60days, 90days, 6months, 1year
                           # Default: 90days

--compress-old           # Compress reports older than archival period
--compress-level <level> # Compression level (1-9, default: 6)

--keep-critical          # Keep critical reports indefinitely
--keep-high-importance   # Keep high importance reports longer
```

### Cleanup Options
```bash
--remove-duplicates      # Remove duplicate reports
--merge-similar          # Merge similar reports
--remove-obsolete        # Remove superseded reports
--cleanup-temp           # Clean temporary and intermediate files

--storage-limit <size>   # Maximum storage usage (e.g., 500MB, 2GB)
--free-space <size>      # Target free space to maintain
```

### Index and Search
```bash
--create-index           # Create searchable index
--update-index           # Update existing index
--rebuild-index          # Rebuild index from scratch

--extract-metadata       # Extract and store metadata
--generate-thumbnails    # Generate report thumbnails/summaries
--create-summaries       # Generate executive summaries
```

### Output Control
```bash
--verbose                # Detailed output logging
--quiet                  # Minimal output
--summary                # Show organization summary only
--report-file <file>     # Save detailed report to file

--json-output            # Output in JSON format
--csv-output             # Output in CSV format
```

## Workflow Stages

### Stage 1: Report Discovery (10-30 seconds)

**Scans and identifies**:
- All report files in repository
- Report types based on content analysis
- File metadata (size, dates, hashes)
- Duplicate or similar reports

**Output**:
```
============================================================
REPORT DISCOVERY
============================================================

📁 Report Files Found: 18
├─ Root Directory: 3 files
├─ Subdirectories: 15 files
└─ Hidden Reports: 0 files

📊 Report Types Detected:
├─ Validation Reports: 6
├─ Quality Reports: 4
├─ Performance Reports: 3
├─ Plugin Reports: 2
├─ Security Reports: 1
└─ Summary Reports: 2

🔍 Analysis Results:
├─ Total Size: 2.4 MB
├─ Duplicate Files: 2
├─ Obsolete Reports: 1
├─ Critical Reports: 3
└─ High Importance: 7

⏱ Discovery completed in 23 seconds
```

### Stage 2: Categorization and Analysis (30-60 seconds)

**Analyzes and categorizes**:
- Report content and structure
- Importance and relevance scoring
- Date-based categorization
- Cross-reference relationships

**Output**:
```
============================================================
CATEGORIZATION ANALYSIS
============================================================

📋 Classification Results:
├─ Current Reports (≤30 days): 8 files
├─ Recent Reports (30-90 days): 6 files
├─ Archive Candidates (>90 days): 4 files
└─ Template Files: 0 files

🎯 Importance Distribution:
├─ Critical Issues: 3 reports
│  ├─ Security vulnerabilities
│  ├─ Breaking validation failures
│  └─ Critical quality issues
├─ High Priority: 7 reports
├─ Medium Priority: 5 reports
└─ Low Priority: 3 reports

🔗 Report Relationships:
├─ Related Report Groups: 4
├─ Duplicate Pairs: 2
├─ Sequential Reports: 3
└─ Cross-References: 12

📈 Quality Metrics:
├─ Average Report Score: 82/100
├─ Completeness Rate: 94%
├─ Consistency Score: 88%
└─ Actionability Index: 76%

⏱ Categorization completed in 47 seconds
```

### Stage 3: Organization Execution (1-3 minutes)

**Executes organization**:
- Creates directory structure
- Moves files to appropriate locations
- Updates file names and metadata
- Creates cross-references and links

**Output**:
```
============================================================
ORGANIZATION EXECUTION
============================================================

📂 Directory Structure Created:
├─ .reports/current/validation/ ✓
├─ .reports/current/quality/ ✓
├─ .reports/current/performance/ ✓
├─ .reports/recent/2024-01/ ✓
├─ .reports/archive/2023/Q4/ ✓
└─ .reports/metrics/ ✓

📁 Files Organized:
├─ Current Reports: 8 files moved
├─ Recent Reports: 6 files moved
├─ Archived Reports: 4 files moved
├─ Duplicates Removed: 2 files
└─ Obsolete Reports: 1 file removed

🏷️ File Naming Applied:
├─ Standardized format: {type}-{date}-{id}.md
├─ Consistent date format: YYYY-MM-DD
├─ Unique identifiers added: 12 files
└─ Metadata embedded: 18 files

🔗 Cross-References Created:
├─ Related reports linked: 12 links
├─ Sequential reports grouped: 3 groups
├─ Summary reports updated: 2 summaries
└─ Index entries created: 18 entries

📊 Storage Optimization:
├─ Space Saved: 156 KB (6.5% reduction)
├─ Compression Applied: 4 files
├─ Duplicates Removed: 320 KB
└─ Index Size: 45 KB

🎯 Organization Status: SUCCESS
⏱ Organization completed in 2.1 minutes
```

### Stage 4: Index Creation and Search (30-60 seconds)

**Creates search infrastructure**:
- Full-text search index
- Metadata database
- Cross-reference map
- Trend analysis data

**Output**:
```
============================================================
SEARCH INDEX CREATION
============================================================

🔍 Search Index Built:
├─ Full-Text Index: 18 documents indexed
├─ Metadata Database: 18 records
├─ Cross-Reference Map: 32 relationships
└─ Trend Data: 6 months of history

📊 Index Statistics:
├─ Total Terms: 3,247 unique terms
├─ Document Count: 18 reports
├─ Average Document Size: 15.2 KB
├─ Index Size: 127 KB
└─ Search Speed: <50ms average

🎯 Search Capabilities:
├─ Content Search: Full-text search across all reports
├─ Metadata Search: Search by type, date, importance
├─ Trend Analysis: Track metrics over time
├─ Comparative Analysis: Compare similar reports
└─ Custom Queries: Advanced search with filters

📈 Analytics Data Generated:
├─ Quality Trends: Monthly quality score progression
├─ Issue Patterns: Common issues and frequencies
├─ Resolution Times: Average time to address issues
└─ Improvement Metrics: Progress tracking over time

🔗 Integration Ready:
├─ CLI Search Interface: Available
├─ Web Dashboard: Optional
├─ API Access: RESTful API available
└─ Export Formats: JSON, CSV, PDF

🎯 Index Creation: SUCCESS
⏱ Index creation completed in 54 seconds
```

## Search and Retrieval

### Built-in Search Commands
```bash
# Search by content
search-reports "validation failed" --type validation

# Search by metadata
search-reports --importance critical --date-range "2024-01-01..2024-01-31"

# Trend analysis
analyze-trends --metric quality_score --period monthly

# Generate summaries
generate-summary --type validation --period "last_30_days"

# Compare reports
compare-reports --type validation --date-range "2023-12..2024-01"
```

### Search Query Examples
```bash
# Find critical security issues
search-reports "security vulnerability" --importance critical --type security

# Track quality improvements
search-reports --type quality --metric score --trend improving

# Find all validation reports from January
search-reports --type validation --date 2024-01

# Generate performance summary
generate-summary --type performance --format markdown --output performance-summary.md
```

## Integration with Other Commands

### With Validation Commands
```bash
# Run validation then organize results
/validate-fullstack
/organize-reports --type validation --quick
```

### With Quality Commands
```bash
# Quality check with report organization
/quality-check
/organize-reports --type quality --create-index
```

### With Learning Commands
```bash
# Analyze patterns and organize findings
/auto-analyze
/organize-reports --deep --extract-metadata
```

## Retention Policies

### Default Retention Rules
```yaml
retention_policies:
  current_reports:
    duration: 30 days
    compression: false
    backup: true

  recent_reports:
    duration: 90 days
    compression: true
    backup: true

  archived_reports:
    duration: 1 year
    compression: true
    backup: true

  critical_reports:
    duration: permanent
    compression: false
    backup: true
    multiple_copies: true
```

### Custom Retention Rules
```bash
# Set custom retention policy
/organize-reports \
  --archive-policy 6months \
  --keep-critical \
  --compress-old \
  --storage-limit 1GB
```

## Best Practices

### Regular Organization
- **Daily**: Quick organization of new reports
- **Weekly**: Deep organization with archival
- **Monthly**: Index rebuilding and optimization
- **Quarterly**: Complete cleanup and retention review

### Storage Management
- Monitor storage usage regularly
- Set appropriate retention policies
- Compress old reports to save space
- Maintain backups of critical reports

### Search Optimization
- Update index regularly
- Use descriptive file names
- Add relevant metadata and tags
- Create executive summaries for quick reference

## Troubleshooting

### Common Issues

**Insufficient Permissions**:
```bash
# Check permissions
ls -la .reports/
# Fix permissions
chmod -R 755 .reports/
```

**Storage Space Issues**:
```bash
# Check disk usage
df -h
# Free up space
/organize-reports --compress-old --archive-policy 30days
```

**Search Index Corruption**:
```bash
# Rebuild index
/organize-reports --rebuild-index
```

### Recovery Procedures

**Lost Reports**:
```bash
# Check for moved files
find . -name "*validation*" -type f
# Restore from backup if available
```

**Damaged Index**:
```bash
# Remove corrupted index
rm -f .reports/index/*.json
# Rebuild from scratch
/organize-reports --rebuild-index --deep
```

## Integration with Learning System

The Report Organizer learns from organization patterns to improve future operations:

**Pattern Learning**:
- Optimal categorization rules for different report types
- User preferences for report organization and access
- Common report patterns and relationships
- Storage optimization strategies based on usage

**Continuous Improvement**:
- Improved duplicate detection algorithms
- Better relevance scoring for reports
- Enhanced search result ranking
- Optimized retention policies

---

**Version**: 1.0.0
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: Standard file system tools
**Integration**: Works with all validation and quality reporting commands