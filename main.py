import streamlit as st
import requests
import time

st.set_page_config(layout="wide")
st.title("🌐 Browser Streaming (Robust Version)")

# 🔑 Put your Browserless API key here
TOKEN = "YOUR_API_KEY"

url = st.text_input(
    "Enter URL",
    value="https://www.bajajfinserv.in/tnc-b2c-urban"
)

start = st.button("Start Streaming")

placeholder = st.empty()
debug_box = st.expander("🔍 Debug Info")

# -------------------------------
# 🔹 API CALL FUNCTION
# -------------------------------
def get_screenshot(scroll_y=0):
    try:
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

        # ✅ If valid image → return
        if res.status_code == 200 and "image" in res.headers.get("content-type", ""):
            return res.content

        # 🔁 Fallback to UNBLOCK
        debug_box.write("⚠️ Switching to /unblock...")

        unblock_url = f"https://production-sfo.browserless.io/unblock?token={TOKEN}"

        res2 = requests.post(unblock_url, json={"url": url})

        if res2.status_code == 200 and "image" in res2.headers.get("content-type", ""):
            return res2.content

        # ❌ Still failed → show debug
        debug_box.write("❌ Not an image response")
        debug_box.write("Status:", res2.status_code)
        debug_box.code(res2.text[:1000])

        return None

    except Exception as e:
        debug_box.write("🔥 Exception occurred")
        debug_box.code(str(e))
        return None


# -------------------------------
# 🔹 STREAMING LOOP
# -------------------------------
if start:
    scroll = 0

    for i in range(20):  # limit frames (avoid infinite loop)
        img = get_screenshot(scroll)

        if img:
            placeholder.image(img, use_container_width=True)
        else:
            st.error("Stopping due to invalid response")
            break

        scroll += 400
        time.sleep(1)

    st.success("✅ Streaming finished")
