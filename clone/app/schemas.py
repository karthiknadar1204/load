"""Pydantic schemas for API request/response."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    """Standard envelope for all API responses."""
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None


class HealthData(BaseModel):
    """Health check payload."""
    status: str = "ok"
    supported_export_formats: List[str] = Field(default_factory=lambda: ["markdown", "html", "excel"])


class ExportRequest(BaseModel):
    """Request body for POST /api/v1/export."""
    md_lines: List[str] = Field(default_factory=list, description="Markdown content lines")
    html_lines: List[str] = Field(default_factory=list, description="HTML content lines")
    structured_items: List[Dict[str, Any]] = Field(default_factory=list, description="Tables/charts data")
    images: Dict[str, str] = Field(default_factory=dict, description="Rel path -> base64 image data")
    format: str = Field(..., description="One of: markdown, html, excel")
