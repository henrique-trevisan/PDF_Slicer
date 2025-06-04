from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import tempfile

from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader

from pdf_slicer import slice_pdf


def create_test_pdf(pages: int, path: Path) -> None:
    c = canvas.Canvas(str(path))
    for page in range(pages):
        c.drawString(100, 750, f"Page {page + 1}")
        c.showPage()
    c.save()


def test_slice_pdf(tmp_path: Path):
    source = tmp_path / "src.pdf"
    create_test_pdf(3, source)

    output = tmp_path / "out.pdf"
    slice_pdf(str(source), 2, 3, str(output))

    reader = PdfReader(str(output))
    assert len(reader.pages) == 2
    text = reader.pages[0].extract_text()
    assert "Page 2" in text
