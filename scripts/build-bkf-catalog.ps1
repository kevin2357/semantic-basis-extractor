param(
    [Parameter(Mandatory = $true)][string]$ExtractionRoot,
    [Parameter(Mandatory = $true)][string]$ManifestRoot
)

$ErrorActionPreference = 'Stop'

function Join-MetadataValue($value) {
    if ($null -eq $value) { return '' }
    if ($value -is [System.Array]) { return (($value | ForEach-Object { [string]$_ }) -join '; ') }
    return [string]$value
}

function Get-CarelessScore([string]$blob) {
    $score = 0
    $reasons = [System.Collections.Generic.List[string]]::new()
    if ($blob -match '(?i)careless\s*whisper') { $score += 100; $reasons.Add('Careless Whisper phrase') }
    else {
        if ($blob -match '(?i)careless|carel') { $score += 35; $reasons.Add('Careless-like text') }
        if ($blob -match '(?i)whisper|whisp') { $score += 35; $reasons.Add('Whisper-like text') }
    }
    if ($blob -match '(?i)george[ _.-]*michael') { $score += 30; $reasons.Add('George Michael') }
    if ($blob -match '(?i)(^|[^a-z])wham([^a-z]|$)') { $score += 15; $reasons.Add('Wham') }
    if ($blob -match '(?i)\bremix\b|\bre-mix\b|\bmix\b|\bedit\b|\bbootleg\b|\bmashup\b|\bdnb\b|drum.?and.?bass|\bbreaks\b') { $score += 10; $reasons.Add('Remix / DJ text') }
    return [pscustomobject]@{ Score=$score; Reasons=($reasons -join '; ') }
}

function Get-DjScore([string]$blob) {
    $score = 0
    $reasons = [System.Collections.Generic.List[string]]::new()
    if ($blob -match '(?i)(^|[^a-z])graham([^a-z]|$)') { $score += 100; $reasons.Add('Graham') }
    if ($blob -match '(?i)(^|[^a-z0-9])(dnb|d&b|d\s*n\s*b)([^a-z0-9]|$)|drum\s*(and|&|n)?\s*bass') { $score += 70; $reasons.Add('DnB / drum and bass') }
    if ($blob -match '(?i)(^|[^a-z])(breaks|breakbeat|break beat|nu breaks)([^a-z]|$)') { $score += 60; $reasons.Add('breaks / breakbeat') }
    if ($blob -match '(?i)(^|[^a-z])(serato|traktor|rekordbox|virtualdj|virtual dj|ableton|mixxx)([^a-z]|$)') { $score += 45; $reasons.Add('DJ library software') }
    if ($blob -match '(?i)(^|[^a-z])(jungle|liquid funk|neurofunk|jump up)([^a-z]|$)') { $score += 35; $reasons.Add('DnB-adjacent genre') }
    if ($blob -match '(?i)(^|[^a-z])(mixed set|mix set|dj set|live set|mixtape|mix tape)([^a-z]|$)') { $score += 35; $reasons.Add('explicit set / mixtape') }
    if ($blob -match '(?i)(^|[^a-z])(playlist|playlists|crate|crates|record pool)([^a-z]|$)') { $score += 20; $reasons.Add('playlist / DJ crate') }
    if ($blob -match '(?i)(^|[^a-z])(session|sessions|radio show|podcast)([^a-z]|$)') { $score += 20; $reasons.Add('session / broadcast') }
    return [pscustomobject]@{ Score=$score; Reasons=($reasons -join '; ') }
}

New-Item -ItemType Directory -Force -Path $ManifestRoot | Out-Null
$files = @(Get-ChildItem -LiteralPath $ExtractionRoot -File -Recurse -Force -ErrorAction SilentlyContinue)
$manifest = foreach ($file in $files) {
    $relative = $file.FullName.Substring($ExtractionRoot.Length).TrimStart('\')
    [pscustomobject]@{
        OriginalPath = ($relative -replace '\\','/')
        RelativePath = $relative
        RecoveredPath = $file.FullName
        FileName = $file.Name
        Extension = $file.Extension.ToLowerInvariant()
        SizeBytes = $file.Length
        Created = $file.CreationTime
        Modified = $file.LastWriteTime
        Attributes = $file.Attributes
    }
}
$manifest | Sort-Object OriginalPath | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'archive-manifest.csv') -NoTypeInformation -Encoding UTF8

