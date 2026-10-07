<#
QA OS - one-time MCP connector setup for a QA member's Windows PC.

Configures every MCP connector QA OS uses:
  selenium               browser automation (npx @angiejones/mcp-selenium)
  snd-schema             S&D application DB, read-only (connectors\db-mcp)
  selenium-framework-db  CTA_CONFIG_ASSERTION framework DB, read-only (connectors\db-mcp)

Writes them into the Claude Desktop config (%APPDATA%\Claude\claude_desktop_config.json),
after taking a timestamped backup. With -ClaudeCode it also registers them for the
Claude Code CLI (user scope). Atlassian (Jira) is a claude.ai connector: see the
message printed at the end.

Run from the qa-os folder:
  powershell -ExecutionPolicy Bypass -File connectors\setup_mcp.ps1
  powershell -ExecutionPolicy Bypass -File connectors\setup_mcp.ps1 -ClaudeCode
  powershell -ExecutionPolicy Bypass -File connectors\setup_mcp.ps1 -SkipDb   (Selenium only)

Passwords are typed by you (hidden input). They are stored only in your own Claude
config file on this PC, the same way every MCP client stores them. Never commit or
share that file. Use read-only database users.
#>
param(
    [switch]$ClaudeCode,
    [switch]$SkipDb,
    [switch]$SkipSelenium
)

$ErrorActionPreference = 'Stop'

function Write-Step($text) { Write-Host ""; Write-Host "== $text" -ForegroundColor Cyan }
function Write-Ok($text)   { Write-Host "   OK  $text" -ForegroundColor Green }
function Write-Warn2($text){ Write-Host "   !!  $text" -ForegroundColor Yellow }

function Read-Value($prompt, $default) {
    if ($default) { $v = Read-Host "$prompt [$default]" } else { $v = Read-Host $prompt }
    if ([string]::IsNullOrWhiteSpace($v)) { return $default }
    return $v.Trim()
}

function Read-Secret($prompt) {
    $s = Read-Host $prompt -AsSecureString
    $b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($b) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b) }
}

$QaosRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$DbMcp    = Join-Path $QaosRoot 'connectors\db-mcp'
$VenvPy   = Join-Path $DbMcp 'venv\Scripts\python.exe'
$Server   = Join-Path $DbMcp 'mcp_server.py'

Write-Host "QA OS MCP setup  (qa-os folder: $QaosRoot)"

# ---------------------------------------------------------------- prerequisites
Write-Step "Checking prerequisites"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python -and -not $SkipDb) { throw "Python 3.10+ not found on PATH. Install it from python.org (tick 'Add to PATH') and run again." }
if ($python) { Write-Ok ("Python: " + (& python --version 2>&1)) }

$npx = Get-Command npx -ErrorAction SilentlyContinue
if (-not $npx -and -not $SkipSelenium) { throw "Node.js (npx) not found. Install Node.js LTS from nodejs.org and run again." }
if ($npx) { Write-Ok ("Node: " + (& node --version 2>&1)) }

$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
            "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
            "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($chrome) { Write-Ok "Chrome: $chrome" } else { Write-Warn2 "Google Chrome not found - the selenium connector needs it." }

# ---------------------------------------------------------------- db-mcp venv
$servers = [ordered]@{}

if (-not $SkipSelenium) {
    $servers['selenium'] = [ordered]@{ command = 'npx'; args = @('-y', '@angiejones/mcp-selenium@latest') }
}

if (-not $SkipDb) {
    Write-Step "Installing the read-only DB connector (connectors\db-mcp)"
    if (-not (Test-Path $VenvPy)) {
        & python -m venv (Join-Path $DbMcp 'venv')
        if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }
    }
    & $VenvPy -m pip install --quiet --upgrade pip
    & $VenvPy -m pip install --quiet -r (Join-Path $DbMcp 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { throw "pip install failed - check your internet/proxy and run again." }
    Write-Ok "db-mcp installed"

    foreach ($name in @('snd-schema', 'selenium-framework-db')) {
        $label = if ($name -eq 'snd-schema') { 'S&D application database' } else { 'framework database (CTA_CONFIG_ASSERTION)' }
        Write-Step "Connection for $name - $label (ask the QA lead / DBA for a read-only login)"
        $dbHost = Read-Value '   Host' ''
        $port   = Read-Value '   Port' '5432'
        $db     = Read-Value '   Database name' ''
        $user   = Read-Value '   Read-only user' ''
        $pwd    = Read-Secret '   Password (hidden)'
        $schema = Read-Value '   Schema owner' 'public'
        if (-not $dbHost -or -not $db -or -not $user -or -not $pwd) { throw "Host, database, user and password are required for $name." }

        $envBlock = [ordered]@{
            DB_TYPE           = 'postgres'
            POSTGRES_HOST     = $dbHost
            POSTGRES_PORT     = $port
            POSTGRES_DATABASE = $db
            POSTGRES_USER     = $user
            POSTGRES_PASSWORD = $pwd
            SCHEMA_OWNER      = $schema
        }

        # Connection test: list a few tables through the real server code.
        Write-Host "   Testing connection..."
        $saved = @{}
        foreach ($k in $envBlock.Keys) { $saved[$k] = [Environment]::GetEnvironmentVariable($k, 'Process'); [Environment]::SetEnvironmentVariable($k, $envBlock[$k], 'Process') }
        Push-Location $DbMcp
        try {
            $out = & $VenvPy -c "from schema_discovery import get_all_table_names; t=get_all_table_names(); print(len(t))" 2>&1
            if ($LASTEXITCODE -eq 0) { Write-Ok "$name connected ($($out | Select-Object -Last 1) tables visible)" }
            else { Write-Warn2 "$name could not connect: $($out | Select-Object -Last 1). Saving anyway - fix the values in the config file later." }
        } finally {
            Pop-Location
            foreach ($k in $saved.Keys) { [Environment]::SetEnvironmentVariable($k, $saved[$k], 'Process') }
        }

        $servers[$name] = [ordered]@{ command = $VenvPy; args = @($Server); env = $envBlock }
    }
}

