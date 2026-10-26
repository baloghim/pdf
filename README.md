# PDF Műhely

Magyar nyelvű asztali alkalmazás PDF-ek összefűzésére és kettévágására. A fájlokat helyben dolgozza fel, feltöltés nélkül.

## Letöltések

A kész alkalmazásokhoz nem kell Pythont telepíteni.

| Rendszer / változat | Letöltés | Melyiket válaszd? |
| --- | --- | --- |
| **Windows x64 – LTSB 1607 kompatibilitási változat** | **[Legutóbbi Windows ZIP](https://github.com/baloghim/pdf/releases/latest/download/PDF-Muhely-Windows-x64.zip)** | Windows 10 Enterprise 2016 LTSB 1607 géphez ezt készítjük; újabb 64 bites Windows is célplatform. |
| **macOS – Apple Silicon** | **[Mac-csomagok az Actions oldalon](https://github.com/baloghim/pdf/actions/workflows/macos-app.yml)** | M-sorozatú processzorhoz az `PDF-Muhely-macOS-arm64` artifactot válaszd. |
| **macOS – Intel** | **[Mac-csomagok az Actions oldalon](https://github.com/baloghim/pdf/actions/workflows/macos-app.yml)** | Intel processzorhoz az `PDF-Muhely-macOS-x86_64` artifactot válaszd. |

**[Összes Windows-kiadás és korábbi verziók](https://github.com/baloghim/pdf/releases)** · **[Windows-build állapota](https://github.com/baloghim/pdf/actions/workflows/windows-app.yml)** · **[Mac-build állapota](https://github.com/baloghim/pdf/actions/workflows/macos-app.yml)**

A Windows-link a legutóbb sikeresen **közzétett** kiadásra mutat. Ha egy új build még fut vagy hibás, továbbra is az előző csomagot adja. Az első sikeres közzététel előtt a link nem működik. A kiadás címében szereplő rövid commitazonosító alapján ellenőrizhető, melyik változatot töltöd le. Privát tárolóhoz GitHub-bejelentkezés szükséges.

A Mac-csomagok jelenleg az Actions futások **Artifacts** részéből tölthetők le, bejelentkezés után; 30 napig érhetők el. Nyisd meg a legutóbbi sikeres futást, és válaszd a processzorodhoz tartozó artifactot. Lejárt csomag esetén a **Run workflow** gombbal indítható új build.

## Verziók és kompatibilitás

Az alkalmazás projektverziója **0.1.0**. A fejlesztési csomagokat ezen belül a commitazonosító különbözteti meg; ezek nem külön számozott stabil kiadások.

| Változat | Azonosító / hivatkozás | Megjegyzés |
| --- | --- | --- |
| **Windows LTSB 1607 kompatibilitási alap** | [`b7bcc00`](https://github.com/baloghim/pdf/commit/b7bcc00) · [pontos kiadás, ha a build közzétette](https://github.com/baloghim/pdf/releases/tag/windows-b7bcc009e8b015212c5e567ebdb46d96978291dc) | Python 3.10, Qt 5.15.2 / PySide2 5.15.2.1. A későbbi Windows-csomagok is ezen az alapon készülnek, amíg a dokumentáció mást nem jelez. |
| Korábbi Windows Qt 6.8 változat | [`17e2403`](https://github.com/baloghim/pdf/commit/17e2403) | Nem az 1607-es rendszerhez készült; arra ne ezt válaszd. |
| Első Windows Qt 6 változat | [`2c391e9`](https://github.com/baloghim/pdf/commit/2c391e9) | Korábbi csomag, LTSB 1607-hez nem megfelelő. |
| macOS, Apple Silicon / Intel | [Legutóbbi sikeres Mac-build](https://github.com/baloghim/pdf/actions/workflows/macos-app.yml) | Python 3.12-vel csomagolva, Qt 6.10.2 / PySide6. |

**Ellenőrzöttség:** az 1607-es változat célzottan ehhez a rendszerhez készül, de a valódi LTSB 1607 gépen történő sikeres indítás még nincs visszaigazolva. A Windows-csomagot a GitHub Windows Server 2022-n építi és teszteli. A Linuxos fejlesztőkörnyezetben mind a Qt 5-ös, mind a Qt 6-os változat 11 tesztje sikeres. Ez nem helyettesíti a natív Windows- és Mac-próbát.

## Használat Windows alatt

1. Töltsd le a fenti Windows ZIP-et, és **bontsd ki a teljes tartalmát új, üres mappába**.
2. A kibontott `PDF-Muhely` mappában indítsd a **`PDF-Muhely.exe`** fájlt.
3. Az EXE mellett maradjon meg az **`_internal` mappa**. Az EXE önmagában nem elegendő; másik PC-re az egész mappát másold át.

Ne a ZIP-en belül indítsd, és frissítéskor ne keverd a régi és az új csomag fájljait. A 32 bites Windows nem támogatott. A csomag tartalmazza a Pythont, a Qt-t és a hozzá tartozó Visual C++ runtime DLL-eket. A kiadás melletti `SHA256SUMS.txt` segítségével ellenőrizhető a ZIP ellenőrzőösszege.

A program nincs digitálisan aláírva, ezért a SmartScreen figyelmeztethet. Csak megbízható forrásból letöltött csomagot indíts el.

## Használat macOS alatt

1. A fenti Mac-linken nyisd meg a legutóbbi sikeres futást, és töltsd le a megfelelő artifactot.
2. Bontsd ki az archívumot, majd a benne lévő ZIP-et is.
3. Másold a **`PDF Muhely.app`** fájlt az **Alkalmazások** mappába, és indítsd dupla kattintással.

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

Macen és Linuxon Python 3.10 vagy újabb, Windowson **Python 3.10 x64** szükséges a Qt 5-ös változathoz.

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
powershell -ExecutionPolicy Bypass -File packaging/build_windows.ps1
```

Ez csak erre a folyamatra engedi a saját buildszkript futtatását; nem módosítja a tartós házirendet. Eredmény: `dist/PDF-Muhely-Windows-x64.zip`.

### Mac-csomag

Macen, Python 3.10+ használatával:

```sh
bash packaging/build_macos.sh
```

Eredmény: `dist/PDF Muhely.app` és a gép processzorához tartozó ZIP. A Windows- és Mac-build a teszteket és a becsomagolt alkalmazás indulását is ellenőrzi.

A GitHub munkafolyamatok a main ágra feltöltött programmódosításokra automatikusan indulnak, vagy kézzel az Actions oldali **Run workflow** gombbal. A Windows-build siker után Release-ként is közzéteszi a csomagot; a Mac-build jelenleg artifactot készít.
