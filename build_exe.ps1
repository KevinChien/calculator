<#
PowerShell helper to build executables with PyInstaller.

Usage (PowerShell):
    cd e:\workspace\src_code\smaple_project
    .\build_exe.ps1 -Target gui    # build GUI exe
    .\build_exe.ps1 -Target cli    # build CLI exe

Requires: `pyinstaller` installed in the active Python environment.
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("gui","cli")]
    [string]$Target = "gui"
)

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller 未找到，請先安裝： pip install pyinstaller" -ForegroundColor Yellow
    exit 1
}

if ($Target -eq "gui") {
    pyinstaller --onefile --name calculator_gui --windowed calculator/gui.py
} else {
    pyinstaller --onefile --name calculator_cli calculator/cli.py
}
