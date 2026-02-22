"""
Export a ParseResult to bytes (markdown, HTML, or Excel).

Used by the API and SDK for in-memory export without filesystem.
"""
from __future__ import annotations

from unstructured.models import ParseResult
from unstructured.exporters.html_writer import build_html_document_bytes
from unstructured.exporters.excel_writer import write_structured_excel_to_buffer


def export(result: ParseResult, format: str) -> bytes:
    """
    Export a ParseResult to bytes in the given format.

    :param result: In-memory parse result from StructuredPDFParser.parse().
    :param format: One of "markdown", "html", "excel".
    :return: UTF-8 bytes for markdown/html, binary for excel.
    :raises ValueError: If format is not supported.
    """
    fmt = format.strip().lower()
    if fmt == "markdown":
        content = "\n".join(result.md_lines).strip() + "\n"
        return content.encode("utf-8")
    if fmt == "html":
        return build_html_document_bytes(result.html_lines, result.images)
    if fmt == "excel":
        return write_structured_excel_to_buffer(result.structured_items)
    raise ValueError(f"Unsupported export format: {format!r}. Use one of: markdown, html, excel")
