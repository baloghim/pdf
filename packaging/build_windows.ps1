$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if ($env:OS -ne 'Windows_NT') { throw 'A Windows-csomagot Windowson kell összeállítani.' }

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program hibakód: $LASTEXITCODE" }
}

Invoke-Checked -Program 'python' -Arguments @('-m', 'venv', '.venv-build')
$Python = Join-Path $PWD '.venv-build\Scripts\python.exe'
Invoke-Checked -Program $Python -Arguments @('-m', 'pip', 'install', '-e', '.[test]', 'pyinstaller==6.19.0')
$env:QT_QPA_PLATFORM = 'offscreen'
Invoke-Checked -Program $Python -Arguments @('-m', 'pytest', '-q')
Invoke-Checked -Program $Python -Arguments @('-m', 'PyInstaller', '--noconfirm', '--clean', '--windowed', '--name', 'PDF-Muhely', '--paths', '.', 'packaging/launcher.py')
$Exe = Join-Path $PWD 'dist\PDF-Muhely\PDF-Muhely.exe'
$Process = Start-Process -FilePath $Exe -ArgumentList '--smoke-test' -PassThru
if (-not $Process.WaitForExit(60000)) {
    $Process.Kill()
    throw 'A becsomagolt alkalmazás indítási tesztje túllépte az időkeretet.'
}
if ($Process.ExitCode -ne 0) { throw "Az alkalmazás indítási tesztje sikertelen: $($Process.ExitCode)" }
Compress-Archive -Path 'dist\PDF-Muhely' -DestinationPath 'dist\PDF-Muhely-Windows-x64.zip' -Force
Get-FileHash 'dist\PDF-Muhely-Windows-x64.zip' -Algorithm SHA256 |
    ForEach-Object { "$($_.Hash.ToLower())  PDF-Muhely-Windows-x64.zip" } |
    Set-Content -Encoding ascii 'dist\SHA256SUMS.txt'
Write-Host 'Elkészült: dist\PDF-Muhely-Windows-x64.zip'
