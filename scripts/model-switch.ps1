# Model Switch PowerShell Script for Claude Code Environment
# Cross-platform model switching between Claude and GLM

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("claude", "glm")]
    [string]$To,

    [Parameter(Mandatory=$false)]
    [string]$ApiKey,

    [Parameter(Mandatory=$false)]
    [string]$Model,

    [Parameter(Mandatory=$false)]
    [switch]$Status,

    [Parameter(Mandatory=$false)]
    [switch]$Validate,

    [Parameter(Mandatory=$false)]
    [switch]$Backup,

    [Parameter(Mandatory=$false)]
    [string]$Restore,

    [Parameter(Mandatory=$false)]
    [switch]$ListBackups,

    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Configuration
$ClaudeDir = "$env:USERPROFILE\.claude"
$SettingsFile = "$ClaudeDir\settings.json"
$BackupDir = "$ClaudeDir\backups"

# Model configurations
$GlmConfig = @{
    "ANTHROPIC_BASE_URL" = "https://api.z.ai/api/anthropic"
    "ANTHROPIC_DEFAULT_HAIKU_MODEL" = "glm-4.5-air"
    "ANTHROPIC_DEFAULT_SONNET_MODEL" = "glm-4.6"
    "ANTHROPIC_DEFAULT_OPUS_MODEL" = "glm-4.6"
}

$ClaudeConfig = @{
    "ANTHROPIC_BASE_URL" = "https://api.anthropic.com"
}

function Write-Status {
    param([string]$Message, [string]$Level = "INFO")

    $Color = switch ($Level) {
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        "INFO" { "White" }
        default { "White" }
    }

    Write-Host $Message -ForegroundColor $Color
}

function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Ensure-ClaudeDir {
    if (-not (Test-Path $ClaudeDir)) {
        try {
            New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
            Write-Status "Claude directory created: $ClaudeDir" "SUCCESS"
            return $true
        } catch {
            Write-Status "Failed to create Claude directory: $_" "ERROR"
            return $false
        }
    }
    return $true
}

function Backup-CurrentSettings {
    if (-not (Test-Path $SettingsFile)) {
        Write-Status "No existing settings to backup" "INFO"
        return $true
    }

    try {
        if (-not (Test-Path $BackupDir)) {
            New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
        }

        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFile = "$BackupDir\settings_backup_$timestamp.json"

        Copy-Item $SettingsFile $backupFile -Force
        Write-Status "Settings backed up to: $backupFile" "SUCCESS"
        return $true
    } catch {
        Write-Status "Failed to backup settings: $_" "ERROR"
        return $false
    }
}

function Get-CurrentSettings {
    if (-not (Test-Path $SettingsFile)) {
        return @{ "env" = @{} }
    }

    try {
        $content = Get-Content $SettingsFile -Raw | ConvertFrom-Json
        return $content
    } catch {
        Write-Status "Failed to load settings: $_" "ERROR"
        return $null
    }
}

function Save-Settings {
    param([hashtable]$Settings)

    try {
        $json = $Settings | ConvertTo-Json -Depth 10
        $json | Out-File -FilePath $SettingsFile -Encoding UTF8 -Force
        Write-Status "Settings saved to: $SettingsFile" "SUCCESS"
        return $true
    } catch {
        Write-Status "Failed to save settings: $_" "ERROR"
        return $false
    }
}

function Test-ApiKey {
    param([string]$ApiKey)

    if (-not $ApiKey) {
        return $false
    }

    if (-not $ApiKey.StartsWith("sk-")) {
        Write-Status "Z.AI API keys typically start with 'sk-'" "WARNING"
        return $false
    }

    if ($ApiKey.Length -lt 20) {
        Write-Status "API key seems too short" "WARNING"
        return $false
    }

    return $true
}

