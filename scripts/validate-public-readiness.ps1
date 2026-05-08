param(
    [switch]$VerboseOutput
)

$ErrorActionPreference = "Stop"

function Add-Failure {
    param([string]$Message)
    $script:Failures.Add($Message) | Out-Null
}

function Invoke-Git {
    param([string[]]$Arguments)
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git @Arguments 2>&1
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }
    return [PSCustomObject]@{
        Code = $code
        Output = @($output)
    }
}

$Failures = [System.Collections.Generic.List[string]]::new()
$repoRootResult = Invoke-Git @("rev-parse", "--show-toplevel")
if ($repoRootResult.Code -ne 0) {
    Write-Error "Not inside a Git repository."
}

$repoRoot = ($repoRootResult.Output | Select-Object -First 1).ToString()
Set-Location -LiteralPath $repoRoot

$tracked = @(git ls-files)

if ($tracked.Count -eq 0) {
    Add-Failure "No tracked files found."
}

$sourceDir = Join-Path $repoRoot "sources"
if (Test-Path -LiteralPath $sourceDir) {
    Add-Failure "Local sources/ directory still exists inside the repo root. Move it outside the checkout before publishing."
}

$blockedPathNames = @(
    "andrej-karpathy" + "-skills",
    "matt-pocock" + "-skills",
    "codex" + "-correctness",
    "philosophies" + "_discussions",
    "superpowers"
)

foreach ($file in $tracked) {
    if ($file -eq "scripts/validate-public-readiness.ps1") {
        continue
    }

    foreach ($name in $blockedPathNames) {
        if ($file -eq $name -or $file.StartsWith("$name/")) {
            Add-Failure "Tracked source-corpus path remains: $file"
        }
    }
}

$skillRoot = Join-Path $repoRoot "skills"
$skillNames = [System.Collections.Generic.List[string]]::new()
if (-not (Test-Path -LiteralPath $skillRoot)) {
    Add-Failure "Missing skills/ directory."
} else {
    $skillDirs = @(Get-ChildItem -LiteralPath $skillRoot -Directory)
    foreach ($dir in $skillDirs) {
        $skillFile = Join-Path $dir.FullName "SKILL.md"
        if (-not (Test-Path -LiteralPath $skillFile)) {
            Add-Failure "Skill folder missing SKILL.md: $($dir.Name)"
            continue
        }

        $nameLine = Select-String -LiteralPath $skillFile -Pattern "^name:\s*(.+)\s*$" | Select-Object -First 1
        if ($null -eq $nameLine) {
            Add-Failure "Skill missing frontmatter name: $($dir.Name)"
            continue
        }

        $skillName = $nameLine.Matches[0].Groups[1].Value.Trim()
        if ($skillName -ne $dir.Name) {
            Add-Failure "Skill name mismatch: folder '$($dir.Name)' has name '$skillName'"
        }
        $skillNames.Add($dir.Name) | Out-Null
    }
}

$readmePath = Join-Path $repoRoot "README.md"
if (-not (Test-Path -LiteralPath $readmePath)) {
    Add-Failure "Missing README.md."
} else {
    $readmeText = Get-Content -LiteralPath $readmePath -Raw
    foreach ($skillName in $skillNames) {
        $skillMapPattern = '(?m)^\|\s*`' + [regex]::Escape($skillName) + '`\s*\|'
        if ($readmeText -notmatch $skillMapPattern) {
            Add-Failure "README skill map is missing skill: $skillName"
        }
    }

    $mappedSkills = [regex]::Matches($readmeText, '(?m)^\|\s*`([^`]+)`\s*\|') |
        ForEach-Object { $_.Groups[1].Value }
    foreach ($mappedSkill in $mappedSkills) {
        if (-not $skillNames.Contains($mappedSkill)) {
            Add-Failure "README skill map references missing skill: $mappedSkill"
        }
    }
}

$renamedSkillNames = @(
    ("thin" + "-plan"),
    ("github-work" + "-tracking"),
    ("manage" + "-subagents")
)
$renamedSkillPattern = ($renamedSkillNames | ForEach-Object { [regex]::Escape($_) }) -join "|"
$renamedSkillHits = Invoke-Git @("grep", "-n", "-I", "-E", $renamedSkillPattern, "--", ".")
if ($renamedSkillHits.Code -eq 0) {
    foreach ($hit in $renamedSkillHits.Output) {
        if ($hit -match "^scripts/validate-public-readiness\.ps1:") {
            continue
        }
        Add-Failure "Stale renamed skill reference: $hit"
    }
} elseif ($renamedSkillHits.Code -ne 1) {
    Add-Failure "git grep renamed skill scan failed: $($renamedSkillHits.Output -join ' ')"
}

