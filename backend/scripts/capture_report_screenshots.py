import os
import sys
import time
import csv
import openpyxl
import subprocess
from playwright.sync_api import sync_playwright

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
screenshots_dir = os.path.join(backend_dir, "sandbox", "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

def render_excel_html():
    excel_path = os.path.join(backend_dir, "api_list_snapshot.xlsx")
    if not os.path.exists(excel_path):
        return ""
    
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    html = """<!DOCTYPE html><html><head><style>
    body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f4f6f9; margin: 20px; }
    h2 { color: #1F4E78; text-align: center; }
    table { width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
    th { background-color: #1F4E78; color: white; padding: 12px; font-size: 13px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #e0e0e0; font-size: 12px; vertical-align: top; }
    tr:nth-child(even) { background-color: #f9fafb; }
    .badge-get { background: #E2EFDA; color: #276A3C; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-post { background: #FCE4D6; color: #A61C1C; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-delete { background: #FCE4D6; color: #C00000; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style></head><body>
    <h2>📊 Snapshot API List (.xlsx Export Render)</h2>
    <table><thead><tr>
        <th>Domain / Tag</th><th>API Endpoint Path</th><th>HTTP Verb</th><th>Summary</th><th>Description</th><th>Parameters</th><th>Status Codes</th>
    </tr></thead><tbody>"""
    
    for row in list(ws.iter_rows(values_only=True))[4:]: # Skip header title rows
        if not any(row):
            continue
        tag, path, verb, summary, desc, params, status = row[:7]
        badge_cls = "badge-get" if verb == "GET" else ("badge-post" if verb == "POST" else "badge-delete")
        params_formatted = (params or "").replace('\n', '<br>')
        html += f"""<tr>
            <td><b>{tag}</b></td>
            <td><code>{path}</code></td>
            <td><span class="{badge_cls}">{verb}</span></td>
            <td>{summary or ''}</td>
            <td>{desc or ''}</td>
            <td>{params_formatted}</td>
            <td><code>{status or ''}</code></td>
        </tr>"""
        
    html += "</tbody></table></body></html>"
    
    html_path = os.path.join(screenshots_dir, "excel_preview.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path

def capture_screenshots():
    print("Starting FastAPI server in background for screenshot capture...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3) # Wait for server startup

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 900})

            # 1. Swagger UI (/docs)
            print("Capturing Swagger UI screenshot...")
            page.goto("http://127.0.0.1:8000/docs", wait_until="networkidle")
            time.sleep(1.5)
            page.screenshot(path=os.path.join(screenshots_dir, "screenshot_swagger_ui.png"), full_page=False)

            # 2. ReDoc (/redoc)
            print("Capturing ReDoc screenshot...")
            page.goto("http://127.0.0.1:8000/redoc", wait_until="networkidle")
            time.sleep(2)
            page.screenshot(path=os.path.join(screenshots_dir, "screenshot_redoc_ui.png"), full_page=False)

            # 3. OpenAPI JSON (/api/v1/openapi.json)
            print("Capturing OpenAPI JSON screenshot...")
            page.goto("http://127.0.0.1:8000/api/v1/openapi.json", wait_until="networkidle")
            time.sleep(0.5)
            page.screenshot(path=os.path.join(screenshots_dir, "screenshot_openapi_json.png"), full_page=False)

            # 4. Health Check (/api/v1/system/health)
            print("Capturing Health Check screenshot...")
            page.goto("http://127.0.0.1:8000/api/v1/system/health", wait_until="networkidle")
            time.sleep(0.5)
            page.screenshot(path=os.path.join(screenshots_dir, "screenshot_health_check.png"), full_page=False)

            # 5. Rendered Excel Snapshot (.xlsx)
            print("Capturing Excel snapshot preview...")
            html_file = render_excel_html()
            if html_file:
                page.goto(f"file:///{html_file.replace(os.sep, '/')}")
                time.sleep(1)
                page.screenshot(path=os.path.join(screenshots_dir, "screenshot_excel_snapshot.png"), full_page=False)

            browser.close()
            print("All live screenshots captured successfully!")
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    capture_screenshots()
