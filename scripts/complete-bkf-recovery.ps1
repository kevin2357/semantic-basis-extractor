param(
    [Parameter(Mandatory = $true)][int]$ExtractionProcessId,
    [Parameter(Mandatory = $true)][string]$ExtractionRoot,
    [Parameter(Mandatory = $true)][string]$ManifestRoot,
    [Parameter(Mandatory = $true)][string]$RepositoryRoot
)

$ErrorActionPreference = 'Stop'
$statusPath = Join-Path $ManifestRoot 'recovery-status.log'

function Write-Status([string]$message) {
    "$(Get-Date -Format o) $message" | Add-Content -LiteralPath $statusPath -Encoding utf8
}

try {
    Write-Status "WAITING extraction_process_id=$ExtractionProcessId"
    while (Get-Process -Id $ExtractionProcessId -ErrorAction SilentlyContinue) {
        Start-Sleep -Seconds 30
    }

    $files = @(Get-ChildItem -LiteralPath $ExtractionRoot -Recurse -File -Force -ErrorAction SilentlyContinue)
    $bytes = ($files | Measure-Object Length -Sum).Sum
    Write-Status "EXTRACTION_FINISHED files=$($files.Count) bytes=$bytes"
    if ($files.Count -eq 0) { throw 'Extraction process ended without producing files.' }

    & (Join-Path $RepositoryRoot 'scripts\build-bkf-catalog.ps1') -ExtractionRoot $ExtractionRoot -ManifestRoot $ManifestRoot *>&1 |
        Add-Content -LiteralPath (Join-Path $ManifestRoot 'catalog-build.log') -Encoding utf8
    Write-Status 'CATALOG_FINISHED'

    $candidateRoot = Join-Path $ManifestRoot 'Graham and DJ Library Candidates'
    & (Join-Path $RepositoryRoot 'scripts\find-graham-audio-library-candidates.ps1') `
        -AudioManifestPaths (Join-Path $ManifestRoot 'audio-manifest.csv') `
        -FileManifestPaths (Join-Path $ManifestRoot 'archive-manifest.csv') `
        -OutputDirectory $candidateRoot `
        -LongAudioMinutes 20 *>&1 |
        Add-Content -LiteralPath (Join-Path $ManifestRoot 'candidate-build.log') -Encoding utf8
    Write-Status 'CANDIDATE_REPORTS_FINISHED'

    $junction = 'D:\BackupXPExtract'
    if (Test-Path -LiteralPath $junction) {
        $item = Get-Item -LiteralPath $junction -Force
        if ($item.LinkType -eq 'Junction' -and [string]$item.Target -eq $ExtractionRoot) {
            Remove-Item -LiteralPath $junction -Force
            Write-Status 'REMOVED_TEMP_EXTRACTION_JUNCTION'
        }
    }

    $hardLink = 'D:\BackupXP-source.bkf'
    if (Test-Path -LiteralPath $hardLink) {
        $item = Get-Item -LiteralPath $hardLink -Force
        if ($item.LinkType -eq 'HardLink' -and $item.Length -eq (Get-Item -LiteralPath 'D:\Backup xp.bkf').Length) {
            Remove-Item -LiteralPath $hardLink -Force
            Write-Status 'REMOVED_TEMP_SOURCE_HARDLINK'
        }
    }

    Write-Status 'COMPLETE'
} catch {
    Write-Status "FAILED $($_.Exception.Message)"
    $_ | Out-String | Add-Content -LiteralPath (Join-Path $ManifestRoot 'recovery-failure.log') -Encoding utf8
    exit 1
}
