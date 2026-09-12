param(
    [Parameter(Mandatory)] [string] $InputFile,
    [Parameter(Mandatory)] [string] $OutputDirectory,
    [string] $Image = 'brandi-song-finder'
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$inputRoot = Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$inputName = Split-Path -Leaf $InputFile

$filters = [ordered]@{
    'tempo-0.94' = 'atempo=0.94'
    'tempo-0.97' = 'atempo=0.97'
    'tempo-1.03' = 'atempo=1.03'
    'tempo-1.06' = 'atempo=1.06'
    'pitch-minus-1-semitone' = 'asetrate=11025*0.943874,aresample=11025,atempo=1.059463'
    'pitch-plus-1-semitone' = 'asetrate=11025*1.059463,aresample=11025,atempo=0.943874'
}

foreach ($entry in $filters.GetEnumerator()) {
    docker run --rm --entrypoint ffmpeg `
        -v "${inputRoot}:/input:ro" -v "${OutputDirectory}:/output" $Image `
        -nostdin -y -v error -i "/input/$inputName" -af $entry.Value -c:a aac -b:a 256k "/output/$($entry.Key).m4a"
}
