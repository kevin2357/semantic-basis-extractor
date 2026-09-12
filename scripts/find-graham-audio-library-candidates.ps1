param(
    [Parameter(Mandatory = $true)]
    [string[]]$AudioManifestPaths,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,

    [string[]]$FileManifestPaths = @(),

    [int]$LongAudioMinutes = 20
)

$ErrorActionPreference = 'Stop'

function Get-TextScore {
    param([string]$Text, [bool]$IsITunes)
    $score = 0
    $reasons = [System.Collections.Generic.List[string]]::new()
    if ($Text -match '(?i)(^|[^a-z])graham([^a-z]|$)') { $score += 100; $reasons.Add('Graham') }
    if ($Text -match '(?i)(^|[^a-z0-9])(dnb|d&b|d\s*n\s*b)([^a-z0-9]|$)|drum\s*(and|&|n)?\s*bass') { $score += 70; $reasons.Add('DnB / drum and bass') }
    if ($Text -match '(?i)(^|[^a-z])(breaks|breakbeat|break beat|nu breaks)([^a-z]|$)') { $score += 60; $reasons.Add('breaks / breakbeat') }
    if ($Text -match '(?i)(^|[^a-z])(mixed set|mix set|dj set|live set|mixtape|mix tape)([^a-z]|$)') { $score += 35; $reasons.Add('explicit set / mixtape') }
    if ($Text -match '(?i)(^|[^a-z])(session|sessions|radio show|podcast)([^a-z]|$)') { $score += 20; $reasons.Add('session / broadcast') }
    if ($Text -match '(?i)(^|[^a-z])(dj|mix|mixed|live)([^a-z]|$)') { $score += 8; $reasons.Add('DJ / mix / live') }
    if ($IsITunes) { $score -= 15; $reasons.Add('iTunes lower priority') }
    [pscustomobject]@{ Score = $score; Reasons = ($reasons -join '; ') }
}

function Get-Ancestors {
    param([string]$Path, [int]$Maximum = 5)
    $result = [System.Collections.Generic.List[string]]::new()
    $current = [System.IO.Path]::GetDirectoryName($Path)
    for ($i = 0; $i -lt $Maximum -and $current; $i++) {
        $result.Add($current)
        $parent = [System.IO.Path]::GetDirectoryName($current)
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }
    return $result
}

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$audio = foreach ($manifest in $AudioManifestPaths) {
    if (Test-Path -LiteralPath $manifest) { Import-Csv -LiteralPath $manifest }
}

$normalized = foreach ($row in $audio) {
    $isArchiveRow = -not [string]::IsNullOrWhiteSpace([string]$row.OriginalPath)
    $fullName = if ($isArchiveRow) { [string]$row.OriginalPath } else { [string]$row.FullName }
    $accessiblePath = if ($isArchiveRow) { [string]$row.RecoveredPath } else { $fullName }
    $name = if ($isArchiveRow) { [string]$row.FileName } else { [string]$row.Name }
    $isITunes = $fullName -match '(?i)\\itunes(\\|$)'
    $text = @($fullName, $name, $row.Title, $row.Artist, $row.AlbumArtist, $row.Album, $row.Genre) -join ' '
    $signal = Get-TextScore -Text $text -IsITunes $isITunes
    [pscustomobject]@{
        Source = if ($isArchiveRow) { 'January 2013 migration archive' } else { "$($row.Drive): drive" }
        Drive = if ($isArchiveRow) { 'Archive' } else { $row.Drive }
        FullName = $fullName
        AccessiblePath = $accessiblePath
        Name = $name
        Extension = $row.Extension
        SizeBytes = [int64]$row.SizeBytes
        Modified = $row.Modified
        Title = $row.Title
        Artist = $row.Artist
        AlbumArtist = $row.AlbumArtist
        Album = $row.Album
        Genre = $row.Genre
        DurationSeconds = [double]$row.DurationSeconds
        IsITunes = $isITunes
        SignalScore = $signal.Score
        MatchReasons = $signal.Reasons
    }
}

$evidence = $normalized | Where-Object { $_.SignalScore -gt 0 } | Sort-Object @{Expression='SignalScore';Descending=$true}, @{Expression='DurationSeconds';Descending=$true}

$folderRows = foreach ($track in $normalized) {
    $depth = 0
    foreach ($folder in (Get-Ancestors -Path $track.FullName -Maximum 5)) {
        $depth++
        [pscustomobject]@{ Folder = $folder; DepthFromFile = $depth; Track = $track }
    }
}

