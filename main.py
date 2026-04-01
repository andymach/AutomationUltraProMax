import streamlit as st
import time
from playwright.sync_api import sync_playwright

st.title("🌐 Remote Browser Scroll Viewer")

url = st.text_input("Enter URL")

if st.button("Run"):
    if not url:
        st.warning("Enter URL")
    else:
        try:
            placeholder = st.empty()

            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(
                    "wss://chrome.browserless.io?token=YOUR_API_KEY"
                )

                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.new_page()

                page.goto(url, timeout=60000)
                page.wait_for_load_state("domcontentloaded")

                # Get total height
                total_height = page.evaluate("document.body.scrollHeight")
                viewport_height = page.viewport_size["height"]

                scroll_position = 0

                while scroll_position < total_height:
                    # Scroll
                    page.evaluate(f"window.scrollTo(0, {scroll_position})")

                    # Take screenshot
                    screenshot = page.screenshot(full_page=False)

                    # Show frame
                    placeholder.image(screenshot)

                    # Move down
                    scroll_position += viewport_height // 2

                    time.sleep(1)  # 1 frame per second

                browser.close()

            st.success("✅ Finished scrolling")

        except Exception as e:
            st.error(str(e))
