# PowerShell equivalent of start.sh
$ErrorActionPreference = "Stop"

# Start FastAPI backend
Write-Host "Starting Backend..."
$backendJob = Start-Job {
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
}

# Start Streamlit frontend
Write-Host "Starting Frontend..."
$frontendJob = Start-Job {
    streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
}

try {
    # Keep the script running until user interrupts (Ctrl+C)
    Write-Host "Services started! Press Ctrl+C to stop both."
    while($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    # Cleanup jobs when script is cancelled or fails
    Write-Host "Stopping services..."
    Stop-Job $backendJob
    Stop-Job $frontendJob
    Remove-Job $backendJob
    Remove-Job $frontendJob
}
