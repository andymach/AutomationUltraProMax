import streamlit as st
import os
import time
from playwright.sync_api import sync_playwright

# -------------------------------
# 🔹 Ensure Playwright browser is installed
# -------------------------------
PLAYWRIGHT_PATH = "/home/appuser/.cache/ms-playwright"

if not os.path.exists(PLAYWRIGHT_PATH):
    os.system("playwright install chromium")

# -------------------------------
# 🔹 Session State Setup
# -------------------------------
if "browser_started" not in st.session_state:
    st.session_state.browser_started = False

if "url" not in st.session_state:
    st.session_state.url = ""

# -------------------------------
# 🔹 UI
# -------------------------------
st.set_page_config(page_title="Mini Browser", layout="wide")

st.title("🌐 Mini Browser (Simulated)")

col1, col2 = st.columns([1, 2])

# -------------------------------
# 🔹 LEFT PANEL (Controls)
# -------------------------------
with col1:
    st.subheader("Controls")

    url_input = st.text_input("Enter URL", value=st.session_state.url)

    if st.button("Open Page"):
        st.session_state.url = url_input
        st.session_state.browser_started = True

    click_selector = st.text_input("CSS Selector to Click (optional)")
    fill_selector = st.text_input("CSS Selector to Fill (optional)")
    fill_value = st.text_input("Value to Fill")

    action = st.selectbox("Action", ["None", "Click", "Fill"])

    run_action = st.button("Run Action")
    refresh = st.button("Refresh Page")

# -------------------------------
# 🔹 RIGHT PANEL (Browser View)
# -------------------------------
with col2:
    st.subheader("Browser View")

    if st.session_state.browser_started and st.session_state.url:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled"
                    ]
                )

                # 🔥 Use context (important for stealth)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                    viewport={"width": 1280, "height": 800},
                    locale="en-US"
                )

                page = context.new_page()

                # 🔥 Extra headers
                page.set_extra_http_headers({
                    "Accept-Language": "en-US,en;q=0.9"
                })

                # 🔥 Go to page with wait
                page.goto(st.session_state.url, timeout=60000)
                page.wait_for_load_state("domcontentloaded")

                time.sleep(2)  # mimic human delay

                # -------------------------------
                # 🔹 Perform action
                # -------------------------------
                if run_action:
                    if action == "Click" and click_selector:
                        page.wait_for_selector(click_selector, timeout=5000)
                        page.click(click_selector)
                        time.sleep(2)

                    elif action == "Fill" and fill_selector:
                        page.wait_for_selector(fill_selector, timeout=5000)
                        page.fill(fill_selector, fill_value)
                        time.sleep(1)

                if refresh:
                    page.reload()
                    time.sleep(2)

                # -------------------------------
                # 🔹 Screenshot
                # -------------------------------
                screenshot_path = "page.png"
                page.screenshot(path=screenshot_path, full_page=True)

                title = page.title()

                browser.close()

            st.success(f"Loaded: {title}")
            st.image(screenshot_path, use_container_width=True)

        except Exception as e:
            st.error("Error loading page")
            st.code(str(e))

    else:
        st.info("Enter a URL and click 'Open Page'")
