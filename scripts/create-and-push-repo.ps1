#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$ProjectDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$gh = "C:\Program Files\GitHub CLI\gh.exe"

$token = $env:GITHUB_TOKEN
if (-not $token) { $token = $env:GH_TOKEN }
if (-not $token -and (Test-Path (Join-Path $ProjectDir ".gh-token"))) {
    $token = (Get-Content (Join-Path $ProjectDir ".gh-token") -Raw).Trim()
}
if (-not $token) {
    $cred = "protocol=https`nhost=github.com" | git credential fill 2>$null
    if ($cred -match "password=(.+)") { $env:GH_TOKEN = $Matches[1].Trim() }
}

if (-not $token) {
    $err = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    $null = & $gh auth status 2>&1
    $needsLogin = $LASTEXITCODE -ne 0
    $ErrorActionPreference = $err
    if ($needsLogin) {
        Write-Host "GitHub CLI is not logged in. Opening browser for one-time login..."
        & $gh auth login --web --git-protocol https
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}

Set-Location $ProjectDir
git branch -M main 2>$null

$repoName = "study-reminder-service"
$create = & $gh repo create $repoName --public --source=. --remote=origin --push --description "Discord webhook reminders for a weekly class schedule" 2>&1
if ($LASTEXITCODE -ne 0) {
    if ($create -match "already exists") {
        $login = & $gh api user -q .login 2>$null
        if ($login) {
            git remote remove origin 2>$null
            git remote add origin "https://github.com/$login/$repoName.git"
            git push -u origin main
        }
    } else {
        Write-Error $create
        exit 1
    }
}
Write-Host "Done. Repo: https://github.com/$(& $gh api user -q .login)/$repoName"
