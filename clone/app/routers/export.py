"""Export pre-parsed content to a format (bytes)."""
from __future__ import annotations

import base64
from typing import Dict, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.schemas import ApiResponse, ExportRequest

router = APIRouter(tags=["export"])


@router.post("/export")
def export_content(req: ExportRequest):
    """
    Export already-parsed content to markdown, html, or excel.
    Send md_lines, html_lines, structured_items, and images (base64) from a previous parse.
    """
    from unstructured.models import ParseResult
    from unstructured.export import export

    fmt = req.format.strip().lower()
    if fmt not in ("markdown", "html", "excel"):
        raise HTTPException(400, "format must be one of: markdown, html, excel")
    # Rebuild images dict: base64 -> (bytes, mime)
    images: Dict[str, Tuple[bytes, str]] = {}
    for rel, b64 in (req.images or {}).items():
        try:
            raw = base64.b64decode(b64)
            images[rel] = (raw, "image/jpeg")  # assume jpeg if unknown
        except Exception:
            continue
    result = ParseResult(
        md_lines=req.md_lines or [],
        html_lines=req.html_lines or [],
        structured_items=req.structured_items or [],
        images=images,
    )
    body = export(result, fmt)
    if fmt == "markdown":
        media_type, ext = "text/markdown", "md"
    elif fmt == "html":
        media_type, ext = "text/html", "html"
    else:
        media_type, ext = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"
    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="export.{ext}"'},
    )
