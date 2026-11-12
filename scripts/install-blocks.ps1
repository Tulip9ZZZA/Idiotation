<#
.SYNOPSIS
  Clones the five Idiotation blocks into blocks/ (gitignored, optional at runtime).
.DESCRIPTION
  Each block is cloned per its own repo. Blocks are EXTERNAL dependencies:
  - firecrawl is AGPL-3.0 -> never vendored into your own repo; used as an external API/MCP.
  - llm-council has NO license -> clone only for the visual web app; the Idiotation
    council protocol runs natively without it.
.NOTES
  Firecrawl key (optional, for hosted API): set FIRECRAWL_API_KEY env var,
  or add the Firecrawl MCP server:
    opencode mcp add firecrawl --global --url https://mcp.firecrawl.dev/<your-key>/v2.0/mcp
#>
param(
    [string]$BlocksDir = (Join-Path (Split-Path -Parent $PSScriptRoot) "blocks")
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $BlocksDir | Out-Null

$repos = @(
    @{ name = "firecrawl";     url = "https://github.com/firecrawl/firecrawl";            branch = $null; license = "AGPL-3.0 (external tool only, never vendored)" },
    @{ name = "superpowers";   url = "https://github.com/obra/superpowers";               branch = $null; license = "MIT" },
    @{ name = "maxxing-itout"; url = "https://github.com/Tulip9ZZZA/maxxing-itout";       branch = "v2-gauntlet"; license = "MIT" },
    @{ name = "roast-room";    url = "https://github.com/nateherkai/roast-room";          branch = $null; license = "MIT" },
    @{ name = "llm-council";   url = "https://github.com/karpathy/llm-council";           branch = $null; license = "NONE - clone for the visual app only; no code/text copied into Idiotation" }
)

foreach ($r in $repos) {
    $dest = Join-Path $BlocksDir $r.name
    if (Test-Path $dest) {
        Write-Output "[skip] $($r.name) already present"
        continue
    }
    Write-Output "[clone] $($r.name) ($($r.license))"
    if ($r.branch) {
        git clone --depth 1 -b $r.branch $r.url $dest
    } else {
        git clone --depth 1 $r.url $dest
    }
}

Write-Output ""
Write-Output "Done. Blocks live in $BlocksDir (gitignored)."
Write-Output "All skills work WITHOUT the blocks - each SKILL.md embeds a native fallback."
