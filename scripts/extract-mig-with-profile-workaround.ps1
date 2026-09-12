$ErrorActionPreference = 'Stop'

$sids = @(
    'S-1-5-21-2200702986-2626199075-278470708-1002',
    'S-1-5-21-2200702986-2626199075-278470708-1005'
)
$root = 'D:\2026 Extracted Archives\External Drive Jan 2013 Windows Easy Transfer'
$destination = Join-Path $root 'Extracted Remainder Excluding MOD'
$log = Join-Path $root 'usmt-extract-excluding-mod.log'
$status = Join-Path $root 'extraction-excluding-mod-status.txt'
$mig = 'E:\Transfer\Windows Easy Transfer - Items from old computer.MIG'
$usmt = 'C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\User State Migration Tool\amd64\usmtutils.exe'

New-Item -ItemType Directory -Path $destination -Force | Out-Null
"STARTED=$(Get-Date -Format o)" | Set-Content -LiteralPath $status

$profiles = foreach ($sid in $sids) {
    $profileKey = "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$sid"
    $profilePsPath = "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$sid"
    $backup = Join-Path $root "$sid-profile-registry-backup.reg"
    if (-not (Test-Path -LiteralPath $profilePsPath)) {
        throw "Expected profile registry key is missing: $profilePsPath"
    }
    & reg.exe export $profileKey $backup /y | Out-Null
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $backup)) {
        throw "Failed to export profile registry key to $backup"
    }
    [pscustomobject]@{ Sid = $sid; PsPath = $profilePsPath; Backup = $backup; Removed = $false }
}

$usmtExit = 999
try {
    foreach ($profile in $profiles) {
        Remove-Item -LiteralPath $profile.PsPath -Recurse -Force
        $profile.Removed = $true
    }
    & $usmt '/extract' $mig $destination '/e:*.MOD' "/l:$log" '/v:13'
    $usmtExit = $LASTEXITCODE
}
catch {
    "ERROR=$($_.Exception.Message)" | Add-Content -LiteralPath $status
    throw
}
finally {
    foreach ($profile in $profiles) {
        if ($profile.Removed) {
            & reg.exe import $profile.Backup | Out-Null
            if ($LASTEXITCODE -ne 0) {
                "CRITICAL_RESTORE_FAILURE=$($profile.Sid) BACKUP=$($profile.Backup)" | Add-Content -LiteralPath $status
            }
        }
    }
    "FINISHED=$(Get-Date -Format o)" | Add-Content -LiteralPath $status
    "USMT_EXIT_CODE=$usmtExit" | Add-Content -LiteralPath $status
}

exit $usmtExit