if ($servers.Count -eq 0) { Write-Warn2 "Nothing to configure."; exit 0 }

# ---------------------------------------------------------------- Claude Desktop config
Write-Step "Writing Claude Desktop config"
$cfgDir  = Join-Path $env:APPDATA 'Claude'
$cfgPath = Join-Path $cfgDir 'claude_desktop_config.json'
if (-not (Test-Path $cfgDir)) { New-Item -ItemType Directory -Path $cfgDir | Out-Null }

$cfg = $null
if (Test-Path $cfgPath) {
    $backup = "$cfgPath.bak-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
    Copy-Item $cfgPath $backup
    Write-Ok "Backup: $backup"
    $raw = Get-Content $cfgPath -Raw
    if (-not [string]::IsNullOrWhiteSpace($raw)) { $cfg = $raw | ConvertFrom-Json }
}
if (-not $cfg) { $cfg = New-Object PSObject }
if (-not ($cfg.PSObject.Properties.Name -contains 'mcpServers')) {
    $cfg | Add-Member -NotePropertyName mcpServers -NotePropertyValue (New-Object PSObject)
}
foreach ($name in $servers.Keys) {
    $value = [PSCustomObject]$servers[$name]
    if ($servers[$name].Contains('env')) { $value.env = [PSCustomObject]$servers[$name].env }
    if ($cfg.mcpServers.PSObject.Properties.Name -contains $name) {
        $cfg.mcpServers.$name = $value
        Write-Ok "updated $name"
    } else {
        $cfg.mcpServers | Add-Member -NotePropertyName $name -NotePropertyValue $value
        Write-Ok "added $name"
    }
}
$json = $cfg | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText($cfgPath, $json, (New-Object Text.UTF8Encoding($false)))
Write-Ok "Saved $cfgPath"

# ---------------------------------------------------------------- Claude Code CLI (optional)
if ($ClaudeCode) {
    Write-Step "Registering for the Claude Code CLI (user scope)"
    $claude = Get-Command claude -ErrorAction SilentlyContinue
    if (-not $claude) { Write-Warn2 "claude CLI not found on PATH - skipped." }
    else {
        foreach ($name in $servers.Keys) {
            & claude mcp remove $name --scope user 2>$null | Out-Null
            $cliArgs = @('mcp', 'add', $name, '--scope', 'user')
            if ($servers[$name].Contains('env')) {
                foreach ($k in $servers[$name].env.Keys) { $cliArgs += @('-e', "$k=$($servers[$name].env[$k])") }
            }
            $cliArgs += '--'
            $cliArgs += $servers[$name].command
            $cliArgs += $servers[$name].args
            & claude @cliArgs | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Ok "claude mcp: $name" } else { Write-Warn2 "claude mcp add failed for $name" }
        }
    }
}

# ---------------------------------------------------------------- done
Write-Step "Done"
Write-Host @"
Next:
  1. Restart the Claude Desktop app (fully quit it from the system tray first).
  2. In a new session, ask: "which connectors does this session have?" -
     selenium, snd-schema and selenium-framework-db should show as connected.
  3. Jira (Atlassian Rovo) is a claude.ai connector, not configured here:
     claude.ai -> Settings -> Connectors -> Atlassian -> Connect, sign in with the
     Atlassian account that can open SDMS tickets, then enable it for the session
     (message box + -> Connectors).
  4. Permissions: open the workspace once and set the mode selector to "Ask permissions"
     (not auto). qa-os\docs\TRAINING_GUIDE.md section 2 has the details.
"@
