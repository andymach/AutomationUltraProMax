import streamlit as st
import time
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Remote Browser Scroll Viewer", layout="wide")

st.title("🌐 Remote Browser Scroll Viewer")

url = st.text_input("Enter URL", placeholder="https://example.com")

if st.button("Run"):
    if not url:
        st.warning("Please enter a URL")
    else:
        try:
            placeholder = st.empty()

            with sync_playwright() as p:
                # 🔹 Connect to Browserless
                browser = p.chromium.connect_over_cdp(
                    "wss://chrome.browserless.io?token=2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"
                )

                # 🔹 Create context with viewport (fixes NoneType issue)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 800}
                )

                page = context.new_page()

                # 🔹 Open page
                page.goto(url, timeout=60000)
                page.wait_for_load_state("domcontentloaded")

                # 🔹 Give time to fully render
                page.wait_for_timeout(2000)

                # 🔹 Get dimensions safely
                total_height = page.evaluate("document.body.scrollHeight")
                viewport_height = page.evaluate("window.innerHeight")

                scroll_position = 0

                # 🔹 Scroll loop
                while scroll_position < total_height:
                    # Scroll
                    page.evaluate(f"window.scrollTo(0, {scroll_position})")

                    # Take screenshot (viewport only)
                    screenshot = page.screenshot(full_page=False)

                    # Show frame
                    placeholder.image(screenshot, use_container_width=True)

                    # Move scroll
                    scroll_position += viewport_height // 2

                    # 1 frame per second
                    time.sleep(1)

                browser.close()

            st.success("✅ Finished scrolling")

        except Exception as e:
            st.error("❌ Error occurred")
            st.code(str(e))
