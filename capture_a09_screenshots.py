import asyncio
import os
from playwright.async_api import async_playwright

async def capture_all():
    out_dir = r"backend\sandbox\screenshots"
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        # Login to Grafana
        try:
            print("Logging into Grafana...")
            await page.goto("http://localhost:3000/login", wait_until="networkidle")
            await page.fill('input[name="user"]', "admin")
            await page.fill('input[name="password"]', "admin")
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Login notice: {e}")

        # 1. Grafana Datasources UI
        try:
            print("Capturing Grafana Datasources UI...")
            await page.goto("http://localhost:3000/connections/datasources", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_grafana_datasources_wtn_a09.png"))
            print("Captured screenshot_grafana_datasources_wtn_a09.png")
        except Exception as e:
            print(f"Error Grafana Datasources: {e}")

        # 2. Prometheus Targets UI
        try:
            print("Capturing Prometheus Targets UI...")
            await page.goto("http://localhost:9090/targets", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_prometheus_ui_wtn_a09.png"))
            print("Captured screenshot_prometheus_ui_wtn_a09.png")
        except Exception as e:
            print(f"Error Prometheus UI: {e}")

        # 3. Grafana Metrics Explorer
        try:
            print("Capturing Grafana Metrics Explorer...")
            await page.goto("http://localhost:3000/explore?left=%7B%22datasource%22:%22Prometheus%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22up%22%7D%5D%7D", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_grafana_metrics_dashboard_wtn_a09.png"))
            print("Captured screenshot_grafana_metrics_dashboard_wtn_a09.png")
        except Exception as e:
            print(f"Error Grafana Metrics: {e}")

        # 4. Grafana Loki Logs
        try:
            print("Capturing Grafana Loki Logs...")
            await page.goto("http://localhost:3000/explore?left=%7B%22datasource%22:%22Loki%22%7D", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_grafana_loki_logs_wtn_a09.png"))
            print("Captured screenshot_grafana_loki_logs_wtn_a09.png")
        except Exception as e:
            print(f"Error Grafana Loki: {e}")

        # 5. Grafana Tempo Traces
        try:
            print("Capturing Grafana Tempo Traces...")
            await page.goto("http://localhost:3000/explore?left=%7B%22datasource%22:%22Tempo%22%7D", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_grafana_tempo_traces_wtn_a09.png"))
            print("Captured screenshot_grafana_tempo_traces_wtn_a09.png")
        except Exception as e:
            print(f"Error Grafana Tempo: {e}")

        # 6. Swagger Predict API Telemetry UI (expanded)
        try:
            print("Capturing Swagger Predict API Telemetry UI...")
            await page.goto("http://localhost:8000/docs#/Inference%20Domain/enqueue_prediction_api_v1_inference_predict_post", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=os.path.join(out_dir, "screenshot_predict_api_telemetry_wtn_a09.png"))
            print("Captured screenshot_predict_api_telemetry_wtn_a09.png")
        except Exception as e:
            print(f"Error Swagger UI: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_all())
