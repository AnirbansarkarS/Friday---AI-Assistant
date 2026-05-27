# Friday AI Assistant - CLI Launcher (PowerShell)
# Usage: .\friday.ps1 "your command"
# Usage: .\friday.ps1 --voice (for voice mode)
# Usage: .\friday.ps1 (for interactive mode)

param(
    [string]$Command = "",
    [switch]$Voice = $false
)

# Change to project directory
Set-Location -Path $PSScriptRoot

# Build arguments
$args = @()
if ($Voice) {
    $args += "--voice"
} elseif ($Command) {
    $args += $Command
}

# Run CLI
python cli.py @args
