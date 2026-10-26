param([ValidateSet('modern', 'ltsb1607')][string]$Variant = 'ltsb1607')
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if ($env:OS -ne 'Windows_NT') { throw 'A Windows-csomagot Windowson kell összeállítani.' }

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program hibakód: $LASTEXITCODE" }
}

$ExpectedMinor = if ($Variant -eq 'ltsb1607') { '10' } else { '12' }
Invoke-Checked -Program 'python' -Arguments @('-c', "import sys; assert sys.version_info[:2] == (3, $ExpectedMinor), 'Incorrect Python version for Windows variant'")
$Venv = ".venv-build-win-$Variant"
Invoke-Checked -Program 'python' -Arguments @('-m', 'venv', $Venv)
$Python = Join-Path $PWD "$Venv\Scripts\python.exe"
$Binding = if ($Variant -eq 'ltsb1607') { 'PySide2' } else { 'PySide6' }
$Asset = if ($Variant -eq 'ltsb1607') { 'PDF-Muhely-Windows-x64-LTSB1607.zip' } else { 'PDF-Muhely-Windows-x64.zip' }
Invoke-Checked -Program $Python -Arguments @('-m', 'pip', 'install', '-e', '.[test]', 'pyinstaller==6.19.0')
$env:QT_QPA_PLATFORM = 'offscreen'
Invoke-Checked -Program $Python -Arguments @('-m', 'pytest', '-q')
# Collect the official wheel's app-local VC++ runtime explicitly. The CI
# machine has global runtimes installed, which must not mask missing bundle DLLs.
$QtDirectory = & $Python -c "import pathlib, $Binding; print(pathlib.Path($Binding.__file__).parent)"
if ($LASTEXITCODE -ne 0) { throw "A $Binding könyvtára nem található." }
$RuntimeNames = @('msvcp140.dll', 'msvcp140_1.dll', 'msvcp140_2.dll', 'msvcp140_codecvt_ids.dll', 'vcruntime140.dll', 'vcruntime140_1.dll', 'concrt140.dll')
$BuildArguments = @('-m', 'PyInstaller', '--noconfirm', '--clean', '--windowed', '--name', 'PDF-Muhely', '--paths', '.')
foreach ($Name in $RuntimeNames) {
    $Dll = Join-Path $QtDirectory $Name
    if (-not (Test-Path $Dll)) { throw "Hiányzó runtime a hivatalos Qt csomagból: $Name" }
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
Compress-Archive -Path 'dist\PDF-Muhely' -DestinationPath (Join-Path 'dist' $Asset) -Force
Write-Host "Elkészült: dist\$Asset"
