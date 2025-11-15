---
name: dev:model-switch
description: Switch between Claude and GLM AI models with secure token management
delegates-to: autonomous-agent:orchestrator
---

# Development Model Switch Command

Switch between Claude and GLM models in your Claude Code environment with secure token management and cross-platform compatibility.

## Usage

```bash
# Switch to GLM models (interactive setup)
/autonomous-agent:dev:model-switch --to glm

# Switch to Claude models (restore defaults)
/autonomous-agent:dev:model-switch --to claude

# Check current model configuration
/autonomous-agent:dev:model-switch --status

# Auto-switch based on task type (future feature)
/autonomous-agent:dev:model-switch --auto

# Set up initial configuration
/autonomous-agent:dev:model-switch --setup
```

## How It Works

### Model Configuration

The command modifies `~/.claude/settings.json` to configure model endpoints:

**GLM Configuration:**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zai_api_key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.5-air",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-4.6"
  }
}
```

**Claude Configuration (Default):**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_anthropic_api_key",
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
  }
}
```

### Cross-Platform Implementation

**Windows (PowerShell):**
```powershell
# Create settings directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"

# Update configuration
$config = Get-Content "$env:USERPROFILE\.claude\settings.json" | ConvertFrom-Json
$config.env.ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"
$config.env.ANTHROPIC_AUTH_TOKEN = $apiKey
$config | ConvertTo-Json | Set-Content "$env:USERPROFILE\.claude\settings.json"
```

**Linux/macOS (Bash):**
```bash
# Create settings directory
mkdir -p ~/.claude

# Update configuration
jq '.env.ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic" |
jq '.env.ANTHROPIC_AUTH_TOKEN = "'$apiKey'"' ~/.claude/settings.json > ~/.claude/settings.json.tmp &&
mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

## Features

### 🔒 **Secure Token Management**

- **Token Validation**: Validates API key format before use
- **Secure Storage**: Stores tokens only in local settings file
- **Privacy First**: Never shares tokens with external services
- **Token Encryption**: Future enhancement for encrypted token storage

### 🌐 **Cross-Platform Compatibility**

- **Windows**: PowerShell script execution
- **Linux/macOS**: Bash script execution with jq fallback
- **Automatic Detection**: Detects platform and uses appropriate method
- **Fallback Options**: Manual instructions if automation fails

### 🎯 **Smart Configuration**

- **Backup Creation**: Automatically backs up current settings
- **Validation**: Validates JSON syntax before applying changes
- **Rollback**: Easy rollback to previous configuration
- **Status Checking**: Real-time configuration status display

### 🚀 **Future Automation**

- **Task-Based Switching**: Automatically switch models based on task complexity
- **Performance Optimization**: Choose models based on task requirements
- **Cost Management**: Optimize model usage for cost efficiency
- **Load Balancing**: Distribute tasks across available models

## Command Options

### Basic Switching

```bash
# Switch to GLM (interactive)
/autonomous-agent:dev:model-switch --to glm

# Switch to Claude (restore defaults)
/autonomous-agent:dev:model-switch --to claude
```

### Status and Information

```bash
# Check current configuration
/autonomous-agent:dev:model-switch --status

# Show available models
/autonomous-agent:dev:model-switch --list-models

# Validate current configuration
/autonomous-agent:dev:model-switch --validate
```

### Advanced Options

```bash
# Force switch without confirmation
/autonomous-agent:dev:model-switch --to glm --force

# Use specific GLM model
/autonomous-agent:dev:model-switch --to glm --model glm-4.6

# Backup current settings before switching
/autonomous-agent:dev:model-switch --to glm --backup

# Dry run (show changes without applying)
/autonomous-agent:dev:model-switch --to glm --dry-run
```

## Model Comparison

| Feature | Claude (Anthropic) | GLM (Z.AI) | Best For |
|---------|-------------------|-------------|-----------|
| **Response Quality** | Excellent | Very Good | General tasks |
| **Speed** | Fast | Very Fast | Quick tasks |
| **Cost** | Higher | Lower | Budget-conscious |
| **Chinese Support** | Good | Excellent | Chinese content |
| **Code Analysis** | Excellent | Good | Code review |
| **Creative Tasks** | Excellent | Very Good | Creative writing |
| **Technical Accuracy** | Excellent | Good | Technical docs |

## Security Best Practices

### 🔒 **Token Security**

- **Never share API keys** in plain text
- **Use environment variables** when possible
- **Rotate tokens regularly** for security
- **Monitor usage** for unauthorized access
- **Store securely** in encrypted format

### 🛡️ **Configuration Security**

- **Backup settings** before making changes
- **Validate JSON syntax** to prevent corruption
- **Use secure connections** (HTTPS only)
- **Close Claude windows** before applying changes
- **Verify changes** after applying

### 🔐 **Privacy Protection**

- **Local storage only** - no cloud sync of tokens
- **No telemetry** - usage data stays private
- **Secure deletion** - clear tokens when needed
- **Access control** - limit file permissions
- **Audit trail** - log configuration changes

## Examples

### Initial GLM Setup

```bash
# First-time GLM setup
/autonomous-agent:dev:model-switch --to glm