$folderCandidates = foreach ($group in ($folderRows | Group-Object Folder)) {
    $tracks = @($group.Group.Track)
    $folder = $group.Name
    $isITunes = $folder -match '(?i)\\itunes(\\|$)'
    $folderSignal = Get-TextScore -Text $folder -IsITunes $isITunes
    $keywordTracks = @($tracks | Where-Object { $_.SignalScore -gt 0 })
    $longTracks = @($tracks | Where-Object { $_.DurationSeconds -ge ($LongAudioMinutes * 60) })
    $audioCount = $tracks.Count
    $bytes = ($tracks | Measure-Object SizeBytes -Sum).Sum
    $seconds = ($tracks | Measure-Object DurationSeconds -Sum).Sum
    $genres = ($tracks | Where-Object Genre | Group-Object Genre | Sort-Object Count -Descending | Select-Object -First 5 -ExpandProperty Name) -join '; '
    $formatCount = ($tracks | Group-Object Extension).Count
    $collectionScore = $folderSignal.Score
    $reasons = [System.Collections.Generic.List[string]]::new()
    if ($folderSignal.Reasons) { $reasons.Add($folderSignal.Reasons) }
    if ($keywordTracks.Count -gt 0) { $collectionScore += [math]::Min(40, $keywordTracks.Count * 3); $reasons.Add("$($keywordTracks.Count) signal track(s)") }
    if ($longTracks.Count -gt 0) { $collectionScore += [math]::Min(30, $longTracks.Count * 5); $reasons.Add("$($longTracks.Count) long track(s)") }
    if ($audioCount -ge 100) { $collectionScore += 25; $reasons.Add("$audioCount audio files") }
    elseif ($audioCount -ge 25) { $collectionScore += 12; $reasons.Add("$audioCount audio files") }
    if ($seconds -ge 36000) { $collectionScore += 20; $reasons.Add(('{0:N1} total hours' -f ($seconds / 3600))) }
    elseif ($seconds -ge 18000) { $collectionScore += 10; $reasons.Add(('{0:N1} total hours' -f ($seconds / 3600))) }
    if ($isITunes) { $collectionScore -= 20 }

    if ($folderSignal.Score -gt 0 -or $keywordTracks.Count -gt 0 -or $longTracks.Count -ge 2 -or $audioCount -ge 25) {
        [pscustomobject]@{
            RankScore = $collectionScore
            LocationPriority = if ($isITunes) { 'iTunes backstop' } else { 'Non-iTunes priority' }
            Folder = $folder
            AudioFiles = $audioCount
            LongAudioFiles = $longTracks.Count
            SignalTracks = $keywordTracks.Count
            TotalHours = [math]::Round($seconds / 3600, 2)
            TotalGB = [math]::Round($bytes / 1GB, 3)
            Formats = (($tracks | Group-Object Extension | Sort-Object Count -Descending | ForEach-Object { "$($_.Name) ($($_.Count))" }) -join '; ')
            LeadingGenres = $genres
            EarliestModified = ($tracks | Sort-Object { [datetime]$_.Modified } | Select-Object -First 1 -ExpandProperty Modified)
            LatestModified = ($tracks | Sort-Object { [datetime]$_.Modified } -Descending | Select-Object -First 1 -ExpandProperty Modified)
            Evidence = ($reasons -join '; ')
        }
    }
}

$folderCandidates = $folderCandidates | Sort-Object @{Expression={ if ($_.LocationPriority -eq 'Non-iTunes priority') { 0 } else { 1 } }}, @{Expression='RankScore';Descending=$true}, @{Expression='AudioFiles';Descending=$true}

$filesets = foreach ($group in ($normalized | Group-Object { [System.IO.Path]::GetDirectoryName($_.FullName) })) {
    $tracks = @($group.Group)
    $folder = $group.Name
    $isITunes = $folder -match '(?i)\\itunes(\\|$)'
    $folderSignal = Get-TextScore -Text ($folder + ' ' + (($tracks | Select-Object -ExpandProperty Album -Unique) -join ' ')) -IsITunes $isITunes
    $longTracks = @($tracks | Where-Object { $_.DurationSeconds -ge ($LongAudioMinutes * 60) })
    $signalTracks = @($tracks | Where-Object { $_.SignalScore -gt 0 })
    $seconds = ($tracks | Measure-Object DurationSeconds -Sum).Sum
    $bytes = ($tracks | Measure-Object SizeBytes -Sum).Sum
    $score = $folderSignal.Score + [math]::Min(45, $signalTracks.Count * 5) + [math]::Min(35, $longTracks.Count * 8)
    if ($tracks.Count -ge 10) { $score += 10 }
    if ($isITunes) { $score -= 15 }
    if ($folderSignal.Score -gt 0 -or $signalTracks.Count -gt 0 -or $longTracks.Count -gt 0) {
        $evidenceParts = [System.Collections.Generic.List[string]]::new()
        if ($folderSignal.Reasons) { $evidenceParts.Add($folderSignal.Reasons) }
        foreach ($reason in ($signalTracks.MatchReasons | Where-Object { $_ } | Select-Object -Unique)) {
            if (-not $evidenceParts.Contains([string]$reason)) { $evidenceParts.Add([string]$reason) }
        }
        [pscustomobject]@{
            RankScore = $score
            LocationPriority = if ($isITunes) { 'iTunes backstop' } else { 'Non-iTunes priority' }
            Folder = $folder
            AudioFiles = $tracks.Count
            LongAudioFiles = $longTracks.Count
            SignalTracks = $signalTracks.Count
            TotalHours = [math]::Round($seconds / 3600, 2)
            TotalMB = [math]::Round($bytes / 1MB, 1)
            AlbumValues = (($tracks | Select-Object -ExpandProperty Album -Unique | Where-Object { $_ } | Select-Object -First 8) -join '; ')
            Artists = (($tracks | Select-Object -ExpandProperty Artist -Unique | Where-Object { $_ } | Select-Object -First 8) -join '; ')
            Evidence = ($evidenceParts -join '; ')
        }
    }
}

