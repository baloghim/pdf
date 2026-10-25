# PDF Műhely

Python-alapú asztali alkalmazás magyar grafikus felülettel. A fájlokat helyben dolgozza fel, nem tölti fel őket.

- Több PDF összefűzése, húzással módosítható fájlsorrenddel.
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

Az alkalmazás első verziója. A macOS-es natív indítás, a külön telepíthető .app csomag, a kódaláírás és a notarizálás még nincs ellenőrizve vagy elkészítve. A PDF-könyvjelzők, űrlapok és digitális aláírások teljes megőrzése nem garantált; az aláírt dokumentum módosítása érvénytelenítheti az aláírást. Jelszóval védett PDF-eket a program jelenleg nem kezel.