# Interactive prompts:
# 1. Enter your Z.AI API key: [sk-xxxxxxxx]
# 2. Validate API key... ✅ Valid
# 3. Back up current settings... ✅ Backed up
# 4. Apply GLM configuration... ✅ Applied
# 5. Restart Claude Code to apply changes

# Status after setup:
Current Model: GLM (glm-4.6)
API Endpoint: https://api.z.ai/api/anthropic
Token Status: ✅ Valid
Last Updated: 2025-01-26 20:45:30
```

### Quick Model Toggle

```bash
# Switch to GLM for Chinese content
/autonomous-agent:dev:model-switch --to glm --force

# Switch back to Claude for code analysis
/autonomous-agent:dev:model-switch --to claude

# Check current status
/autonomous-agent:dev:model-switch --status
```

### Advanced Configuration

```bash
# Use specific GLM model with backup
/autonomous-agent:dev:model-switch --to glm --model glm-4.5-air --backup

# Dry run to preview changes
/autonomous-agent:dev:model-switch --to glm --dry-run

# Validate configuration without switching
/autonomous-agent:dev:model-switch --validate --target glm
```

## Troubleshooting

### Common Issues

**API Key Invalid:**
```bash
# Check token format
/autonomous-agent:dev:model-switch --validate-token sk-xxxxxxxx

# Re-enter token
/autonomous-agent:dev:model-switch --to glm --renew-token
```

**Configuration Not Applied:**
```bash
# Check file permissions
/autonomous-agent:dev:model-switch --check-permissions

# Manually apply changes
/autonomous-agent:dev:model-switch --to glm --manual
```

**Model Not Responding:**
```bash
# Test API connection
/autonomous-agent:dev:model-switch --test-connection

# Switch to backup model
/autonomous-agent:dev:model-switch --fallback claude
```

### Platform-Specific Issues

**Windows PowerShell:**
```powershell
# Check PowerShell execution policy
Get-ExecutionPolicy

# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/macOS:**
```bash
# Check jq installation
jq --version

# Install jq if needed
# Ubuntu/Debian: sudo apt-get install jq
# macOS: brew install jq
# CentOS/RHEL: sudo yum install jq
```

### Recovery Options

```bash
# Restore from backup
/autonomous-agent:dev:model-switch --restore-backup

# Reset to defaults
/autonomous-agent:dev:model-switch --reset-defaults

# Generate new configuration
/autonomous-agent:dev:model-switch --generate-config
```

## Integration with Learning System

The model-switch command integrates with the autonomous learning system:

**Pattern Storage:**
```json
{
  "model_switch_patterns": {
    "task_type": "chinese_translation",
    "preferred_model": "glm",
    "success_rate": 0.92,
    "performance_improvement": "+15%",
    "cost_savings": "-40%"
  }
}
```

**Auto-Switching Logic:**
- Analyze task requirements
- Match with historical performance
- Recommend optimal model
- Learn from user choices
- Optimize for cost and quality

## Future Enhancements

### 🚀 **Planned Features**

- **Multi-Model Load Balancing**: Distribute tasks across models
- **Performance Analytics**: Track model performance metrics
- **Cost Optimization**: Automatic cost-effective model selection
- **Smart Routing**: Route tasks to best-suited models
- **Token Management**: Automated token rotation and management
- **Model Comparison**: Side-by-side model performance testing

### 🔧 **Technical Improvements**

- **Encrypted Storage**: Secure token encryption
- **API Rate Limiting**: Intelligent rate limit handling
- **Connection Pooling**: Optimized connection management
- **Caching**: Response caching for faster performance
- **Monitoring**: Real-time model performance monitoring

---

**Version**: 1.0.0
**Integration**: Uses orchestrator agent with security-patterns skill
**Platform**: Cross-platform (Windows, Linux, Mac)
**Security**: Privacy-first with secure token management
