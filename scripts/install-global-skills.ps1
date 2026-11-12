<#
.SYNOPSIS
  Installs frequently-used skills at GLOBAL level for OpenCode (and optionally Claude Code):
  brand-skills, logo-design, beautify-github-readme, and Matt Pocock's "Skills For Real Engineers".
.DESCRIPTION
  Global skills load in every OpenCode session and project.
  Target:  ~/.config/opencode/skills  (OpenCode global skill source)
           ~/.claude/skills           (with -AlsoClaude, for Claude Code)
  Every copied pack keeps its MIT license; attributions land in <target>/_credits/.
.PARAMETER ZipsDir
  Folder containing the source packs as GitHub zips (e.g. Downloads).
  Expected zips: brand-skills-main.zip, logo-design-skill-main*.zip,
  beautify-github-readme-main.zip, skills-main.zip
.PARAMETER SourceDir
  Folder containing the packs ALREADY EXTRACTED (one folder per pack).
  Use this OR -ZipsDir, not both.
.PARAMETER AlsoClaude
  Additionally copy the skills to ~/.claude/skills.
#>
param(
    [string]$ZipsDir = "",
    [string]$SourceDir = "",
    [switch]$AlsoClaude
)

$ErrorActionPreference = "Stop"
$work = Join-Path $env:TEMP "idiotation-skill-packs"
$globalTarget = Join-Path $HOME ".config\opencode\skills"
$claudeTarget = Join-Path $HOME ".claude\skills"

# ---- resolve sources -------------------------------------------------------
if ($ZipsDir) {
    if (-not (Test-Path $ZipsDir)) { throw "ZipsDir not found: $ZipsDir" }
    if (Test-Path $work) { Remove-Item $work -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $work | Out-Null
    Get-ChildItem $ZipsDir -Filter "*.zip" | Where-Object {
        $_.Name -match "brand-skills|logo-design-skill|beautify-github-readme|skills-main"
    } | ForEach-Object {
        $out = Join-Path $work ([IO.Path]::GetFileNameWithoutExtension($_.Name) -replace "[^a-zA-Z0-9\-]", "-")
        New-Item -ItemType Directory -Force -Path $out | Out-Null
        Expand-Archive -LiteralPath $_.FullName -DestinationPath $out -Force
        Write-Output "[zip] expanded $($_.Name)"
    }
    $SourceDir = $work
}
if (-not $SourceDir) { throw "Provide -ZipsDir <folder-with-zips> or -SourceDir <folder-with-extracted-packs>" }
if (-not (Test-Path $SourceDir)) { throw "SourceDir not found: $SourceDir" }

function Find-Pack([string]$stem) {
    # prefer a folder that actually contains the skills/ subfolder
    $hits = Get-ChildItem $SourceDir -Directory -Recurse -Depth 3 |
        Where-Object { $_.Name -match $stem -and (Test-Path (Join-Path $_.FullName "skills")) }
    if (-not $hits) {
        $hits = Get-ChildItem $SourceDir -Directory -Recurse -Depth 3 | Where-Object { $_.Name -match $stem }
    }
    return ($hits | Select-Object -First 1)
}

function Copy-SkillFolder([string]$from, [string]$id, [string]$target) {
    $dest = Join-Path $target $id
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
    Copy-Item $from $dest -Recurse -Force
}

function Install-Pack([string]$stem, [string]$subfolder, [string]$prefix, [string]$target) {
    $pack = Find-Pack $stem
    if (-not $pack) { Write-Output "[warn] pack '$stem' not found under $SourceDir"; return }
    if ($subfolder) { $srcRoot = Join-Path $pack.FullName $subfolder } else { $srcRoot = $pack.FullName }
    if (-not (Test-Path $srcRoot)) { Write-Output "[warn] missing $srcRoot"; return }
    Get-ChildItem $srcRoot -Directory | Where-Object {
        Test-Path (Join-Path $_.FullName "SKILL.md")
    } | ForEach-Object {
        $id = if ($prefix) { "$prefix-$($_.Name)" } else { $_.Name }
        Copy-SkillFolder $_.FullName $id $target
        Write-Output "  [global] $id"
    }
}

New-Item -ItemType Directory -Force -Path $globalTarget | Out-Null
Write-Output "== Installing global skills to $globalTarget =="

Write-Output "-- brand-skills (Cofoundy SAC, MIT; naming skill adapted from glacierphonk/naming) --"
Install-Pack "brand-skills" "skills" "" $globalTarget

Write-Output "-- logo-design (kaankiziltug, MIT) --"
Install-Pack "logo-design-skill" "skills" "" $globalTarget

Write-Output "-- beautify-github-readme (oil-oil, MIT) --"
Install-Pack "beautify-github-readme" "skills" "" $globalTarget

Write-Output "-- matt-pocock skills (Matt Pocock, MIT) - engineering + productivity --"
Install-Pack "skills-main" "skills\engineering" "" $globalTarget
Install-Pack "skills-main" "skills\productivity" "" $globalTarget

# ---- attribution -----------------------------------------------------------
$credits = Join-Path $globalTarget "_credits"
New-Item -ItemType Directory -Force -Path $credits | Out-Null
$attribution = @"
# Global skill attributions

Installed at global level by Idiotation (scripts/install-global-skills.ps1).
All packs copied as-is, unmodified, under their MIT licenses.

- brand-skills/* - MIT (c) 2026 Cofoundy SAC (brand-skills repo)
  skills/naming/ adapted from glacierphonk/naming - MIT (c) 2026 GlacierPhonk
  (see the NOTICE file in the brand-skills source repo)
- logo-design - MIT (c) 2026 kaankiziltug (logo-design-skill repo)
- beautify-github-readme - MIT (c) 2026 oil-oil (beautify-github-readme repo)
- engineering/* and productivity/* - MIT (c) 2026 Matt Pocock
  (mattpocock/skills - "Skills For Real Engineers")
"@
Set-Content -Path (Join-Path $credits "ATTRIBUTION.md") -Value $attribution -Encoding utf8

if ($AlsoClaude) {
    Write-Output "== Also installing to $claudeTarget =="
    New-Item -ItemType Directory -Force -Path $claudeTarget | Out-Null
    Install-Pack "brand-skills" "skills" "" $claudeTarget
    Install-Pack "logo-design-skill" "skills" "" $claudeTarget
    Install-Pack "beautify-github-readme" "skills" "" $claudeTarget
    Install-Pack "skills-main" "skills\engineering" "" $claudeTarget
    Install-Pack "skills-main" "skills\productivity" "" $claudeTarget
}

Write-Output ""
Write-Output "Done. New OpenCode sessions (any folder) now advertise these skills."
Write-Output "Tip: run '/reload' in OpenCode, or just start a new session, to pick them up."
