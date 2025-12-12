
Finances
Description
Finances is a financial literacy app developed during the BlackRock hackathon. It aims to address real-life financial literacy challenges.

Installation
Ensure that you have Node.js installed on your system.

Clone the repository to your local machine:

bash
Copy code
git clone <repository-url>
Navigate to the project directory in your terminal:

bash
Copy code
cd finances
Install the necessary dependencies:

Copy code
npm install
Install nodemon globally if not already installed:

Copy code
npm install -g nodemon
Usage
To start the project, use the following command:

sql
Copy code
npm start
This will execute the start script defined in the package.json file.

















param(
    # CHANGE THESE TWO PATHS TO YOURS
    [string]$SourcePath      = "\\nas-prod\bankfiles\incoming",
    [string]$DestinationPath = "X:\YourWorkspace\YourLakehouse\Files\other_files\raw",
    [string]$Filter          = "*.*"        # e.g. "*.csv" if you only expect CSVs
)

# ---------- Helper: Wait until file is fully written ----------
function Wait-FileReady {
    param(
        [string]$FilePath,
        [int]$TimeoutSeconds = 300,
        [int]$SleepMillis = 500
    )

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $lastSize = -1

    while ($stopwatch.Elapsed.TotalSeconds -lt $TimeoutSeconds) {
        if (-not (Test-Path $FilePath)) {
            Start-Sleep -Milliseconds $SleepMillis
            continue
        }

        try {
            $fileInfo = Get-Item $FilePath -ErrorAction Stop
            $currentSize = $fileInfo.Length

            if ($currentSize -eq $lastSize -and $currentSize -gt 0) {
                # Size stable for one interval = assume done writing
                return $true
            }

            $lastSize = $currentSize
            Start-Sleep -Milliseconds $SleepMillis
        }
        catch {
            Start-Sleep -Milliseconds $SleepMillis
        }
    }

    Write-Warning "Timeout waiting for file to be ready: $FilePath"
    return $false
}

# ---------- Ensure paths exist ----------
if (-not (Test-Path $SourcePath)) {
    throw "SourcePath does not exist: $SourcePath"
}

if (-not (Test-Path $DestinationPath)) {
    Write-Host "DestinationPath does not exist, creating: $DestinationPath"
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}

Write-Host "Watching $SourcePath for new files matching '$Filter'"
Write-Host "Copying to: $DestinationPath"
Write-Host ""

# ---------- Create FileSystemWatcher ----------
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $SourcePath
$watcher.Filter = $Filter
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

# Optional: log file
$logFile = Join-Path $PSScriptRoot "NasToBronzeWatcher.log"

function Write-Log {
    param([string]$Message)
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $line = "[$timestamp] $Message"
    Write-Host $line
    Add-Content -Path $logFile -Value $line
}

# ---------- Action when file created or changed ----------
$action = {
    param($Source, $EventArgs)

    $fullPath = $EventArgs.FullPath
    $name = $EventArgs.Name

    Write-Log "Detected event '$($EventArgs.ChangeType)' for file: $fullPath"

    if (-not (Wait-FileReady -FilePath $fullPath)) {
        Write-Log "File not ready, skipping: $fullPath"
        return
    }

    $destFile = Join-Path $DestinationPath $name

    try {
        # Copy to OneLake bronze
        Copy-Item -Path $fullPath -Destination $destFile -Force
        Write-Log "Copied '$fullPath' -> '$destFile'"
    }
    catch {
        Write-Log "ERROR copying '$fullPath' -> '$destFile': $($_.Exception.Message)"
    }
}

# ---------- Register events ----------
$createdReg = Register-ObjectEvent -InputObject $watcher -EventName Created -SourceIdentifier "FileCreated" -Action $action
$changedReg = Register-ObjectEvent -InputObject $watcher -EventName Changed -SourceIdentifier "FileChanged" -Action $action

Write-Log "File watcher started. Press Ctrl+C to stop if running interactively."

# Keep script alive
while ($true) {
    Wait-Event -Timeout 5 | Out-Null
}