$audioExtensions = @('.mp3','.m4a','.wma','.wav','.flac','.aac','.ogg','.oga','.opus','.aif','.aiff','.ape','.mp2','.m4b')
$shell = New-Object -ComObject Shell.Application
$folderCache = @{}
$audioRows = foreach ($file in ($manifest | Where-Object Extension -in $audioExtensions)) {
    $folderPath = [System.IO.Path]::GetDirectoryName($file.RecoveredPath)
    if (-not $folderCache.ContainsKey($folderPath)) { $folderCache[$folderPath] = $shell.Namespace($folderPath) }
    $folder = $folderCache[$folderPath]
    $item = if ($folder) { $folder.ParseName($file.FileName) } else { $null }
    $title = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Title') } else { '' }
    $artist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Artist') } else { '' }
    $albumArtist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumArtist') } else { '' }
    $album = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumTitle') } else { '' }
    $genre = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Genre') } else { '' }
    $durationRaw = if ($item) { $item.ExtendedProperty('System.Media.Duration') } else { $null }
    $durationSeconds = if ($durationRaw) { [math]::Round(([double]$durationRaw / 10000000),2) } else { $null }
    $blob = "$($file.OriginalPath) $title $artist $albumArtist $album $genre"
    $careless = Get-CarelessScore $blob
    $dj = Get-DjScore $blob
    [pscustomobject]@{
        OriginalPath=$file.OriginalPath; RecoveredPath=$file.RecoveredPath; FileName=$file.FileName
        Extension=$file.Extension; SizeBytes=$file.SizeBytes; Modified=$file.Modified
        Title=$title; Artist=$artist; AlbumArtist=$albumArtist; Album=$album; Genre=$genre
        DurationSeconds=$durationSeconds; CandidateScore=$careless.Score; MatchReasons=$careless.Reasons
        DjCandidateScore=$dj.Score; DjMatchReasons=$dj.Reasons
    }
}
$audioRows | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'audio-manifest.csv') -NoTypeInformation -Encoding UTF8
$audioRows | Where-Object CandidateScore -gt 0 | Sort-Object @{e='CandidateScore';Descending=$true},OriginalPath | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'careless-whisper-candidates.csv') -NoTypeInformation -Encoding UTF8
$audioRows | Where-Object DjCandidateScore -gt 0 | Sort-Object @{e='DjCandidateScore';Descending=$true},OriginalPath | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'graham-dnb-breaks-dj-audio-candidates.csv') -NoTypeInformation -Encoding UTF8

$pathCandidates = foreach ($file in $manifest) {
    $dj = Get-DjScore "$($file.OriginalPath) $($file.FileName)"
    if ($dj.Score -gt 0) { [pscustomobject]@{Score=$dj.Score;Reasons=$dj.Reasons;OriginalPath=$file.OriginalPath;RecoveredPath=$file.RecoveredPath;Extension=$file.Extension;SizeBytes=$file.SizeBytes} }
}
$pathCandidates | Sort-Object @{e='Score';Descending=$true},OriginalPath | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'graham-dnb-breaks-dj-path-candidates.csv') -NoTypeInformation -Encoding UTF8

