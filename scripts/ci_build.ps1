param()

$log = Join-Path -Path (Get-Location) -ChildPath "build_log.txt"
if (Test-Path $log) { Remove-Item $log -Force }
Start-Transcript -Path $log -Force

Write-Host "Running CI build script..."

Write-Host "Locating Python executable..."
$pythonCmd = $null
$pythonDef = $null
try {
	$pythonCmdInfo = Get-Command python -ErrorAction SilentlyContinue
	if ($pythonCmdInfo) { $pythonDef = $pythonCmdInfo.Definition }
} catch {}

if ($pythonDef) {
	Write-Host "Found 'python' -> $pythonDef"
	# If the path points to the WindowsApps stub (Microsoft Store), prefer the 'py' launcher or a real python.exe
	if ($pythonDef -match 'WindowsApps') {
		Write-Host "Notice: 'python' resolves to WindowsApps stub (Microsoft Store). Will try 'py' launcher instead." -ForegroundColor Yellow
		$pythonDef = $null
	}
}

if (-not $pythonDef -and (Get-Command py -ErrorAction SilentlyContinue)) {
	$pyInfo = Get-Command py -ErrorAction SilentlyContinue
	if ($pyInfo) { $pythonDef = $pyInfo.Definition; Write-Host "Using 'py' launcher -> $pythonDef" }
}

# If still not resolved, try to find actual python.exe via where.exe and pick the first non-WindowsApps result
if (-not $pythonDef) {
	try {
		$whereOut = & where.exe python 2>$null
		if ($whereOut) {
			foreach ($p in $whereOut) {
				if ($p -notmatch 'WindowsApps') { $pythonDef = $p; break }
			}
		}
	} catch {}
}

if (-not $pythonDef) {
	Write-Host "ERROR: No usable Python executable found in PATH. Run 'where.exe python' and ensure a real python.exe is installed (not the Microsoft Store stub)." -ForegroundColor Red
	Stop-Transcript
	exit 1
}

$pythonCmd = $pythonDef
Write-Host "Using Python executable: $pythonCmd"

Write-Host "Upgrading pip..."
& $pythonCmd -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { Write-Host "pip upgrade failed with code $LASTEXITCODE" }

Write-Host "Installing PyInstaller (if missing)..."
& $pythonCmd -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { Write-Host "pyinstaller install failed with code $LASTEXITCODE" }

Write-Host "Verifying PyInstaller import..."
try {
	& $pythonCmd -c "import PyInstaller; print('pyinstaller-ok')"
	if ($LASTEXITCODE -ne 0) { Write-Host "PyInstaller import failed after install (exit code $LASTEXITCODE)." -ForegroundColor Yellow }
} catch {
	Write-Host "PyInstaller import failed after install. Exception: $_" -ForegroundColor Yellow
}

Write-Host "Running PyInstaller..."
& $pythonCmd -m PyInstaller -y --clean --onefile --name calculator_gui --windowed calculator/gui.py --log-level=DEBUG
if ($LASTEXITCODE -ne 0) { Write-Host "PyInstaller exited with code $LASTEXITCODE" }

Write-Host "Build finished. Listing dist contents:"
if (Test-Path .\dist) {
	Get-ChildItem -Path .\dist -Recurse -Force
} else {
	Write-Host "NO_DIST: dist directory not found"
}

Stop-Transcript
Write-Host "Transcript saved to $log"
