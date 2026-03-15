#Requires -RunAsAdministrator

param(
    [string]$TaskName = "StudyReminderService",
    [string]$PythonPath = "",
    [string]$ProjectDir = ""
)

if (-not $ProjectDir) {
    $ProjectDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $PythonPath) {
        Write-Error "Python not found in PATH. Specify -PythonPath explicitly."
        exit 1
    }
}

Write-Host "Task name   : $TaskName"
Write-Host "Python      : $PythonPath"
Write-Host "Project dir : $ProjectDir"
Write-Host ""

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Task '$TaskName' already exists. Removing it first..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

$action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "-m app.main" `
    -WorkingDirectory $ProjectDir

$trigger = New-ScheduledTaskTrigger -AtLogon

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RestartCount 5 `
    -ExecutionTimeLimit (New-TimeSpan -Days 365)

$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Discord study schedule reminder service (runs continuously)"

Write-Host ""
Write-Host "Task '$TaskName' registered successfully." -ForegroundColor Green
Write-Host "It will start automatically at next logon."
Write-Host "To start it now:  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "To remove it:     Unregister-ScheduledTask -TaskName '$TaskName'"
