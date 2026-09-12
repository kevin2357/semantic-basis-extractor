$ErrorActionPreference = 'Stop'

$catalogRoot = 'D:\2026 Extracted Archives\External Drive Jan 2013 Windows Easy Transfer'
$mainRoot = Join-Path $catalogRoot 'Extracted Files\USMT'
$remainderRoot = Join-Path $catalogRoot 'Extracted Remainder Excluding MOD\USMT'
$allCsv = Join-Path $catalogRoot 'archive-manifest.csv'
$audioCsv = Join-Path $catalogRoot 'audio-manifest.csv'
$candidateCsv = Join-Path $catalogRoot 'careless-whisper-candidates.csv'
$corruptCsv = Join-Path $catalogRoot 'corrupt-or-unrecoverable-items.csv'
$htmlPath = Join-Path $catalogRoot 'archive-catalog.html'
$summaryPath = Join-Path $catalogRoot 'catalog-summary.txt'

function Get-OriginalPath([string]$relativePath) {
    $normalized = $relativePath -replace '/', '\'
    if ($normalized -match '^File\\([A-Za-z])\$\\(.*)$') {
        return "$($Matches[1]):\$($Matches[2])"
    }
    if ($normalized -match '^([A-Za-z])_\\(.*)$') {
        return "$($Matches[1]):\$($Matches[2])"
    }
    return $normalized
}

function Join-MetadataValue($value) {
    if ($null -eq $value) { return '' }
    if ($value -is [System.Array]) { return (($value | ForEach-Object { [string]$_ }) -join '; ') }
    return [string]$value
}

$chosen = [System.Collections.Generic.List[object]]::new()

