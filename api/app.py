import json
import os
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen

import fitz
from flask import Flask, jsonify, abort, Response, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

COMPONENTS_DIR = os.environ.get("COMPONENTS_DIR", "/components")
CATALOG_PATH = os.path.join(COMPONENTS_DIR, "catalog.json")
DEFAULT_TIMEOUT_SECONDS = 30
MAX_PDF_BYTES = 35 * 1024 * 1024
TEMP_PNG_TTL_SECONDS = int(os.environ.get("TEMP_PNG_TTL_SECONDS", "3600"))
TEMP_PNG_DIR = os.environ.get("TEMP_PNG_DIR", "/tmp/lib-components-american/page-1")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").strip().rstrip("/")
TEMP_PNG_INDEX = {}

TEMP_IMAGE_DIR = os.environ.get("TEMP_IMAGE_DIR", "/tmp/lib-components-american/images")
TEMP_IMAGE_INDEX = {}


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _utc_iso(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _cleanup_expired_temp_pngs():
    now = int(time.time())
    expired_tokens = [
        token for token, metadata in TEMP_PNG_INDEX.items()
        if metadata.get("expires_at", 0) <= now
    ]
    for token in expired_tokens:
        metadata = TEMP_PNG_INDEX.pop(token, None)
        if not metadata:
            continue
        path = metadata.get("path", "")
        if path and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass


def _store_temp_png(png_bytes):
    _cleanup_expired_temp_pngs()
    os.makedirs(TEMP_PNG_DIR, exist_ok=True)

    token = uuid.uuid4().hex
    path = os.path.join(TEMP_PNG_DIR, f"{token}.png")
    with open(path, "wb") as f:
        f.write(png_bytes)

    expires_at = int(time.time()) + TEMP_PNG_TTL_SECONDS
    TEMP_PNG_INDEX[token] = {"path": path, "expires_at": expires_at}
    return token, expires_at


def _normalize_pdf_url(raw_url):
    cleaned = "".join(ch for ch in str(raw_url).strip() if ch not in "\r\n\t")
    parts = urlsplit(cleaned)
    if parts.scheme not in ("http", "https"):
        return cleaned

    path = quote(parts.path, safe="/%:@")
    query = quote(parts.query, safe="=&%:@/?")
    fragment = quote(parts.fragment, safe="=&%:@/?")
    return urlunsplit((parts.scheme, parts.netloc, path, query, fragment))


def _read_pdf_url():
    if request.method == "GET":
        pdf_url = _normalize_pdf_url(request.args.get("pdf_url", ""))
        return pdf_url

    payload = request.get_json(silent=True) or {}
    return _normalize_pdf_url(payload.get("pdf_url", ""))


def _download_pdf(pdf_url):
    parsed = urlparse(pdf_url)
    if parsed.scheme not in ("http", "https"):
        abort(400, description="pdf_url must start with http:// or https://")

    req = Request(
        pdf_url,
        headers={
            "User-Agent": "lib-components-american/1.0",
            "Accept": "application/pdf,*/*",
        },
    )

    try:
        with urlopen(req, timeout=DEFAULT_TIMEOUT_SECONDS) as resp:
            chunks = []
            total = 0
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_PDF_BYTES:
                    abort(413, description="PDF is too large for this endpoint")
                chunks.append(chunk)
            return b"".join(chunks)
    except HTTPException:
        raise
    except Exception as e:
        abort(400, description=f"Could not download PDF: {e}")


def _build_temp_png_url(token):
    if PUBLIC_BASE_URL:
        return f"{PUBLIC_BASE_URL}/pdf/page-1/temp/{token}"

    forwarded_proto = request.headers.get("X-Forwarded-Proto", "").strip()
    forwarded_host = request.headers.get("X-Forwarded-Host", "").strip()
    if forwarded_proto and forwarded_host:
        return f"{forwarded_proto}://{forwarded_host}/pdf/page-1/temp/{token}"

    return f"{request.url_root.rstrip('/')}/pdf/page-1/temp/{token}"


# ── 1. List all components from catalog.json ─────────────────────────────────
# Used as an OCR prompt: gives the LLM the full component list so it can
# categorize which blocks appear in the PDF.
@app.route("/components", methods=["GET"])
def list_components():
    catalog = load_catalog()
    return jsonify(catalog)


# ── 2. List files inside a specific component folder ─────────────────────────
# Used by a second OCR to inspect what variants exist for a given component type.
@app.route("/components/<folder>", methods=["GET"])
def list_component_folder(folder):
    folder_path = os.path.join(COMPONENTS_DIR, folder)
    if not os.path.isdir(folder_path):
        abort(404, description=f"Folder '{folder}' not found")

    files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".html")
    ]

    catalog = load_catalog()
    matching = [
        c for c in catalog.get("components", [])
        if c.get("file", "").startswith(f"{folder}/")
    ]

    return jsonify({
        "folder": folder,
        "files": sorted(files),
        "components": matching,
    })


