$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if ($env:OS -ne 'Windows_NT') { throw 'A Windows-csomagot Windowson kell összeállítani.' }

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program hibakód: $LASTEXITCODE" }
}

Invoke-Checked -Program 'python' -Arguments @('-c', 'import sys; assert sys.version_info[:2] == (3, 10), "A Windows 1607 buildhez Python 3.10 kell."')
Invoke-Checked -Program 'python' -Arguments @('-m', 'venv', '.venv-build-win1607')
$Python = Join-Path $PWD '.venv-build-win1607\Scripts\python.exe'
Invoke-Checked -Program $Python -Arguments @('-m', 'pip', 'install', '-e', '.[test]', 'pyinstaller==6.19.0')
$env:QT_QPA_PLATFORM = 'offscreen'
Invoke-Checked -Program $Python -Arguments @('-m', 'pytest', '-q')
# Collect the official wheel's app-local VC++ runtime explicitly. The CI
# machine has global runtimes installed, which must not mask missing bundle DLLs.
$QtDirectory = & $Python -c "import pathlib, PySide2; print(pathlib.Path(PySide2.__file__).parent)"
if ($LASTEXITCODE -ne 0) { throw 'A PySide2 könyvtára nem található.' }
$RuntimeNames = @('msvcp140.dll', 'msvcp140_1.dll', 'msvcp140_2.dll', 'msvcp140_codecvt_ids.dll', 'vcruntime140.dll', 'vcruntime140_1.dll', 'concrt140.dll')
$BuildArguments = @('-m', 'PyInstaller', '--noconfirm', '--clean', '--windowed', '--name', 'PDF-Muhely', '--paths', '.')
foreach ($Name in $RuntimeNames) {
    $Dll = Join-Path $QtDirectory $Name
    if (-not (Test-Path $Dll)) { throw "Hiányzó runtime a hivatalos PySide2 csomagból: $Name" }
    $BuildArguments += @('--add-binary', "$Dll;.")
}
$BuildArguments += 'packaging/launcher.py'
Invoke-Checked -Program $Python -Arguments $BuildArguments
foreach ($Name in $RuntimeNames) {
    if (-not (Test-Path (Join-Path 'dist\PDF-Muhely\_internal' $Name))) {
        throw "Hiányzó runtime a kész csomagból: $Name"
    }
}
$Exe = Join-Path $PWD 'dist\PDF-Muhely\PDF-Muhely.exe'
$Process = Start-Process -FilePath $Exe -ArgumentList '--smoke-test' -PassThru
if (-not $Process.WaitForExit(60000)) {
    $Process.Kill()
    throw 'A becsomagolt alkalmazás indítási tesztje túllépte az időkeretet.'
}
$Process.Refresh()
if ($Process.ExitCode -ne 0) { throw "Az alkalmazás indítási tesztje sikertelen: $($Process.ExitCode)" }
Compress-Archive -Path 'dist\PDF-Muhely' -DestinationPath 'dist\PDF-Muhely-Windows-x64.zip' -Force
Get-FileHash 'dist\PDF-Muhely-Windows-x64.zip' -Algorithm SHA256 |
    ForEach-Object { "$($_.Hash.ToLower())  PDF-Muhely-Windows-x64.zip" } |
    Set-Content -Encoding ascii 'dist\SHA256SUMS.txt'
Write-Host 'Elkészült: dist\PDF-Muhely-Windows-x64.zip'