# The second pass is complete for every named non-MOD item. The first pass is
# authoritative for MOD files recovered before the single damaged MOD member.
Get-ChildItem -LiteralPath $remainderRoot -File -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object Extension -ne '.MOD' |
    ForEach-Object {
        $rel = $_.FullName.Substring($remainderRoot.Length).TrimStart('\')
        $chosen.Add([pscustomobject]@{
            OriginalPath = Get-OriginalPath $rel
            RelativePath = $rel
            RecoveredPath = $_.FullName
            FileName = $_.Name
            Extension = $_.Extension.ToLowerInvariant()
            SizeBytes = $_.Length
            Created = $_.CreationTime
            Modified = $_.LastWriteTime
            RecoverySource = 'Non-MOD recovery pass'
        })
    }

Get-ChildItem -LiteralPath $mainRoot -File -Recurse -Force -Filter '*.MOD' -ErrorAction SilentlyContinue |
    ForEach-Object {
        $rel = $_.FullName.Substring($mainRoot.Length).TrimStart('\')
        $chosen.Add([pscustomobject]@{
            OriginalPath = Get-OriginalPath $rel
            RelativePath = $rel
            RecoveredPath = $_.FullName
            FileName = $_.Name
            Extension = $_.Extension.ToLowerInvariant()
            SizeBytes = $_.Length
            Created = $_.CreationTime
            Modified = $_.LastWriteTime
            RecoverySource = 'Main recovery pass (MOD)'
        })
    }

$manifest = $chosen | Sort-Object OriginalPath
$manifest | Export-Csv -LiteralPath $allCsv -NoTypeInformation -Encoding utf8BOM

$audioExtensions = @('.mp3','.m4a','.wma','.wav','.flac','.aac','.ogg','.oga','.opus','.aif','.aiff','.ape','.mp2','.m4b')
$audioFiles = $manifest | Where-Object Extension -in $audioExtensions
$shell = New-Object -ComObject Shell.Application
$folderCache = @{}
$audioRows = foreach ($file in $audioFiles) {
    $folderPath = [System.IO.Path]::GetDirectoryName($file.RecoveredPath)
    if (-not $folderCache.ContainsKey($folderPath)) {
        $folderCache[$folderPath] = $shell.Namespace($folderPath)
    }
    $folder = $folderCache[$folderPath]
    $item = if ($folder) { $folder.ParseName($file.FileName) } else { $null }
    $title = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Title') } else { '' }
    $artist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Artist') } else { '' }
    $albumArtist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumArtist') } else { '' }
    $album = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumTitle') } else { '' }
    $genre = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Genre') } else { '' }
    $durationRaw = if ($item) { $item.ExtendedProperty('System.Media.Duration') } else { $null }
    $durationSeconds = if ($durationRaw) { [math]::Round(([double]$durationRaw / 10000000), 2) } else { $null }
    $blob = "$($file.OriginalPath) $title $artist $albumArtist $album $genre"
    $score = 0
    $reasons = [System.Collections.Generic.List[string]]::new()
    if ($blob -match '(?i)careless\s*whisper') { $score += 100; $reasons.Add('Careless Whisper phrase') }
    else {
        if ($blob -match '(?i)careless|carel') { $score += 35; $reasons.Add('Careless-like text') }
        if ($blob -match '(?i)whisper|whisp') { $score += 35; $reasons.Add('Whisper-like text') }
    }
    if ($blob -match '(?i)george[ _.-]*michael') { $score += 30; $reasons.Add('George Michael') }
    if ($blob -match '(?i)(^|[^a-z])wham([^a-z]|$)') { $score += 15; $reasons.Add('Wham') }
    if ($blob -match '(?i)\bremix\b|\bre-mix\b|\bmix\b|\bedit\b|\bbootleg\b|\bmashup\b|\bdnb\b|drum.?and.?bass|\bbreaks\b') { $score += 10; $reasons.Add('Remix/DnB/breaks text') }
    [pscustomobject]@{
        OriginalPath = $file.OriginalPath
        RecoveredPath = $file.RecoveredPath
        FileName = $file.FileName
        Extension = $file.Extension
        SizeBytes = $file.SizeBytes
        Modified = $file.Modified
        Title = $title
        Artist = $artist
        AlbumArtist = $albumArtist
        Album = $album
        Genre = $genre
        DurationSeconds = $durationSeconds
        CandidateScore = $score
        MatchReasons = ($reasons -join '; ')
    }
}

$audioRows | Export-Csv -LiteralPath $audioCsv -NoTypeInformation -Encoding utf8BOM
$candidates = $audioRows | Where-Object CandidateScore -gt 0 | Sort-Object @{ Expression = 'CandidateScore'; Descending = $true }, OriginalPath
$candidates | Export-Csv -LiteralPath $candidateCsv -NoTypeInformation -Encoding utf8BOM

@(
    [pscustomobject]@{ Item='C:\MyWorks\EverioBackup\25214a6595a5\PRG004\MOV086_1.MOD'; Status='CORRUPTED; USMT crashed when reading payload'; Recovery='Not recovered'; SourceLog='usmt-extract.log' }
    [pscustomobject]@{ Item='unknown(1)'; Status='CORRUPTED unnamed catalog member; USMT crashed during finalization'; Recovery='No recoverable pathname'; SourceLog='usmt-extract-excluding-mod.log' }
) | Export-Csv -LiteralPath $corruptCsv -NoTypeInformation -Encoding utf8BOM

$extensionSummary = $manifest | Group-Object Extension | Sort-Object Count -Descending | Select-Object Name,Count,@{n='Bytes';e={($_.Group | Measure-Object SizeBytes -Sum).Sum}}
$summary = @(
    "Catalog generated: $(Get-Date -Format o)"
    "Logical recovered files: $($manifest.Count)"
    "Logical recovered bytes: $(($manifest | Measure-Object SizeBytes -Sum).Sum)"
    "Audio files inspected: $($audioRows.Count)"
    "Ranked candidates: $($candidates.Count)"
    'Known unrecoverable named files: 1'
    'Known corrupt unnamed members: 1'
)
$summary | Set-Content -LiteralPath $summaryPath -Encoding utf8

$candidateHtml = if ($candidates.Count) {
    $candidates | Select-Object CandidateScore,MatchReasons,Title,Artist,Album,OriginalPath,RecoveredPath |
        ConvertTo-Html -Fragment
} else { '<p>No filename or embedded-tag candidates matched.</p>' }
$extensionHtml = $extensionSummary | Select-Object Name,Count,Bytes | ConvertTo-Html -Fragment
$html = @"
<!doctype html><html><head><meta charset="utf-8"><title>January 2013 archive catalog</title>
<style>body{font:14px Arial,sans-serif;max-width:1400px;margin:32px auto;color:#222}table{border-collapse:collapse;width:100%;margin:12px 0 28px}th{background:#243447;color:#fff;text-align:left}th,td{padding:6px 8px;border-bottom:1px solid #ddd;vertical-align:top}tr:nth-child(even){background:#f6f7f8}code{font-size:12px}a{color:#075985}</style></head><body>
<h1>January 2013 Windows Easy Transfer archive</h1>
<p>Recovered $($manifest.Count) logical files. Inspected $($audioRows.Count) audio files. One named MOD video and one unnamed catalog member were corrupt.</p>
<h2>Careless Whisper candidates</h2>$candidateHtml
<h2>File types</h2>$extensionHtml
<h2>Downloadable manifests</h2><ul><li>archive-manifest.csv</li><li>audio-manifest.csv</li><li>careless-whisper-candidates.csv</li><li>corrupt-or-unrecoverable-items.csv</li></ul>
</body></html>
"@
$html | Set-Content -LiteralPath $htmlPath -Encoding utf8

Get-Content -LiteralPath $summaryPath
if ($candidates.Count) { $candidates | Select-Object -First 25 | Format-List }