function Switch-ToGlm {
    param([string]$ApiKey, [string]$Model = "glm-4.6")

    if (-not (Test-ApiKey $ApiKey)) {
        return $false
    }

    if (-not (Backup-CurrentSettings)) {
        return $false
    }

    $settings = Get-CurrentSettings
    if ($null -eq $settings) {
        return $false
    }

    # Apply GLM configuration
    foreach ($key in $GlmConfig.Keys) {
        $settings.env[$key] = $GlmConfig[$key]
    }
    $settings.env["ANTHROPIC_AUTH_TOKEN"] = $ApiKey

    # Override specific model if requested
    if ($Model -in @("glm-4.5-air", "glm-4.6")) {
        $settings.env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = $Model
        $settings.env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = $Model
    }

    if (Save-Settings $settings) {
        Write-Status "Switched to GLM model: $Model" "SUCCESS"
        Write-Status "Restart Claude Code to apply changes" "INFO"
        return $true
    }

    return $false
}

function Switch-ToClaude {
    param([string]$ApiKey)

    if (-not (Backup-CurrentSettings)) {
        return $false
    }

    $settings = Get-CurrentSettings
    if ($null -eq $settings) {
        return $false
    }

    # Apply Claude configuration
    foreach ($key in $ClaudeConfig.Keys) {
        $settings.env[$key] = $ClaudeConfig[$key]
    }

    # Set API key if provided
    if ($ApiKey) {
        if (-not $ApiKey.StartsWith("sk-ant-")) {
            Write-Status "Anthropic API keys typically start with 'sk-ant-'" "WARNING"
            return $false
        }
        $settings.env["ANTHROPIC_AUTH_TOKEN"] = $ApiKey
    } elseif ($settings.env.ContainsKey("ANTHROPIC_AUTH_TOKEN")) {
        # Keep existing token
    } else {
        Write-Status "No Anthropic API key provided" "WARNING"
        return $false
    }

    if (Save-Settings $settings) {
        Write-Status "Switched to Claude models" "SUCCESS"
        Write-Status "Restart Claude Code to apply changes" "INFO"
        return $true
    }

    return $false
}

function Get-CurrentStatus {
    $settings = Get-CurrentSettings
    if ($null -eq $settings -or -not $settings.ContainsKey("env")) {
        Write-Status "No configuration found" "WARNING"
        return
    }

    $env = $settings.env
    $baseUrl = $env.ANTHROPIC_BASE_URL

    if ($baseUrl -and $baseUrl.Contains("z.ai")) {
        $model = $env.ANTHROPIC_DEFAULT_SONNET_MODEL
        Write-Status "Current Status: GLM" "INFO"
        if ($model) {
            Write-Status "Model: $model" "INFO"
        }
        Write-Status "Base URL: $baseUrl" "INFO"
    } elseif ($baseUrl -and $baseUrl.Contains("anthropic.com")) {
        Write-Status "Current Status: Claude" "INFO"
        Write-Status "Base URL: $baseUrl" "INFO"
    } else {
        Write-Status "Current Status: Unknown" "WARNING"
        if ($baseUrl) {
            Write-Status "Base URL: $baseUrl" "INFO"
        }
    }

    $tokenStatus = if ($env.ANTHROPIC_AUTH_TOKEN) { "configured" } else { "missing" }
    Write-Status "Token: $tokenStatus" "INFO"
}

function Test-Configuration {
    if (-not (Test-Path $SettingsFile)) {
        Write-Status "Settings file does not exist" "ERROR"
        return
    }

    try {
        $settings = Get-Content $SettingsFile -Raw | ConvertFrom-Json
        if (-not $settings.ContainsKey("env")) {
            Write-Status "No env section in settings" "ERROR"
            return
        }

        $env = $settings.env

        if (-not $env.ANTHROPIC_AUTH_TOKEN) {
            Write-Status "No API token configured" "ERROR"
            return
        }

        if (-not $env.ANTHROPIC_BASE_URL) {
            Write-Status "No base URL configured" "ERROR"
            return
        }

        Write-Status "Configuration is valid" "SUCCESS"
    } catch {
        Write-Status "Invalid JSON: $_" "ERROR"
    }
}

