# PDF Műhely

Python-alapú asztali alkalmazás magyar grafikus felülettel. A fájlokat helyben dolgozza fel, nem tölti fel őket.

- Több PDF összefűzése, húzással módosítható fájlsorrenddel.
- PDF-ek behúzása Finderből vagy más fájlkezelőből az ablakra: az Összefűzés fülön hozzáadás a listához, a Kettévágás fülön egyetlen PDF megnyitása. Mappák és nem PDF fájlok nem húzhatók be.
- Egy PDF kettévágása a megadott oldal után.
- Bemeneti és meglévő fájlok felülírásának tiltása.
- Háttérben végzett mentés, hogy a felület használható maradjon.

## Indítás macOS-en

Python 3.10 vagy újabb szükséges (a python.org telepítőjével is telepíthető).

```sh
cd pdf
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pdf_tool.app
```

Linuxon ugyanezek a parancsok használhatók; a Qt grafikus rendszerkönyvtárait a disztribúció csomagkezelőjével is telepíteni kellhet. Windowson az aktiválás PowerShellben: `.venv\Scripts\Activate.ps1`.

```sh
python -m pytest
```

Az alkalmazás első verziója. A macOS-es natív használatot valódi Macen is ellenőrizni kell. Az .app csomag összeállítását az alábbi buildfolyamat végzi; Apple Developer kódaláírás és notarizálás még nincs beállítva. A PDF-könyvjelzők, űrlapok és digitális aláírások teljes megőrzése nem garantált; az aláírt dokumentum módosítása érvénytelenítheti az aláírást. Jelszóval védett PDF-eket a program jelenleg nem kezel.

## Dupla kattintással indítható macOS alkalmazás

A csomag tartalmazza a Pythont és a függőségeket; a használatához nem kell Python vagy terminál.

1. GitHubon nyisd meg az **Actions → macOS alkalmazás** munkafolyamatot.
2. Nyisd meg a legutóbbi sikeres futást, majd az **Artifacts** részből töltsd le a gépedhez tartozó csomagot: `arm64` Apple Siliconhoz (M1/M2/M3/M4/M5), `x86_64` Intel Machez. A gép típusát az Apple menü **A Mac névjegye** pontjában találod.
3. Bontsd ki a letöltött archívumot, majd a benne található ZIP-et is. A `PDF Muhely.app` fájlt másold az **Alkalmazások** mappába, és indítsd dupla kattintással.

A build automatikusan indul a program main ágra feltöltött módosításakor, vagy kézzel a **Run workflow** gombbal. Az artifactok letöltéséhez GitHub-bejelentkezés szükséges, és 30 napig érhetők el.

A csomag jelenleg nincs Apple Developer tanúsítvánnyal aláírva és notarizálva. A macOS ezért blokkolhatja az első indítást. Ha ellenőrizted a letöltés forrását, a **Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképp** lehetőséggel engedélyezheted. Ne kapcsold ki a Gatekeepert. A helyi ad hoc aláírás nem helyettesíti az Apple Developer aláírást.

### Összeállítás a saját Maceden

Ha nem szeretnél GitHub Actionsre várni, a projekt mappájából futtasd:

```sh
bash packaging/build_macos.sh
```

Ehhez az összeállításkor Python 3.10+ és internet szükséges. Az eredmény a `dist/PDF Muhely.app`, illetve egy, a géped processzorához készült ZIP. A build mind a teszteket, mind a becsomagolt alkalmazás grafikus indulását ellenőrzi. A macOS-verziók közötti kompatibilitást és a natív fájlválasztókat valódi gépen is tesztelni kell.