$libraryExtensions = @('.xml','.plist','.m3u','.m3u8','.wpl','.xspf','.cue','.txt','.csv','.tsv','.json','.nml','.db')
$carelessLibraryHits = [System.Collections.Generic.List[object]]::new()
$djLibraryHits = [System.Collections.Generic.List[object]]::new()
foreach ($file in ($manifest | Where-Object { $_.Extension -in $libraryExtensions -and $_.SizeBytes -le 100MB })) {
    foreach ($match in @(Select-String -LiteralPath $file.RecoveredPath -Pattern 'careless whisper','george michael','wham' -SimpleMatch -ErrorAction SilentlyContinue | Select-Object -First 25)) {
        $carelessLibraryHits.Add([pscustomobject]@{OriginalPath=$file.OriginalPath;RecoveredPath=$file.RecoveredPath;LineNumber=$match.LineNumber;Text=$match.Line.Trim()})
    }
    foreach ($match in @(Select-String -LiteralPath $file.RecoveredPath -Pattern 'graham','dnb','drum and bass','drum & bass','breaks','breakbeat','jungle','mixtape','dj set','serato','traktor','rekordbox','virtualdj' -SimpleMatch -ErrorAction SilentlyContinue | Select-Object -First 50)) {
        $djLibraryHits.Add([pscustomobject]@{OriginalPath=$file.OriginalPath;RecoveredPath=$file.RecoveredPath;LineNumber=$match.LineNumber;Text=$match.Line.Trim()})
    }
}
$carelessLibraryHits | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'careless-whisper-library-hits.csv') -NoTypeInformation -Encoding UTF8
$djLibraryHits | Export-Csv -LiteralPath (Join-Path $ManifestRoot 'graham-dnb-breaks-dj-library-hits.csv') -NoTypeInformation -Encoding UTF8

$summary = @(
    "Catalog generated: $(Get-Date -Format o)"
    "Extracted files: $($manifest.Count)"
    "Extracted bytes: $(($manifest | Measure-Object SizeBytes -Sum).Sum)"
    "Audio files inspected: $($audioRows.Count)"
    "Careless Whisper audio candidates: $(@($audioRows | Where-Object CandidateScore -gt 0).Count)"
    "Careless Whisper library hits: $($carelessLibraryHits.Count)"
    "Graham/DnB/breaks/DJ audio candidates: $(@($audioRows | Where-Object DjCandidateScore -gt 0).Count)"
    "Graham/DnB/breaks/DJ path candidates: $(@($pathCandidates).Count)"
    "Graham/DnB/breaks/DJ library hits: $($djLibraryHits.Count)"
)
$summary | Set-Content -LiteralPath (Join-Path $ManifestRoot 'catalog-summary.txt') -Encoding utf8

$carelessTop = $audioRows | Where-Object CandidateScore -gt 0 | Sort-Object @{e='CandidateScore';Descending=$true} | Select-Object -First 100 CandidateScore,MatchReasons,Title,Artist,Album,OriginalPath,RecoveredPath
$djTop = $audioRows | Where-Object DjCandidateScore -gt 0 | Sort-Object @{e='DjCandidateScore';Descending=$true} | Select-Object -First 200 DjCandidateScore,DjMatchReasons,DurationSeconds,Title,Artist,Album,Genre,OriginalPath,RecoveredPath
$html = @"
<!doctype html><html><head><meta charset="utf-8"><title>Backup XP BKF catalog</title><style>body{font:14px Arial,sans-serif;max-width:1500px;margin:32px auto;color:#222}table{border-collapse:collapse;width:100%;margin:12px 0 28px}th{background:#243447;color:#fff;text-align:left}th,td{padding:6px 8px;border-bottom:1px solid #ddd;vertical-align:top}tr:nth-child(even){background:#f6f7f8}</style></head><body>
<h1>Backup XP BKF catalog</h1><p>$($manifest.Count) extracted files; $($audioRows.Count) audio files inspected.</p>
<h2>Careless Whisper candidates</h2>$(if($carelessTop){$carelessTop|ConvertTo-Html -Fragment}else{'<p>No audio filename or tag candidates matched.</p>'})
<h2>Graham, DnB, breaks and DJ-library candidates</h2>$(if($djTop){$djTop|ConvertTo-Html -Fragment}else{'<p>No audio filename or tag candidates matched.</p>'})
</body></html>
"@
$html | Set-Content -LiteralPath (Join-Path $ManifestRoot 'archive-catalog.html') -Encoding utf8
$summary
