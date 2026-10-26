$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$Project = 'legacy/windows-xp/PdfMuhely.XP.csproj'
dotnet build $Project -c Release --output dist/windows-xp
if ($LASTEXITCODE -ne 0) { throw 'Az XP változat fordítása sikertelen.' }
$Exe = Join-Path $PWD 'dist/windows-xp/PDF-Muhely-XP-x86.exe'
$Config = "$Exe.config"
# Server 2022 provides CLR 4, not the XP CLR 2. Test the same net35 binary
# under CLR 4 here, then ship its original CLR 2 configuration for XP.
$Original = Get-Content -Raw $Config
try {
    '<configuration><startup useLegacyV2RuntimeActivationPolicy="true"><supportedRuntime version="v4.0" /></startup></configuration>' | Set-Content $Config
    foreach ($Test in @('--self-test', '--smoke-test')) {
        $Process = Start-Process -FilePath $Exe -ArgumentList $Test -PassThru -RedirectStandardError 'dist/xp-test-errors.txt'
        if (-not $Process.WaitForExit(60000)) { $Process.Kill(); throw "XP test timeout: $Test" }
        $Process.Refresh()
        if ($Process.ExitCode -ne 0) {
            Get-Content 'dist/xp-test-errors.txt'
            throw "XP test failed: $Test, exit $($Process.ExitCode)"
        }
    }
} finally { [IO.File]::WriteAllText($Config, $Original) }
Copy-Item 'legacy/windows-xp/README.txt' 'dist/windows-xp/README.txt'
Compress-Archive -Path 'dist/windows-xp' -DestinationPath 'dist/PDF-Muhely-Windows-XP-x86.zip' -Force
