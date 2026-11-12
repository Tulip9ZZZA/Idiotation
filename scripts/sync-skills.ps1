# Syncs the canonical skills (.opencode/skills) into the compatibility
# location (.claude/skills) so the pack works in both OpenCode and Claude Code.
# Run after editing any skill:  powershell -File scripts/sync-skills.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$src = Join-Path $root ".opencode\skills"
$dst = Join-Path $root ".claude\skills"

if (-not (Test-Path $src)) { Write-Error "Source $src not found" }
New-Item -ItemType Directory -Force -Path $dst | Out-Null

Get-ChildItem $src -Directory | ForEach-Object {
    $target = Join-Path $dst $_.Name
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Copy-Item $_.FullName $target -Recurse -Force
    Write-Output "synced $($_.Name)"
}
Write-Output "Done. .claude/skills mirrors .opencode/skills."
