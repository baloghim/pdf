import pytest
from pypdf import PdfReader, PdfWriter
from pdf_tool.core import merge, split


def pdf(path, widths):
    writer = PdfWriter()
    for width in widths:
        writer.add_blank_page(width=width, height=200)
    writer.write(path)
    return path


def widths(path):
    return [int(p.mediabox.width) for p in PdfReader(path).pages]


def test_merge_and_split_preserve_page_order(tmp_path):
    a = pdf(tmp_path / 'a.pdf', [100, 110])
    b = pdf(tmp_path / 'b.pdf', [120])
    out = tmp_path / 'merged.pdf'
    merge([b, a], out)
    assert widths(out) == [120, 100, 110]
    first, second = tmp_path / 'first.pdf', tmp_path / 'second.pdf'
    split(out, 1, first, second)
    assert widths(first) == [120]
    assert widths(second) == [100, 110]


def test_protect_inputs_and_existing_outputs(tmp_path):
    a = pdf(tmp_path / 'a.pdf', [100, 110])
    before = a.read_bytes()
    with pytest.raises(ValueError):
        merge([a, a], a)
    with pytest.raises(ValueError):
        split(a, 1, tmp_path / 'new.pdf', a)
    assert a.read_bytes() == before
    assert not (tmp_path / 'new.pdf').exists()


@pytest.mark.parametrize('cut', [0, 2, 3])
def test_invalid_split(tmp_path, cut):
    a = pdf(tmp_path / 'a.pdf', [100, 110])
    with pytest.raises(ValueError):
        split(a, cut, tmp_path / 'one.pdf', tmp_path / 'two.pdf')
    assert not (tmp_path / 'one.pdf').exists()


def test_reject_encrypted_and_corrupt_pdf(tmp_path):
    a = tmp_path / 'encrypted.pdf'
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=200)
    writer.encrypt('secret')
    writer.write(a)
    with pytest.raises(ValueError, match='jelszó'):
        merge([a, a], tmp_path / 'out.pdf')
    a.write_bytes(b'broken')
    with pytest.raises(Exception):
        merge([a, a], tmp_path / 'out.pdf')
    assert not (tmp_path / 'out.pdf').exists()
