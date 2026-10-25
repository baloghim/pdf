"""Exercise actual Qt file drag/drop events, without a display server."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import pytest
from PySide6.QtCore import QMimeData, QPoint, QPointF, Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QApplication
from pypdf import PdfWriter
from pdf_tool.app import Window


@pytest.fixture
def window():
    app = QApplication.instance() or QApplication([])
    w = Window()
    w.show()
    app.processEvents()
    yield w
    w.close()


def make_pdf(path):
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=100, height=200)
    writer.write(path)
    return path


def drop(target, paths):
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(str(p)) for p in paths])
    enter = QDragEnterEvent(QPoint(10, 10), Qt.DropAction.CopyAction,
                            mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(target, enter)
    if enter.isAccepted():
        event = QDropEvent(QPointF(10, 10), Qt.DropAction.CopyAction,
                           mime, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
        QApplication.sendEvent(target, event)
        assert event.isAccepted()
    return enter.isAccepted()


def test_drop_multiple_pdfs_on_list_and_window(window, tmp_path):
    a = make_pdf(tmp_path / 'első.PDF')
    b = make_pdf(tmp_path / 'második.pdf')
    assert drop(window.files.viewport(), [a, b])
    assert drop(window, [a])
    assert [window.files.item(i).text() for i in range(3)] == [str(a), str(b), str(a)]


def test_split_drop_opens_pdf_and_rejects_multiple(window, tmp_path):
    a = make_pdf(tmp_path / 'a.pdf')
    window.tabs.setCurrentIndex(1)
    assert drop(window.source_label, [a])
    assert window.source == str(a)
    assert window.cut.maximum() == 2
    assert window.cut.isEnabled()
    assert not drop(window, [a, a])
    assert window.source == str(a)


def test_invalid_and_busy_drops_rejected(window, tmp_path):
    other = tmp_path / 'text.txt'
    other.write_text('text')
    a = make_pdf(tmp_path / 'a.pdf')
    assert not drop(window, [other])
    assert not drop(window, [tmp_path / 'missing.pdf'])
    assert not drop(window, [a, other])
    window.tabs.setEnabled(False)
    assert not drop(window, [a])
    assert window.files.count() == 0
    window.tabs.setEnabled(True)


def test_invalid_pdf_preserves_previous_split_source(window, tmp_path, monkeypatch):
    a = make_pdf(tmp_path / 'a.pdf')
    broken = tmp_path / 'broken.pdf'
    broken.write_bytes(b'broken')
    errors = []
    monkeypatch.setattr(window, 'error', errors.append)
    window.tabs.setCurrentIndex(1)
    assert drop(window, [a])
    assert drop(window, [broken])
    assert errors
    assert window.source == str(a)
