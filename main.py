import streamlit as st
import os
import time
import random
from playwright.sync_api import sync_playwright

# -------------------------------
# 🔹 Install Chromium if needed
# -------------------------------
PLAYWRIGHT_PATH = "/home/appuser/.cache/ms-playwright"

if not os.path.exists(PLAYWRIGHT_PATH):
    os.system("playwright install chromium")

# -------------------------------
# 🔹 Session State
# -------------------------------
if "browser_started" not in st.session_state:
    st.session_state.browser_started = False

if "url" not in st.session_state:
    st.session_state.url = ""

# -------------------------------
# 🔹 UI
# -------------------------------
st.set_page_config(page_title="Mini Browser (Stealth Fixed)", layout="wide")
st.title("🌐 Mini Browser (Stable Version)")

col1, col2 = st.columns([1, 2])

# -------------------------------
# 🔹 Controls
# -------------------------------
with col1:
    st.subheader("Controls")

    url_input = st.text_input("Enter URL", value=st.session_state.url)

    if st.button("Open Page"):
        st.session_state.url = url_input
        st.session_state.browser_started = True

    click_selector = st.text_input("CSS Selector to Click")
    fill_selector = st.text_input("CSS Selector to Fill")
    fill_value = st.text_input("Value")

    action = st.selectbox("Action", ["None", "Click", "Fill"])

    run_action = st.button("Run Action")
    refresh = st.button("Refresh")

# -------------------------------
# 🔹 Human Simulation
# -------------------------------
def simulate_human(page):
    try:
        page.mouse.move(random.randint(100, 400), random.randint(100, 400))
        time.sleep(random.uniform(0.5, 1.5))

        page.mouse.move(random.randint(400, 800), random.randint(200, 600))
        time.sleep(random.uniform(0.5, 1.5))

        page.mouse.wheel(0, random.randint(200, 800))
        time.sleep(random.uniform(1, 2))
    except:
        pass

# -------------------------------
# 🔹 Browser View
# -------------------------------
with col2:
    st.subheader("Browser View")

    if st.session_state.browser_started and st.session_state.url:
        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=True,  # 🔴 MUST be True on Streamlit Cloud
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars"
                    ]
                )

                context = browser.new_context(
                    user_agent=random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119 Safari/537.36"
                    ]),
                    viewport={"width": 1280, "height": 800},
                    locale="en-US",
                    java_script_enabled=True
                )

                page = context.new_page()

                # -------------------------------
                # 🔥 Manual Stealth Injection
                # -------------------------------
                page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                window.chrome = {
                    runtime: {}
                };

                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });

                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                """)

                # -------------------------------
                # 🔹 Headers
                # -------------------------------
                page.set_extra_http_headers({
                    "Accept-Language": "en-US,en;q=0.9",
                    "Upgrade-Insecure-Requests": "1"
                })

                # -------------------------------
                # 🔹 Open Page
                # -------------------------------
                page.goto(st.session_state.url, timeout=60000)
                page.wait_for_load_state("networkidle")

                time.sleep(random.uniform(2, 4))
                simulate_human(page)

                # -------------------------------
                # 🔹 Actions
                # -------------------------------
                if run_action:
                    if action == "Click" and click_selector:
                        page.wait_for_selector(click_selector, timeout=8000)
                        simulate_human(page)
                        page.click(click_selector)
                        time.sleep(random.uniform(1, 3))

                    elif action == "Fill" and fill_selector:
                        page.wait_for_selector(fill_selector, timeout=8000)
                        page.fill(fill_selector, fill_value)
                        time.sleep(random.uniform(1, 2))

                if refresh:
                    page.reload()
                    page.wait_for_load_state("networkidle")
                    simulate_human(page)

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
        st.info("Enter a URL and click Open Page")