# ── 3. Return raw HTML of a component by id or name ──────────────────────────
# The n8n workflow fetches this to get the actual HTML block to inject.
@app.route("/html/<identifier>", methods=["GET"])
def get_component_html(identifier):
    catalog = load_catalog()
    components = catalog.get("components", [])

    # Match by id (exact) or name (case-insensitive)
    component = None
    for c in components:
        if c.get("id") == identifier:
            component = c
            break
        if c.get("name", "").lower() == identifier.lower():
            component = c
            break

    if not component:
        abort(404, description=f"Component '{identifier}' not found")

    file_rel = component.get("file")
    if not file_rel:
        abort(500, description="Component has no file path in catalog")

    file_path = os.path.join(COMPONENTS_DIR, file_rel)
    if not os.path.isfile(file_path):
        abort(404, description=f"HTML file not found: {file_rel}")

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    return Response(html_content, mimetype="text/html")


# ── 4. Render first page of a PDF URL as PNG ────────────────────────────────
# Useful for OCR/image workflows where page 1 is needed as an image.
@app.route("/pdf/page-1", methods=["GET", "POST"])
def get_pdf_page_1():
    pdf_url = _read_pdf_url()
    if not pdf_url:
        abort(400, description="Missing 'pdf_url'")

    pdf_bytes = _download_pdf(pdf_url)

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            if doc.page_count < 1:
                abort(400, description="PDF has no pages")
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150, alpha=False)
            png_bytes = pix.tobytes("png")
    except Exception as e:
        abort(400, description=f"Could not render PDF page 1: {e}")

    token, expires_at = _store_temp_png(png_bytes)
    return jsonify({
        "png_url": _build_temp_png_url(token),
        "expires_at": _utc_iso(expires_at),
        "expires_in_seconds": TEMP_PNG_TTL_SECONDS,
    })


@app.route("/pdf/page-1/temp/<token>", methods=["GET"])
def get_temp_pdf_page_1(token):
    _cleanup_expired_temp_pngs()
    metadata = TEMP_PNG_INDEX.get(token)
    if not metadata:
        abort(404, description="Temporary PNG not found or expired")

    expires_at = int(metadata.get("expires_at", 0))
    now = int(time.time())
    if expires_at <= now:
        path = metadata.get("path", "")
        TEMP_PNG_INDEX.pop(token, None)
        if path and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass
        abort(410, description="Temporary PNG URL expired")

    path = metadata.get("path", "")
    if not path or not os.path.isfile(path):
        TEMP_PNG_INDEX.pop(token, None)
        abort(404, description="Temporary PNG not found")

    with open(path, "rb") as f:
        png_bytes = f.read()

    max_age = max(expires_at - now, 0)
    return Response(
        png_bytes,
        mimetype="image/png",
        headers={"Cache-Control": f"private, max-age={max_age}"},
    )


# ── helpers: temp image storage (mirrors temp PNG pattern) ───────────────────

def _cleanup_expired_temp_images():
    now = int(time.time())
    expired = [t for t, m in TEMP_IMAGE_INDEX.items() if m.get("expires_at", 0) <= now]
    for token in expired:
        meta = TEMP_IMAGE_INDEX.pop(token, None)
        if meta:
            path = meta.get("path", "")
            if path and os.path.isfile(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


def _store_temp_image(img_bytes, ext="png"):
    _cleanup_expired_temp_images()
    os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
    token = uuid.uuid4().hex
    path = os.path.join(TEMP_IMAGE_DIR, f"{token}.{ext}")
    with open(path, "wb") as f:
        f.write(img_bytes)
    expires_at = int(time.time()) + TEMP_PNG_TTL_SECONDS
    TEMP_IMAGE_INDEX[token] = {"path": path, "ext": ext, "expires_at": expires_at}
    return token, expires_at


def _build_temp_image_url(token):
    if PUBLIC_BASE_URL:
        return f"{PUBLIC_BASE_URL}/pdf/images/temp/{token}"
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "").strip()
    forwarded_host = request.headers.get("X-Forwarded-Host", "").strip()
    if forwarded_proto and forwarded_host:
        return f"{forwarded_proto}://{forwarded_host}/pdf/images/temp/{token}"
    return f"{request.url_root.rstrip('/')}/pdf/images/temp/{token}"


