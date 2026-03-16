# FPR Skills — Manual Installer for Windows
# Usage: .\install.ps1 [skill-name]    Install one skill
#        .\install.ps1 -All            Install all skills
#        .\install.ps1 -List           List available skills

param(
    [string]$SkillName,
    [switch]$All,
    [switch]$List,
    [switch]$Help
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDir = Join-Path $env:USERPROFILE ".claude\skills"

if (-not (Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
}

function Get-AvailableSkills {
    Get-ChildItem "$ScriptDir\*.skill" | ForEach-Object {
        $name = $_.BaseName
        $size = "{0:N0} KB" -f ($_.Length / 1KB)
        $installed = if (Test-Path (Join-Path $SkillsDir $name)) { " [installed]" } else { "" }
        "  $name ($size)$installed"
    }
}

function Show-List {
    Write-Host "Available FPR skills:" -ForegroundColor Cyan
    Write-Host ""
    Get-AvailableSkills
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\install.ps1 <skill-name>   Install one skill"
    Write-Host "  .\install.ps1 -All           Install all skills"
}

function Install-Skill {
    param([string]$Name)

    $file = Join-Path $ScriptDir "$Name.skill"
    if (-not (Test-Path $file)) {
        Write-Host "Error: skill '$Name' not found" -ForegroundColor Red
        return $false
    }

    $dest = Join-Path $SkillsDir $Name
    if (Test-Path $dest) {
        Write-Host "Updating $Name..." -ForegroundColor Yellow
        Remove-Item $dest -Recurse -Force
    } else {
        Write-Host "Installing $Name..." -ForegroundColor Cyan
    }

    # Create temp dir, extract gzip, then extract tar
    $tempGz = Join-Path $env:TEMP "$Name.tar.gz"
    $tempTar = Join-Path $env:TEMP "$Name.tar"
    $tempExtract = Join-Path $env:TEMP "fpr-skill-$Name"

    Copy-Item $file $tempGz -Force

    # Try tar (available on Windows 10+)
    if (Get-Command tar -ErrorAction SilentlyContinue) {
        New-Item -ItemType Directory -Path $tempExtract -Force | Out-Null
        tar xzf $tempGz -C $tempExtract 2>$null

        # Find the extracted folder and move to destination
        $extracted = Get-ChildItem $tempExtract -Directory | Select-Object -First 1
        if ($extracted) {
            Move-Item $extracted.FullName $dest -Force
        } else {
            # Files extracted directly
            Move-Item $tempExtract $dest -Force
        }
    } else {
        Write-Host "Error: 'tar' command not found. Install Windows 10+ or use Git Bash." -ForegroundColor Red
        return $false
    }

    # Cleanup
    Remove-Item $tempGz -Force -ErrorAction SilentlyContinue
    Remove-Item $tempTar -Force -ErrorAction SilentlyContinue
    Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue

    Write-Host "  > $Name -> $dest" -ForegroundColor Green
    return $true
}

# Main
if ($Help -or ($List) -or (-not $SkillName -and -not $All)) {
    Show-List
} elseif ($All) {
    Write-Host "Installing all FPR skills..." -ForegroundColor Cyan
    Write-Host ""
    Get-ChildItem "$ScriptDir\*.skill" | ForEach-Object {
        Install-Skill -Name $_.BaseName
    }
    Write-Host ""
    Write-Host "Done! Restart Claude Code to activate." -ForegroundColor Green
} else {
    Install-Skill -Name $SkillName
    Write-Host ""
    Write-Host "Done! Restart Claude Code to activate." -ForegroundColor Green
}
