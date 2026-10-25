"""PDF operations independent of the graphical interface."""
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
from pypdf import PdfReader, PdfWriter


def _reader(path):
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise ValueError("A jelszóval védett PDF-eket előbb fel kell oldani.")
    if not reader.pages:
        raise ValueError("A PDF nem tartalmaz oldalakat.")
    return reader


def page_count(path):
    return len(_reader(path).pages)


def _destinations(inputs, outputs):
    sources = {Path(p).resolve() for p in inputs}
    targets = [Path(p).resolve() for p in outputs]
    if len(set(targets)) != len(targets):
        raise ValueError("A kimeneti fájlok neve legyen különböző.")
    for target in targets:
        if target in sources:
            raise ValueError("A kimenet nem írhatja felül a bemeneti PDF-et.")
        if target.exists():
            raise ValueError(f"A fájl már létezik: {target.name}. Válassz másik nevet.")
    return targets


def _save(writer, target):
    # Stage complete output first, then publish without overwriting existing files.
    temporary = None
    try:
        with NamedTemporaryFile(dir=target.parent, suffix=".pdf", delete=False) as stream:
            temporary = Path(stream.name)
            writer.write(stream)
        os.link(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def merge(inputs, output):
    inputs = list(inputs)
    if len(inputs) < 2:
        raise ValueError("Legalább két PDF-et válassz ki.")
    target, = _destinations(inputs, [output])
    writer = PdfWriter()
    for path in inputs:
        writer.append(_reader(path))
    _save(writer, target)


def split(source, after_page, first_output, second_output):
    targets = _destinations([source], [first_output, second_output])
    reader = _reader(source)
    if not 1 <= after_page < len(reader.pages):
        raise ValueError("A vágási pont az első és az utolsó előtti oldal közé essen.")
    created = []
    try:
        for target, pages in zip(targets, (reader.pages[:after_page], reader.pages[after_page:])):
            writer = PdfWriter()
            for page in pages:
                writer.add_page(page)
            _save(writer, target)
            created.append(target)
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise
