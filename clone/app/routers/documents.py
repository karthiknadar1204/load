"""Document parse and parse-and-export endpoints."""
from __future__ import annotations

import base64
import os
import tempfile
from typing import Tuple

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.schemas import ApiResponse

router = APIRouter(prefix="/documents", tags=["documents"])


def _get_parser():
    """Lazy import to avoid pulling in doctra/parser until needed."""
    try:
        from unstructured.parsers.structured_pdf_parser import StructuredPDFParser
        return StructuredPDFParser()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Parser not available (install full doctra/unstructured stack): {e!s}",
        )


@router.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    """
    Upload a PDF, parse it, return structured content as JSON.
    Images are returned as base64 in the `images` map.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    parser = _get_parser()
    content = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        try:
            tmp.write(content)
            tmp.flush()
            result = parser.parse(tmp.name)
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
    # Serialize for JSON: images bytes -> base64
    images_b64 = {k: base64.b64encode(v[0]).decode("ascii") for k, v in result.images.items()}
    return ApiResponse(success=True, data={
        "md_lines": result.md_lines,
        "html_lines": result.html_lines,
        "structured_items": result.structured_items,
        "images": images_b64,
    })


@router.post("/parse-and-export")
async def parse_and_export(
    file: UploadFile = File(...),
    format: str = Form("html", description="One of: markdown, html, excel"),
):
    """
    Upload a PDF, parse it, and return the export as a file (no JSON).
    Use format=markdown, html, or excel. Response is the raw file bytes.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    fmt = format.strip().lower()
    if fmt not in ("markdown", "html", "excel"):
        raise HTTPException(400, "format must be one of: markdown, html, excel")
    parser = _get_parser()
    content = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        try:
            tmp.write(content)
            tmp.flush()
            result = parser.parse(tmp.name)
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
    from unstructured.export import export
    body = export(result, fmt)
    filename = (file.filename or "document").rsplit(".", 1)[0]
    if fmt == "markdown":
        media_type, ext = "text/markdown", "md"
    elif fmt == "html":
        media_type, ext = "text/html", "html"
    else:
        media_type, ext = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"
    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}.{ext}"'},
    )
