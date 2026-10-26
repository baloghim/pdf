# PDF Műhely

Magyar nyelvű asztali alkalmazás PDF-ek összefűzésére és kettévágására. A fájlokat helyben dolgozza fel, feltöltés nélkül.

## Letöltések

A Python-alapú csomagok tartalmazzák a futtatókörnyezetet; a külön XP-változathoz .NET Framework 3.5 SP1 kell. Válaszd a rendszeredhez tartozó változatot:

| Változat | Közvetlen letöltés | Rendszer / megjegyzés |
| --- | --- | --- |
| Windows x64 | [ZIP letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Windows-x64.zip) | Modern Windows 10 1809+ / Windows 11, Python 3.12 + Qt 6. |
| Windows x64 – LTSB 1607 kompatibilitási változat | [ZIP letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Windows-x64-LTSB1607.zip) | Windows 10 Enterprise 2016 LTSB 1607 célrendszer, Python 3.10 + Qt 5. |
| Windows XP x86 | [ZIP letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Windows-XP-x86.zip) | Külön alkalmazás: Windows XP SP3 32 bit + .NET Framework 3.5 SP1. XP-n még ellenőrizendő. |
| Linux DEB | [DEB letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Linux-x64.deb) | Ubuntu 22.04+, Debian 12+, x86_64. |
| Linux RPM | [RPM letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Linux-x64.rpm) | Modern RPM-alapú x86_64 rendszer, glibc 2.35+; CI-próba Fedora 42-n. |
| Linux .SH | [SH letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Linux-x64.sh) | Hordozható, önkicsomagoló indító; x86_64, glibc 2.35+, grafikus rendszerkönyvtárak. |
| Mac OS Silicon | [ZIP letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-macOS-arm64.zip) | Apple Silicon, M-sorozatú processzor. |
| Mac OS Intel | [ZIP letöltése](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-macOS-x86_64.zip) | Intel processzor. |

