PDF Műhely – Windows XP x86

Célrendszer: 32 bites Windows XP SP3, Microsoft .NET Framework 3.5 SP1 telepítve.
A .NET Framework nincs a ZIP-ben. Telepítője Microsoft-forrásból:
https://www.microsoft.com/en-us/download/details.aspx?id=25150

Bontsd ki az egész ZIP-et, és indítsd a PDF-Muhely-XP-x86.exe fájlt.
Az EXE, a .config és a PdfSharp.dll maradjon egy mappában.
Python telepítése nem szükséges.

Funkciók: PDF-ek összefűzése és kettévágása, fájlbehúzás mindkét fülön.
A sorrend Fel / Le gombokkal módosítható (egyszerre egy kijelölt fájllal).
A grafikus megjelenés az XP rendszerhez igazodik. Nagy fájlok feldolgozásakor
az ablak átmenetileg nem válaszolhat; ez a változat az előtérben dolgozik.
A meglévő fájlokat és a bemeneteket nem írja felül.

Ez külön, régi PDFsharp-alapú kompatibilitási alkalmazás. Nem minden modern
PDF-et tud feldolgozni; titkosított PDF-ek és digitális aláírások megőrzése
nem támogatott. Csak megbízható PDF-fájlokkal használd.

A CI a .NET 3.5 célkeretrendszerre fordít, x86 EXE-t készít, és a PDF-műveleteket
valamint a felület indítását Server 2022-n CLR 4 alatt ellenőrzi. Ez nem igazolja
az XP-n történő futást: valódi XP SP3 / CLR 2 rendszerben külön próba szükséges.
