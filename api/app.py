import json
import os
from flask import Flask, jsonify, abort, Response

app = Flask(__name__)

COMPONENTS_DIR = os.environ.get("COMPONENTS_DIR", "/components")
CATALOG_PATH = os.path.join(COMPONENTS_DIR, "catalog.json")


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