**[Összes kiadás és korábbi verziók](https://github.com/baloghim/pdf/releases)** · **[Build állapota / kézi indítás](https://github.com/baloghim/pdf/actions/workflows/desktop-release.yml)** · **[SHA256 ellenőrzőösszegek](https://github.com/baloghim/pdf/releases/latest/download/SHA256SUMS.txt)**

A nyolc csomag közös kiadásként jelenik meg, ha minden platform buildje és ellenőrzése sikeres. Addig az új linkek még nem működnek, vagy korábbi csomagot adnak. **LTSB 1607-hez az LTSB feliratú ZIP-et válaszd**; a sima Windows x64 ZIP az új közös kiadástól kezdve a modern változatot tartalmazza. A kiadás címe és a `desktop-<teljes commitazonosító>` tag jelöli a pontos forrásváltozatot. Privát tárolónál bejelentkezés szükséges.

Ha egy platform hibája miatt a közös kiadás nem készül el, a sikeres buildek csomagjai az Actions futás **Artifacts** részéből is letölthetők. A régi Windows-kiadások és Mac-artifactok az előzményekben maradnak.

## Verziók és kompatibilitás

A projektverzió **0.1.0**, ezen belül a commitazonosító különbözteti meg a fejlesztési kiadásokat.

| Változat | Futási környezet a csomagban |
| --- | --- |
| Windows x64 | Python 3.12, PySide6 6.10.2 |
| Windows x64 LTSB 1607 | Python 3.10, PySide2 5.15.2.1 / Qt 5.15.2 |
| Windows XP x86 | C# / WinForms, .NET Framework 3.5 SP1, PDFsharp 1.50.5147; Python nélkül |
| Linux DEB / RPM / .SH | Python 3.12, PySide6 6.10.2; Ubuntu 22.04-en összeállítva |
| Mac OS Silicon / Intel | Python 3.12, PySide6 6.10.2 |

Az LTSB-kompatibilitási alap a [`b7bcc00`](https://github.com/baloghim/pdf/commit/b7bcc00) változatban készült. A korábbi Qt 6-os Windows-csomagok nem az 1607-es géphez valók. Az LTSB célgépen történő sikeres indítás még nincs visszaigazolva. A CI-beli indulási tesztek nem helyettesítik a valódi gépeken történő interaktív próbát.

## Használat Windows alatt

1. Töltsd le a fenti Windows ZIP-et, és **bontsd ki a teljes tartalmát új, üres mappába**.
2. A kibontott `PDF-Muhely` mappában indítsd a **`PDF-Muhely.exe`** fájlt.
3. Az EXE mellett maradjon meg az **`_internal` mappa**. Az EXE önmagában nem elegendő; másik PC-re az egész mappát másold át.

Ne a ZIP-en belül indítsd, és frissítéskor ne keverd a régi és az új csomag fájljait. A 32 bites Windows nem támogatott. A csomag tartalmazza a Pythont, a Qt-t és a hozzá tartozó Visual C++ runtime DLL-eket. A kiadás melletti `SHA256SUMS.txt` segítségével ellenőrizhető a ZIP ellenőrzőösszege.

A program nincs digitálisan aláírva, ezért a SmartScreen figyelmeztethet. Csak megbízható forrásból letöltött csomagot indíts el.

## Használat Windows XP alatt

1. A célgép **Windows XP SP3, 32 bites** legyen.
2. Telepítsd a **[Microsoft .NET Framework 3.5 SP1](https://www.microsoft.com/en-us/download/details.aspx?id=25150)** keretrendszert, ha még nincs fent. A ZIP ezt nem tartalmazza; a telepítést a gép rendszergazdája végezze. Szükség esetén másik gépen töltsd le a teljes telepítőt.
3. A **Windows XP x86** ZIP-et teljesen bontsd ki, majd indítsd a `PDF-Muhely-XP-x86.exe` fájlt. A `PdfSharp.dll` és az EXE `.config` fájlja is maradjon mellette.

Ez külön kompatibilitási alkalmazás. Az összefűzés, kettévágás és fájlbehúzás mindkét fülön elérhető; a lista sorrendje **Fel / Le** gombokkal módosítható. A feldolgozás alatt az ablak átmenetileg nem válaszolhat. Régi PDF-könyvtárat használ, ezért modern vagy titkosított PDF-eknél korlátozott; csak megbízható dokumentumokkal használd. A 32 bites XP-változat nem helyettesíti a modern Windows-csomagokat.

A GitHub a forrást .NET 3.5-re és x86-ra fordítja. A PDF-műveleteket és a felület indítását Server 2022-n, CLR 4 alatt ellenőrzi, majd az eredeti, CLR 2-t használó konfigurációt csomagolja. **Ez nem XP-n végzett teszt:** a célgépen történő indítás és PDF-próba még szükséges.

## Használat Linux alatt

### DEB (Ubuntu / Debian)

A letöltés mappájában:

```sh
sudo apt install ./PDF-Muhely-Linux-x64.deb
```

Ez a szükséges rendszerfüggőségeket is telepíti. Indítás az alkalmazásmenü **PDF Műhely** pontjából vagy a `pdf-muhely` paranccsal. Eltávolítás: `sudo apt remove pdf-muhely`.

### RPM (például Fedora)

```sh
sudo dnf install ./PDF-Muhely-Linux-x64.rpm
```

Indítás a menüből vagy `pdf-muhely`; eltávolítás: `sudo dnf remove pdf-muhely`. A csomag legalább glibc 2.35-öt igényel, így például az alap RHEL 9 glibc 2.34-es rendszere nem célplatform.

### .SH (telepítés nélkül)

```sh
chmod +x PDF-Muhely-Linux-x64.sh
./PDF-Muhely-Linux-x64.sh
```

Vagy `bash PDF-Muhely-Linux-x64.sh`. Az indító ideiglenes mappába bontja ki az alkalmazást, és kilépéskor eltávolítja azt. Rendszergazdai jog és Python-telepítés nem kell. A kicsomagoláshoz szabad hely és végrehajtást engedélyező ideiglenes fájlrendszer szükséges; utóbbi a `TMPDIR` változóval választható. X11 vagy XWayland grafikus munkamenet szükséges. A DEB/RPM által jelzett Qt/XCB rendszerkönyvtáraknak a hordozható változathoz is rendelkezésre kell állniuk; hiányzó könyvtár esetén a DEB/RPM a javasolt telepítés.

## Használat macOS alatt

1. A fenti táblázatból töltsd le a megfelelő ZIP-et.
2. Bontsd ki, és másold a **`PDF Muhely.app`** fájlt az **Alkalmazások** mappába.
3. Indítsd dupla kattintással.

A processzor típusa az Apple menü **A Mac névjegye** pontjában látható. Az alkalmazás nincs Apple Developer tanúsítvánnyal aláírva és notarizálva. Ha a macOS blokkolja, és ellenőrizted a forrást, a **Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképp** lehetőséggel engedélyezheted. Ne kapcsold ki a Gatekeepert.

## Funkciók

- Több PDF összefűzése; a fájlsorrend húzással változtatható.
- Egy PDF kettévágása a megadott oldal után.
- Fájlbehúzás Finderből vagy más fájlkezelőből: az Összefűzés fülön több PDF hozzáadása, a Kettévágás fülön egy PDF megnyitása.
- Bemeneti és meglévő fájlok felülírásának tiltása.
- Háttérben végzett mentés.

Mappák és nem PDF fájlok nem húzhatók be. Jelszóval védett PDF-eket a program jelenleg nem kezel. A könyvjelzők, űrlapok és digitális aláírások teljes megőrzése nem garantált; a módosítás érvénytelenítheti a digitális aláírást.

## Fejlesztés és saját csomag készítése

### Indítás forrásból

Macen és Linuxon Python 3.10 vagy újabb, Windowson **Python 3.10 x64** szükséges az LTSB/Qt 5 változathoz, a modern build Python 3.12 x64-et használ.

```sh
cd pdf
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pdf_tool.app
```

Windowson a környezet létrehozása `python -m venv .venv`, aktiválása PowerShellben `.venv\Scripts\Activate.ps1`. Linuxon a Qt rendszerkönyvtárait a disztribúció csomagkezelőjével is telepíteni kellhet.

Tesztek:

```sh
python -m pytest -q
```

### Windows-csomag

Windows alatt, Python 3.10 x64 használatával:

```powershell
powershell -ExecutionPolicy Bypass -File packaging/build_windows.ps1 -Variant ltsb1607
```

Ez csak erre a folyamatra engedi a saját buildszkript futtatását; nem módosítja a tartós házirendet. Eredmény: `dist/PDF-Muhely-Windows-x64-LTSB1607.zip`. Modern Windows-csomaghoz Python 3.12 mellett `-Variant modern` szükséges; annak fájlneve `PDF-Muhely-Windows-x64.zip`.

### Mac-csomag

Macen, Python 3.10+ használatával:

```sh
bash packaging/build_macos.sh
```

Eredmény: `dist/PDF Muhely.app` és a gép processzorához tartozó ZIP. A Windows- és Mac-build a teszteket és a becsomagolt alkalmazás indulását is ellenőrzi.

### Linux-csomagok készítése

Linux x86_64, Python 3.12, nfpm 2.41.3 és a Qt grafikus rendszerkönyvtárai szükségesek. A build alapja Ubuntu 22.04; újabb rendszeren készült helyi build újabb glibc-t igényelhet.

```sh
bash packaging/build_linux.sh
```

Eredmény a `dist` mappában: DEB, RPM és SH. A CI a DEB telepítését Ubuntu 22.04-en, az RPM telepítését Fedora 42 konténerben, az SH indítását virtuális X11 kijelzővel ellenőrzi.

A közös GitHub munkafolyamat main ágra feltöltött programmódosításra indul, vagy kézzel az Actions **Run workflow** gombjával. Az ellenőrzések után mind a nyolc csomagot és a közös `SHA256SUMS.txt` fájlt egyetlen Release-ben teszi közzé.

### XP-csomag készítése

Windows alatt .NET SDK 8-cal:

```powershell
powershell -ExecutionPolicy Bypass -File packaging/build_windows_xp.ps1
```

A külön forrás a `legacy/windows-xp` mappában található. Eredmény: `dist/PDF-Muhely-Windows-XP-x86.zip`. A szükséges .NET 3.5 referencia-assemblyket és a PDFsharpot a build a NuGetről tölti le.
