# API: How to start the server and test with Postman

## 1. Start the server

From the **clone** directory (project root of this repo):

```bash
cd /path/to/load/clone
```

Install the package in editable mode so the `unstructured` and `app` modules are importable:

```bash
pip install -e .
```

Then start the FastAPI app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Without** installing: run with `PYTHONPATH=src` so `unstructured` is found:

```bash
PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Docs (Swagger UI): **http://localhost:8000/docs**
- Health: **http://localhost:8000/api/v1/health**

**Note:** The **parse** and **parse-and-export** endpoints use `StructuredPDFParser`, which depends on the full **doctra** stack (layout, OCR, etc.). If those dependencies are not installed or not on `PYTHONPATH`, those routes will return **503** with a message. The **health** and **export** (POST with pre-parsed JSON) endpoints work without the parser.

---

## 2. Test with Postman

### Health check

- **Method:** GET  
- **URL:** `http://localhost:8000/api/v1/health`  
- **Headers:** none  
- **Body:** none  

Expected response (200):

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "supported_export_formats": ["markdown", "html", "excel"]
  },
  "error": null
}
```

---

### Parse a PDF (return JSON)

- **Method:** POST  
- **URL:** `http://localhost:8000/api/v1/documents/parse`  
- **Headers:** none (Postman will set `Content-Type: multipart/form-data` when you add a body file).  
- **Body:** form-data  
  - Key: `file` (type: **File**)  
  - Value: choose a PDF file from your machine  

Expected: 200 with JSON like:

```json
{
  "success": true,
  "data": {
    "md_lines": ["# Extracted Content\n", ...],
    "html_lines": ["<h1>Extracted Content</h1>", ...],
    "structured_items": [...],
    "images": { "images/figures/page_001_figure_001.jpg": "<base64>" }
  },
  "error": null
}
```

---

### Parse and export (file in → file out)

- **Method:** POST  
- **URL:** `http://localhost:8000/api/v1/documents/parse-and-export`  
- **Body:** form-data  
  - `file` (File): your PDF  
  - `format` (Text): one of `markdown`, `html`, `excel`  

Expected: 200 with **raw file** in the response (Save Response → Save to a file to get the .md / .html / .xlsx).  
Content-Type and filename depend on `format`.

---

### Export (pre-parsed content → file)

Use when you already have a parse result (e.g. from a previous `/documents/parse` call) and want to export to another format.

- **Method:** POST  
- **URL:** `http://localhost:8000/api/v1/export`  
- **Headers:** `Content-Type: application/json`  
- **Body:** raw JSON  

Example:

```json
{
  "md_lines": ["# Extracted Content\n", "\n## Page 1\n", "Some text.\n"],
  "html_lines": ["<h1>Extracted Content</h1>", "<h2>Page 1</h2>", "<p>Some text.</p>"],
  "structured_items": [],
  "images": {},
  "format": "html"
}
```

Set `format` to `markdown`, `html`, or `excel`.  
Expected: 200 with the exported file as the response body (e.g. HTML or Markdown text, or Excel binary). You can “Send and Download” in Postman to save the file.

---

## 3. Quick checklist in Postman

| What you want           | Method | URL                                          | Body / Params                    |
|-------------------------|--------|----------------------------------------------|----------------------------------|
| Health                  | GET    | `http://localhost:8000/api/v1/health`         | —                                |
| Parse PDF → JSON        | POST   | `http://localhost:8000/api/v1/documents/parse`| form-data: `file` = PDF          |
| Parse PDF → download file | POST | `http://localhost:8000/api/v1/documents/parse-and-export` | form-data: `file` = PDF, `format` = html / markdown / excel |
| Export JSON → file      | POST   | `http://localhost:8000/api/v1/export`        | raw JSON (see example above)     |

Use **Send and Download** for the two POST endpoints that return a file so Postman saves the response as a file.
