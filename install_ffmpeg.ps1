# Download FFmpeg
$ffmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
$downloadPath = "$env:USERPROFILE\Downloads\ffmpeg.zip"
$ffmpegPath = "$env:USERPROFILE\ffmpeg"

Write-Host "Downloading FFmpeg..."
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $downloadPath

# Create FFmpeg directory if it doesn't exist
if (-not (Test-Path $ffmpegPath)) {
    New-Item -ItemType Directory -Path $ffmpegPath
}

# Extract FFmpeg
Write-Host "Extracting FFmpeg..."
Expand-Archive -Path $downloadPath -DestinationPath $ffmpegPath -Force

# Get the name of the extracted directory
$extractedDir = Get-ChildItem $ffmpegPath | Where-Object { $_.PSIsContainer } | Select-Object -First 1

# Move files from the nested directory to the main ffmpeg directory
Move-Item "$ffmpegPath\$($extractedDir.Name)\bin\*" $ffmpegPath -Force
Remove-Item "$ffmpegPath\$($extractedDir.Name)" -Recurse -Force

# Add FFmpeg to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$ffmpegPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$ffmpegPath", "User")
}

# Clean up
Remove-Item $downloadPath

Write-Host "FFmpeg installation complete!"
Write-Host "Please restart your terminal for the PATH changes to take effect." 