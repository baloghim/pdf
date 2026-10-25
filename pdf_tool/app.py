"""Cross-platform desktop interface."""
import sys
from pathlib import Path
from PySide6.QtCore import Qt, QObject, Signal, QThread
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QFileDialog, QMessageBox, QLabel, QTabWidget,
    QSpinBox, QAbstractItemView)
from . import core


class Worker(QObject):
    finished = Signal(str)
    def __init__(self, action):
        super().__init__()
        self.action = action
    def run(self):
        try:
            self.action()
            self.finished.emit("")
        except Exception as error:
            self.finished.emit(str(error))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Műhely")
        self.resize(660, 460)
        self.source = None
        layout = QVBoxLayout(self)
        title = QLabel("PDF Műhely")
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 12px;")
        layout.addWidget(title)
        layout.addWidget(QLabel("Összefűzés és kettévágás helyben, feltöltés nélkül."))
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        merge_tab = QWidget()
        ml = QVBoxLayout(merge_tab)
        ml.addWidget(QLabel("A fájlok az alábbi sorrendben kerülnek az új PDF-be. Húzással átrendezhetők."))
        self.files = QListWidget()
        self.files.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.files.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        ml.addWidget(self.files)
        row = QHBoxLayout()
        self.button(row, "PDF-ek hozzáadása…", self.add_files)
        self.button(row, "Kijelöltek eltávolítása", self.remove_files)
        ml.addLayout(row)
        self.button(ml, "Összefűzés és mentés…", self.merge)
        self.tabs.addTab(merge_tab, "Összefűzés")
        split_tab = QWidget()
        sl = QVBoxLayout(split_tab)
        self.button(sl, "PDF kiválasztása…", self.choose_source)
        self.source_label = QLabel("Még nincs kiválasztott fájl.")
        self.source_label.setWordWrap(True)
        sl.addWidget(self.source_label)
        sl.addWidget(QLabel("Az első fájl utolsó oldalának száma:"))
        self.cut = QSpinBox()
        self.cut.setMinimum(1)
        self.cut.setEnabled(False)
        sl.addWidget(self.cut)
        sl.addWidget(QLabel("A második fájl a következő oldallal kezdődik."))
        self.button(sl, "Kettévágás és mentés…", self.split)
        sl.addStretch()
        self.tabs.addTab(split_tab, "Kettévágás")
        self.status = QLabel("Készen áll.")
        layout.addWidget(self.status)

    def button(self, layout, text, action):
        button = QPushButton(text)
        button.clicked.connect(action)
        layout.addWidget(button)

    def error(self, message):
        QMessageBox.warning(self, "Nem sikerült a művelet", message)

    def add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "PDF-ek kiválasztása", "", "PDF (*.pdf)")
        self.files.addItems(paths)

    def remove_files(self):
        for item in self.files.selectedItems():
            self.files.takeItem(self.files.row(item))

    def destination(self, title, suggested):
        path, _ = QFileDialog.getSaveFileName(self, title, suggested, "PDF (*.pdf)")
        if path and not path.lower().endswith(".pdf"):
            path += ".pdf"
        return path

    def merge(self):
        paths = [self.files.item(i).text() for i in range(self.files.count())]
        if len(paths) < 2:
            return self.error("Legalább két PDF-et adj hozzá.")
        target = self.destination("Összefűzött PDF mentése új fájlba", "osszefuzott.pdf")
        if target:
            self.run(lambda: core.merge(paths, target))

    def choose_source(self):
        path, _ = QFileDialog.getOpenFileName(self, "PDF kiválasztása", "", "PDF (*.pdf)")
        if not path:
            return
        try:
            count = core.page_count(path)
            if count < 2:
                raise ValueError("A kettévágáshoz legalább két oldal szükséges.")
        except Exception as error:
            return self.error(str(error))
        self.source = path
        self.source_label.setText(f"{Path(path).name} — {count} oldal")
        self.cut.setEnabled(True)
        self.cut.setMaximum(count - 1)

    def split(self):
        if not self.source:
            return self.error("Először válassz ki egy PDF-et.")
        source = Path(self.source)
        first = self.destination("Első rész mentése új fájlba", str(source.with_name(source.stem + "_1.pdf")))
        if not first:
            return
        second = self.destination("Második rész mentése új fájlba", str(source.with_name(source.stem + "_2.pdf")))
        if second:
            cut = self.cut.value()
            self.run(lambda: core.split(source, cut, first, second))

    def run(self, action):
        self.tabs.setEnabled(False)
        self.status.setText("Feldolgozás…")
        self.thread = QThread(self)
        self.worker = Worker(action)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.completed)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def completed(self, error):
        self.tabs.setEnabled(True)
        self.status.setText("Sikertelen művelet." if error else "Elkészült. A PDF-fájlok mentve.")
        if error:
            self.error(error)

    def closeEvent(self, event):
        if not self.tabs.isEnabled():
            event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    if "--smoke-test" in sys.argv:
        app.processEvents()
        assert window.tabs.count() == 2
        window.close()
        return 0
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
