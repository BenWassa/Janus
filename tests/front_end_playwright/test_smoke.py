from pathlib import Path
import json
from playwright.sync_api import sync_playwright

def test_basic_flow():
    frontend_path = Path(__file__).resolve().parents[2] / "pilot_humility_hubris" / "frontend" / "index.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(frontend_path.as_uri())
        # Enable quick mode and telemetry for faster deterministic runs
        if page.is_visible('#quick'):
            page.check('#quick')
        if page.is_visible('#telemetry'):
            page.check('#telemetry')
        page.click('#play')
        choices = 0
        # Loop until reflection is visible or safety limit reached
        for _ in range(20):
            if page.is_visible('#reflection'):
                break
            page.wait_for_selector('#decision button')
            page.click('#decision button')
            choices += 1
            page.wait_for_timeout(50)
        assert page.is_visible('#reflection')
        # Telemetry should have at least one entry
        telemetry = page.evaluate("localStorage.getItem('janusTelemetry')")
        data = json.loads(telemetry)
        assert len(data) >= choices
        # Visual snapshot
        snap_dir = Path(__file__).parent / '__snapshots__'
        snap_dir.mkdir(exist_ok=True)
        snap_path = snap_dir / 'reflection.png'
        if not snap_path.exists():
            page.locator('#reflection').screenshot(path=snap_path)
        else:
            new_shot = page.locator('#reflection').screenshot()
            assert new_shot == snap_path.read_bytes()
        browser.close()
