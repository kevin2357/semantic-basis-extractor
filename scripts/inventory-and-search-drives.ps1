$ErrorActionPreference = 'Stop'

$outputRoot = 'D:\2026 Extracted Archives\Drive Manifests'
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

$audioExtensions = @('.mp3','.m4a','.wma','.wav','.flac','.aac','.ogg','.oga','.opus','.aif','.aiff','.ape','.mp2','.m4b')
$libraryExtensions = @('.xml','.plist','.m3u','.m3u8','.wpl','.xspf','.cue','.txt','.csv','.tsv','.json')
$searchPattern = '(?i)careless\s*whisper|careless|whisper|george[ _.-]*michael|(^|[^a-z])wham([^a-z]|$)'

function Join-MetadataValue($value) {
    if ($null -eq $value) { return '' }
    if ($value -is [System.Array]) { return (($value | ForEach-Object { [string]$_ }) -join '; ') }
    return [string]$value
}

$allCandidates = [System.Collections.Generic.List[object]]::new()
$allLibraryHits = [System.Collections.Generic.List[object]]::new()
$summaries = [System.Collections.Generic.List[object]]::new()
$shell = New-Object -ComObject Shell.Application

foreach ($drive in @('D','E')) {
    $root = "${drive}:\"
    $manifestPath = Join-Path $outputRoot "$drive-drive-manifest.csv"
    $audioPath = Join-Path $outputRoot "$drive-audio-metadata.csv"
    $statusPath = Join-Path $outputRoot "$drive-scan-status.txt"
    "STARTED=$(Get-Date -Format o)" | Set-Content -LiteralPath $statusPath

    $files = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object {
            if ($drive -eq 'D') { -not $_.FullName.StartsWith('D:\2026 Extracted Archives\',[System.StringComparison]::OrdinalIgnoreCase) }
            else { $true }
        })

    $files | Select-Object FullName,Name,@{n='Extension';e={$_.Extension.ToLowerInvariant()}},Length,CreationTime,LastWriteTime,Attributes |
        Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8

    foreach ($file in $files) {
        if ($file.FullName -match $searchPattern) {
            $allCandidates.Add([pscustomobject]@{Drive=$drive;Kind='Filename/path';Score=80;Reasons='Filename or path text';Title='';Artist='';Album='';FullName=$file.FullName;SizeBytes=$file.Length})
        }
    }

    $audioFiles = @($files | Where-Object Extension -in $audioExtensions | Sort-Object @{e={$_.FullName -match '(?i)\\iTunes\\'};Ascending=$true},FullName)
    $folderCache = @{}
    $audioRows = foreach ($file in $audioFiles) {
        $folderPath = [System.IO.Path]::GetDirectoryName($file.FullName)
        if (-not $folderCache.ContainsKey($folderPath)) { $folderCache[$folderPath] = $shell.Namespace($folderPath) }
        $folder = $folderCache[$folderPath]
        $item = if ($folder) { $folder.ParseName($file.Name) } else { $null }
        $title = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Title') } else { '' }
        $artist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Artist') } else { '' }
        $albumArtist = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumArtist') } else { '' }
        $album = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.AlbumTitle') } else { '' }
        $genre = if ($item) { Join-MetadataValue $item.ExtendedProperty('System.Music.Genre') } else { '' }
        $durationRaw = if ($item) { $item.ExtendedProperty('System.Media.Duration') } else { $null }
        $durationSeconds = if ($durationRaw) { [math]::Round(([double]$durationRaw / 10000000),2) } else { $null }
        $blob = "$($file.FullName) $title $artist $albumArtist $album $genre"
        $score = 0; $reasons = [System.Collections.Generic.List[string]]::new()
        if ($blob -match '(?i)careless\s*whisper') { $score += 100; $reasons.Add('Careless Whisper phrase') }
        else {
            if ($blob -match '(?i)careless') { $score += 35; $reasons.Add('Careless') }
            if ($blob -match '(?i)whisper') { $score += 35; $reasons.Add('Whisper') }
        }
        if ($blob -match '(?i)george[ _.-]*michael') { $score += 30; $reasons.Add('George Michael') }
        if ($blob -match '(?i)(^|[^a-z])wham([^a-z]|$)') { $score += 15; $reasons.Add('Wham') }
        if ($blob -match '(?i)\bremix\b|\bre-mix\b|\bmix\b|\bedit\b|\bbootleg\b|\bmashup\b|\bdnb\b|drum.?and.?bass|\bbreaks\b') { $score += 10; $reasons.Add('Remix/DnB/breaks text') }
        $row = [pscustomobject]@{Drive=$drive;FullName=$file.FullName;Name=$file.Name;Extension=$file.Extension.ToLowerInvariant();SizeBytes=$file.Length;Modified=$file.LastWriteTime;Title=$title;Artist=$artist;AlbumArtist=$albumArtist;Album=$album;Genre=$genre;DurationSeconds=$durationSeconds;CandidateScore=$score;MatchReasons=($reasons -join '; ')}
        if ($score -gt 0) { $allCandidates.Add([pscustomobject]@{Drive=$drive;Kind='Audio metadata/path';Score=$score;Reasons=($reasons -join '; ');Title=$title;Artist=$artist;Album=$album;FullName=$file.FullName;SizeBytes=$file.Length}) }
        $row
    }
    $audioRows | Export-Csv -LiteralPath $audioPath -NoTypeInformation -Encoding UTF8

    $libraryFiles = $files | Where-Object { $_.Extension.ToLowerInvariant() -in $libraryExtensions -and $_.Length -le 100MB }
    foreach ($file in $libraryFiles) {
        $matches = @(Select-String -LiteralPath $file.FullName -Pattern 'careless whisper','george michael','wham' -SimpleMatch -ErrorAction SilentlyContinue | Select-Object -First 10)
        foreach ($match in $matches) {
            $allLibraryHits.Add([pscustomobject]@{Drive=$drive;FullName=$file.FullName;LineNumber=$match.LineNumber;Text=$match.Line.Trim()})
        }
    }

    $summaries.Add([pscustomobject]@{Drive=$drive;Files=$files.Count;Bytes=($files | Measure-Object Length -Sum).Sum;AudioFiles=$audioFiles.Count;LibraryFilesSearched=@($libraryFiles).Count;Finished=(Get-Date)})
    "FINISHED=$(Get-Date -Format o)" | Add-Content -LiteralPath $statusPath
    "FILES=$($files.Count)" | Add-Content -LiteralPath $statusPath
    "AUDIO=$($audioFiles.Count)" | Add-Content -LiteralPath $statusPath
}

$allCandidates | Sort-Object @{e='Score';Descending=$true},Drive,FullName | Export-Csv -LiteralPath (Join-Path $outputRoot 'careless-whisper-candidates-all-drives.csv') -NoTypeInformation -Encoding UTF8
$allLibraryHits | Export-Csv -LiteralPath (Join-Path $outputRoot 'careless-whisper-library-hits.csv') -NoTypeInformation -Encoding UTF8
$summaries | Export-Csv -LiteralPath (Join-Path $outputRoot 'drive-manifest-summary.csv') -NoTypeInformation -Encoding UTF8
$summaries | Format-Table -AutoSize
$allCandidates | Sort-Object @{e='Score';Descending=$true} | Select-Object -First 100 | Format-List
$allLibraryHits | Select-Object -First 100 | Format-List
