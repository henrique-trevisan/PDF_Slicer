"""Entry point for PDF Slicer."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from pdf_slicer.gui import create_gui


if __name__ == "__main__":
    create_gui()