$filesets = $filesets | Sort-Object @{Expression={ if ($_.LocationPriority -eq 'Non-iTunes priority') { 0 } else { 1 } }}, @{Expression='RankScore';Descending=$true}, @{Expression='TotalHours';Descending=$true}

$longAudio = foreach ($track in ($normalized | Where-Object { $_.DurationSeconds -ge ($LongAudioMinutes * 60) })) {
    $score = $track.SignalScore + [math]::Min(40, [math]::Floor($track.DurationSeconds / 900))
    if ($track.IsITunes) { $score -= 15 }
    [pscustomobject]@{
        RankScore = $score
        LocationPriority = if ($track.IsITunes) { 'iTunes backstop' } else { 'Non-iTunes priority' }
        FullName = $track.FullName
        AccessiblePath = $track.AccessiblePath
        DurationMinutes = [math]::Round($track.DurationSeconds / 60, 1)
        SizeMB = [math]::Round($track.SizeBytes / 1MB, 1)
        Title = $track.Title
        Artist = $track.Artist
        Album = $track.Album
        Genre = $track.Genre
        Modified = $track.Modified
        Evidence = $track.MatchReasons
    }
}

$longAudio = $longAudio | Sort-Object @{Expression={ if ($_.LocationPriority -eq 'Non-iTunes priority') { 0 } else { 1 } }}, @{Expression='RankScore';Descending=$true}, @{Expression='DurationMinutes';Descending=$true}

$containerExtensions = @('.zip', '.rar', '.7z', '.bkf', '.iso', '.img', '.tar', '.gz', '.cab', '.mig')
$containers = foreach ($manifest in $FileManifestPaths) {
    if (-not (Test-Path -LiteralPath $manifest)) { continue }
    foreach ($row in (Import-Csv -LiteralPath $manifest)) {
        $extension = ([string]$row.Extension).ToLowerInvariant()
        if ($containerExtensions -notcontains $extension) { continue }
        $bytes = [int64]$row.Length
        $signal = Get-TextScore -Text ([string]$row.FullName) -IsITunes $false
        if ($bytes -lt 100MB -and $signal.Score -le 0) { continue }
        $score = $signal.Score + [math]::Min(50, [math]::Floor($bytes / 1GB) * 2)
        [pscustomobject]@{
            RankScore = $score
            FullName = $row.FullName
            Extension = $extension
            SizeGB = [math]::Round($bytes / 1GB, 2)
            LastWriteTime = $row.LastWriteTime
            Evidence = if ($signal.Reasons) { $signal.Reasons } else { 'Large archive / backup container; contents not represented by filename' }
        }
    }
}
$containers = $containers | Sort-Object @{Expression='RankScore';Descending=$true}, @{Expression='SizeGB';Descending=$true}

$summary = [pscustomobject]@{
    Generated = (Get-Date).ToString('s')
    AudioFilesScanned = $normalized.Count
    FolderCandidates = @($folderCandidates).Count
    FilesetCandidates = @($filesets).Count
    LongAudioCandidates = @($longAudio).Count
    KeywordEvidenceTracks = @($evidence).Count
    LargeContainerCandidates = @($containers).Count
    LongAudioThresholdMinutes = $LongAudioMinutes
    Note = 'Non-iTunes results sort first. Scores rank search leads; they do not establish ownership.'
}

$folderCandidates | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-folder-candidates.csv') -NoTypeInformation -Encoding UTF8
$filesets | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-fileset-candidates.csv') -NoTypeInformation -Encoding UTF8
$longAudio | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-long-audio-candidates.csv') -NoTypeInformation -Encoding UTF8
$evidence | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-keyword-evidence.csv') -NoTypeInformation -Encoding UTF8
$summary | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-summary.csv') -NoTypeInformation -Encoding UTF8
$containers | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'graham-library-large-container-candidates.csv') -NoTypeInformation -Encoding UTF8

$summary | Format-List
$folderCandidates | Select-Object -First 20 | Format-Table -AutoSize
