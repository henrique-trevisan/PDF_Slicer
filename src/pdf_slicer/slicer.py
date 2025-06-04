"""Utilities for slicing PDF files."""

from typing import Union
from PyPDF2 import PdfReader, PdfWriter


def slice_pdf(input_path: str, start_page: int, end_page: int, output_path: str) -> str:
    """Extract pages from ``input_path`` and save them to ``output_path``.

    Parameters
    ----------
    input_path: str
        Path to the source PDF file.
    start_page: int
        First page to include (1-indexed).
    end_page: int
        Last page to include (1-indexed, inclusive).
    output_path: str
        Where the new PDF should be written.

    Returns
    -------
    str
        The ``output_path`` for convenience.
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # convert to zero based indices
    start_idx = start_page - 1
    end_idx = end_page - 1

    if start_idx < 0 or end_idx >= len(reader.pages) or start_idx > end_idx:
        raise ValueError("Invalid page range")

    for i in range(start_idx, end_idx + 1):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as fh:
        writer.write(fh)

    return output_path
