import streamlit as st
import os
from playwright.sync_api import sync_playwright

# -------------------------------
# 🔹 Install Playwright browser (only once)
# -------------------------------
PLAYWRIGHT_BROWSERS_PATH = "/home/appuser/.cache/ms-playwright"

if not os.path.exists(PLAYWRIGHT_BROWSERS_PATH):
    os.system("playwright install chromium")

# -------------------------------
# 🔹 Streamlit UI
# -------------------------------
st.set_page_config(page_title="Browser Automation", layout="centered")

st.title("🌐 Streamlit Browser Automation")
st.write("Enter a URL and fetch page details using Playwright")

url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")

# -------------------------------
# 🔹 Run Automation
# -------------------------------
if st.button("🚀 Run"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        try:
            with st.spinner("Launching browser..."):
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-dev-shm-usage"]
                    )

                    page = browser.new_page()
                    page.goto(url, timeout=60000)

                    # Extract data
                    title = page.title()

                    # Take screenshot
                    screenshot_path = "screenshot.png"
                    page.screenshot(path=screenshot_path, full_page=True)

                    browser.close()

            # -------------------------------
            # 🔹 Display Results
            # -------------------------------
            st.success("✅ Done!")

            st.subheader("📄 Page Title")
            st.write(title)

            st.subheader("📸 Screenshot")
            st.image(screenshot_path)

        except Exception as e:
            st.error("❌ Something went wrong")
            st.code(str(e))
