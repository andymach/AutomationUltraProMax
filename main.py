import streamlit as st
import requests
import time

st.set_page_config(layout="wide")
st.title("🌐 Browser Streaming (Fixed)")

TOKEN = "2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"

url = st.text_input(
    "Enter URL",
    value="https://www.bajajfinserv.in/tnc-b2c-urban"
)

start = st.button("Start Streaming")

placeholder = st.empty()
debug_box = st.expander("🔍 Debug Info")


# -------------------------------
# 🔹 Screenshot API
# -------------------------------
def get_screenshot(scroll_y=0):
    api_url = f"https://production-sfo.browserless.io/screenshot?token={TOKEN}"

    payload = {
        "url": url,
        "viewport": {"width": 1280, "height": 800},
        "gotoOptions": {
            "waitUntil": "domcontentloaded",
            "timeout": 60000
        },
        "scripts": [
            f"window.scrollTo(0, {scroll_y})"
        ]
    }

    res = requests.post(api_url, json=payload)

    if res.status_code == 200 and "image" in res.headers.get("content-type", ""):
        return res.content

    # Debug safely
    with debug_box:
        st.write(f"❌ Screenshot failed: {res.status_code}")
        st.code(res.text[:500])

    return None


# -------------------------------
# 🔹 HTML fallback (unblock)
# -------------------------------
def get_html():
    api_url = f"https://production-sfo.browserless.io/unblock?token={TOKEN}"

    res = requests.post(api_url, json={"url": url})

    if res.status_code == 200:
        return res.text

    return None


# -------------------------------
# 🔹 MAIN FLOW
# -------------------------------
if start:
    scroll = 0
    success = False

    for i in range(10):  # limit frames
        img = get_screenshot(scroll)

        if img:
            placeholder.image(img, use_container_width=True)
            success = True
            scroll += 400
            time.sleep(1)
        else:
            break

    # 🔁 If screenshot failed → fallback to HTML
    if not success:
        st.warning("⚠️ Falling back to HTML view")

        html = get_html()

        if html:
            st.components.v1.html(html, height=800, scrolling=True)
        else:
            st.error("❌ Could not load page")

    else:
        st.success("✅ Streaming finished")
