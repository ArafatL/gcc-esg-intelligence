"""Extract raw text from disclosure PDFs (pdfplumber with pypdf fallback)."""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("esgintel.pdf")


def extract_text(pdf_path: str | Path, max_pages: int | None = None) -> str:
    """Return concatenated text of a PDF. Empty string on failure."""
    pdf_path = Path(pdf_path)
    text_parts: list[str] = []
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages[:max_pages] if max_pages else pdf.pages
            for page in pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except Exception as exc:  # noqa: BLE001
        log.warning("pdfplumber failed on %s (%s); trying pypdf", pdf_path.name, exc)
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        pages = reader.pages[:max_pages] if max_pages else reader.pages
        for page in pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except Exception as exc:  # noqa: BLE001
        log.error("Text extraction failed for %s: %s", pdf_path.name, exc)
        return ""