function Restore-Backup {
    param([string]$BackupName)

    if (-not (Test-Path $BackupDir)) {
        Write-Status "No backup directory found" "ERROR"
        return
    }

    if ($BackupName) {
        $backupFile = "$BackupDir\$BackupName"
    } else {
        # Find most recent backup
        $backups = Get-ChildItem -Path $BackupDir -Filter "settings_backup_*.json" | Sort-Object LastWriteTime -Descending
        if (-not $backups) {
            Write-Status "No backup files found" "ERROR"
            return
        }
        $backupFile = $backups[0].FullName
    }

    if (-not (Test-Path $backupFile)) {
        Write-Status "Backup file not found: $backupFile" "ERROR"
        return
    }

    try {
        Copy-Item $backupFile $SettingsFile -Force
        Write-Status "Restored from backup: $backupFile" "SUCCESS"
    } catch {
        Write-Status "Failed to restore backup: $_" "ERROR"
    }
}

function Get-BackupList {
    if (-not (Test-Path $BackupDir)) {
        Write-Status "No backups found" "INFO"
        return
    }

    $backups = Get-ChildItem -Path $BackupDir -Filter "settings_backup_*.json" | Sort-Object LastWriteTime -Descending
    if ($backups) {
        Write-Status "Available backups:" "INFO"
        foreach ($backup in $backups) {
            $created = $backup.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
            Write-Host "  $($backup.Name) ($created)"
        }
    } else {
        Write-Status "No backups found" "INFO"
    }
}

# Main execution
if (-not (Ensure-ClaudeDir)) {
    exit 1
}

if ($ListBackups) {
    Get-BackupList
}
elseif ($Restore) {
    Restore-Backup -BackupName $Restore
}
elseif ($Status) {
    Get-CurrentStatus
}
elseif ($Validate) {
    Test-Configuration
}
elseif ($Backup) {
    if (Backup-CurrentSettings) {
        Write-Status "Backup created" "SUCCESS"
    } else {
        Write-Status "Failed to create backup" "ERROR"
    }
}
elseif ($To -eq "glm") {
    $apiKey = $ApiKey
    if (-not $apiKey -and -not $Force) {
        $apiKey = Read-Host "Enter your Z.AI API key"
    }

    $model = $Model
    if (-not $model) {
        $model = "glm-4.6"
    }

    if (Switch-ToGlm -ApiKey $apiKey -Model $model) {
        Write-Status "Successfully switched to GLM" "SUCCESS"
    } else {
        Write-Status "Failed to switch to GLM" "ERROR"
    }
}
elseif ($To -eq "claude") {
    $apiKey = $ApiKey
    if (-not $apiKey -and -not $Force) {
        # Try to use existing token
        $settings = Get-CurrentSettings
        if ($settings -and $settings.ContainsKey("env")) {
            $apiKey = $settings.env["ANTHROPIC_AUTH_TOKEN"]
        }
    }

    if (-not $apiKey -and -not $Force) {
        $apiKey = Read-Host "Enter your Anthropic API key"
    }

    if (Switch-ToClaude -ApiKey $apiKey) {
        Write-Status "Successfully switched to Claude" "SUCCESS"
    } else {
        Write-Status "Failed to switch to Claude" "ERROR"
    }
}
else {
    Write-Host @"
Model Switch PowerShell Script

Usage:
    .\model-switch.ps1 -To <claude|glm> [-ApiKey <key>] [-Model <model>]
    .\model-switch.ps1 -Status
    .\model-switch.ps1 -Validate
    .\model-switch.ps1 -Backup
    .\model-switch.ps1 -Restore [backup-name]
    .\model-switch.ps1 -ListBackups

Examples:
    .\model-switch.ps1 -To glm -ApiKey sk-xxxxxxxx
    .\model-switch.ps1 -To claude -ApiKey sk-ant-xxxxxxxx
    .\model-switch.ps1 -Status
    .\model-switch.ps1 -To glm -Force
"@ -ForegroundColor Cyan
}