$referenceFiles = @()
$candidateReferenceFiles = @("README.md", "AGENTS.md")
foreach ($relativePath in $candidateReferenceFiles) {
    $fullPath = Join-Path $repoRoot $relativePath
    if (Test-Path -LiteralPath $fullPath) {
        $referenceFiles += $fullPath
    }
}
if (Test-Path -LiteralPath $skillRoot) {
    $referenceFiles += @(Get-ChildItem -LiteralPath $skillRoot -Recurse -File -Filter "*.md" | ForEach-Object { $_.FullName })
}

$allowedBacktickTerms = @(
    "needs-triage",
    "needs-info",
    "ready-for-agent",
    "ready-for-human",
    "wontfix"
)

foreach ($file in $referenceFiles) {
    $text = Get-Content -LiteralPath $file -Raw
    foreach ($match in [regex]::Matches($text, '`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`')) {
        $term = $match.Groups[1].Value
        if ($skillNames.Contains($term) -or $allowedBacktickTerms.Contains($term)) {
            continue
        }

        $relativeFile = [System.IO.Path]::GetRelativePath($repoRoot, $file)
        Add-Failure "Backtick skill-shaped term does not match a skill folder: $relativeFile -> $term"
    }
}

$localIdentifierPattern = @(
    ("DESK" + "TOP-"),
    ("S-1-5" + "-21"),
    "[A-Z]:\\",
    "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    ("api" + "[_-]?key\s*[:=]"),
    ("sec" + "ret\s*[:=]"),
    ("tok" + "en\s*[:=]"),
    ("pass" + "word\s*[:=]"),
    ("BEGIN (RSA|OPENSSH|PRI" + "VATE)")
) -join "|"
$localHits = Invoke-Git @("grep", "-n", "-I", "-E", $localIdentifierPattern, "--", ".")
if ($localHits.Code -eq 0) {
    foreach ($hit in $localHits.Output) {
        if ($hit -match "^scripts/validate-public-readiness\.ps1:") {
            continue
        }
        Add-Failure "Potential local identifier or secret pattern: $hit"
    }
} elseif ($localHits.Code -ne 1) {
    Add-Failure "git grep local identifier scan failed: $($localHits.Output -join ' ')"
}

$historyResult = Invoke-Git @("rev-list", "--all", "--", $blockedPathNames)
if ($historyResult.Code -ne 0) {
    Add-Failure "Git history path scan failed: $($historyResult.Output -join ' ')"
} elseif ($historyResult.Output.Count -gt 0 -and ($historyResult.Output -join "").Trim().Length -gt 0) {
    Add-Failure "Git history still references removed source-corpus paths: $($historyResult.Output -join ', ')"
}

$objectsResult = Invoke-Git @("rev-list", "--objects", "--all")
if ($objectsResult.Code -ne 0) {
    Add-Failure "Git object path scan failed: $($objectsResult.Output -join ' ')"
} else {
    $objectPattern = "(^| )(" + (($blockedPathNames | ForEach-Object { [regex]::Escape($_) }) -join "|") + ")(/|$)"
    foreach ($line in $objectsResult.Output) {
        if ($line -match $objectPattern) {
            Add-Failure "Git object path still references source corpus: $line"
        }
    }
}

$diffCheck = Invoke-Git @("diff", "--check")
if ($diffCheck.Code -ne 0) {
    Add-Failure "Working-tree whitespace check failed: $($diffCheck.Output -join ' ')"
}

if ($VerboseOutput) {
    Write-Host "Tracked files: $($tracked.Count)"
    Write-Host "Skill folders: $((Get-ChildItem -LiteralPath $skillRoot -Directory -ErrorAction SilentlyContinue | Measure-Object).Count)"
}

if ($Failures.Count -gt 0) {
    Write-Host "Public readiness check failed:"
    foreach ($failure in $Failures) {
        Write-Host "- $failure"
    }
    exit 1
}

Write-Host "Public readiness check passed."