# ── 5. Extract all images from a PDF with coordinates ────────────────────────
# For each embedded image: returns a temp public URL + bounding box coordinates
# (x0, y0, x1, y1 in PDF points; origin at bottom-left of page).
# Used by n8n to identify and fetch real images to inject into email components.
@app.route("/pdf/images", methods=["GET", "POST"])
def extract_pdf_images():
    pdf_url = _read_pdf_url()
    if not pdf_url:
        abort(400, description="Missing 'pdf_url'")

    pdf_bytes = _download_pdf(pdf_url)

    images = []
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            total_pages = doc.page_count
            for page_index in range(total_pages):
                page = doc.load_page(page_index)
                page_no = page_index + 1
                image_list = page.get_images(full=True)

                for img_i, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base = doc.extract_image(xref)
                    img_bytes = base["image"]
                    ext = base.get("ext", "png")
                    width = base.get("width", 0)
                    height = base.get("height", 0)
                    colorspace = base.get("colorspace", "unknown")
                    if isinstance(colorspace, int):
                        colorspace = {1: "DeviceGray", 3: "DeviceRGB", 4: "DeviceCMYK"}.get(
                            colorspace, f"Colorspace-{colorspace}"
                        )
                    elif not isinstance(colorspace, str):
                        colorspace = str(colorspace)

                    try:
                        bbox = page.get_image_bbox(img)
                        x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
                        bbox_width, bbox_height = bbox.width, bbox.height
                    except Exception:
                        x0 = y0 = x1 = y1 = bbox_width = bbox_height = None

                    token, expires_at = _store_temp_image(img_bytes, ext)
                    images.append({
                        "filename": f"page{page_no:03d}_img{img_i:02d}_xref{xref}.{ext}",
                        "page_number": page_no,
                        "url": _build_temp_image_url(token),
                        "expires_at": _utc_iso(expires_at),
                        "width": width,
                        "height": height,
                        "format": ext,
                        "size_bytes": len(img_bytes),
                        "color_space": colorspace,
                        "x0": x0,
                        "y0": y0,
                        "x1": x1,
                        "y1": y1,
                        "bbox_width": bbox_width,
                        "bbox_height": bbox_height,
                    })
    except Exception as e:
        abort(400, description=f"Could not extract images from PDF: {e}")

    expires_in = TEMP_PNG_TTL_SECONDS
    first_expires = images[0]["expires_at"] if images else None

    return jsonify({
        "total_pages": total_pages,
        "total_images": len(images),
        "expires_in_seconds": expires_in,
        "expires_at": first_expires,
        "coordinate_note": "x0/y0/x1/y1 in PDF points (72pt = 1 inch). Origin (0,0) at bottom-left of page.",
        "images": images,
    })


# ── 6. Serve a single extracted image by token ───────────────────────────────
@app.route("/pdf/images/temp/<token>", methods=["GET"])
def get_temp_pdf_image(token):
    _cleanup_expired_temp_images()
    meta = TEMP_IMAGE_INDEX.get(token)
    if not meta:
        abort(404, description="Image not found or expired")

    now = int(time.time())
    expires_at = int(meta.get("expires_at", 0))
    if expires_at <= now:
        path = meta.get("path", "")
        TEMP_IMAGE_INDEX.pop(token, None)
        if path and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass
        abort(410, description="Image URL expired")

    path = meta.get("path", "")
    if not path or not os.path.isfile(path):
        TEMP_IMAGE_INDEX.pop(token, None)
        abort(404, description="Image file not found")

    ext = meta.get("ext", "png")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "webp": "image/webp"}
    mimetype = mime_map.get(ext.lower(), "application/octet-stream")

    with open(path, "rb") as f:
        img_bytes = f.read()

    max_age = max(expires_at - now, 0)
    return Response(
        img_bytes,
        mimetype=mimetype,
        headers={"Cache-Control": f"private, max-age={max_age}"},
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
