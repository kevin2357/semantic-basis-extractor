$ErrorActionPreference = 'Stop'

$sids = @(
    'S-1-5-21-2200702986-2626199075-278470708-1002',
    'S-1-5-21-2200702986-2626199075-278470708-1005'
)
$destination = 'D:\2026 Extracted Archives\External Drive Jan 2013 Windows Easy Transfer'
$log = Join-Path $destination 'usmt-verify-catalog-workaround.log'
$mig = 'E:\Transfer\Windows Easy Transfer - Items from old computer.MIG'
$usmt = 'C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\User State Migration Tool\amd64\usmtutils.exe'

New-Item -ItemType Directory -Path $destination -Force | Out-Null

$profiles = foreach ($sid in $sids) {
    $profileKey = "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$sid"
    $profilePsPath = "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$sid"
    $backup = Join-Path $destination "$sid-profile-registry-backup.reg"
    if (-not (Test-Path -LiteralPath $profilePsPath)) {
        throw "Expected profile registry key is missing: $profilePsPath"
    }
    & reg.exe export $profileKey $backup /y | Out-Null
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $backup)) {
        throw "Failed to export profile registry key to $backup"
    }
    [pscustomobject]@{ Sid = $sid; PsPath = $profilePsPath; Backup = $backup; Removed = $false }
}

try {
    foreach ($profile in $profiles) {
        Remove-Item -LiteralPath $profile.PsPath -Recurse -Force
        $profile.Removed = $true
    }
    & $usmt '/verify:catalog' $mig "/l:$log" '/v:13'
    $usmtExit = $LASTEXITCODE
}
finally {
    foreach ($profile in $profiles) {
        if ($profile.Removed) {
            & reg.exe import $profile.Backup | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-Error "CRITICAL: automatic profile registry restore failed. Backup: $($profile.Backup)"
            }
        }
    }
}

Write-Output "USMT_EXIT_CODE=$usmtExit"
exit $usmtExit
