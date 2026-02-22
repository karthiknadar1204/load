"""
Portable in-memory result of document parsing.

Used by the API and SDK for parse → export flows without relying on the filesystem.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class ParseResult:
    """
    In-memory result of parsing a document.

    Can be passed to export(result, format) to produce bytes (e.g. for HTTP
    or local use) without writing to disk.

    :param md_lines: Markdown content as list of lines (with image refs as relative paths).
    :param html_lines: HTML content as list of lines (with img src as relative paths).
    :param structured_items: List of table/chart items with keys e.g. title, headers, rows.
    :param images: Map from relative path (as used in md_lines/html_lines) to (raw_bytes, mime_type).
    """

    md_lines: List[str]
    html_lines: List[str]
    structured_items: List[Dict[str, Any]]
    images: Dict[str, Tuple[bytes, str]] = field(default_factory=dict)
