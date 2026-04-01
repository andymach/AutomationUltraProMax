import streamlit as st
import requests
import time

st.set_page_config(layout="wide")
st.title("🌐 Browser Screenshot Stream")

TOKEN = "2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"

url = st.text_input(
    "Enter URL",
    value="https://www.bajajfinserv.in/tnc-b2c-urban"
)

start = st.button("Start")

placeholder = st.empty()


def get_screenshot(target_url):
    api_url = f"https://production-sfo.browserless.io/screenshot?token={TOKEN}&blockAds=false&timeout=60000"

    payload = {
        "url": target_url,
        "options": {
            "fullPage": False
        },
        "viewport": {
            "width": 1280,
            "height": 800
        }
    }

    res = requests.post(api_url, json=payload)

    # ✅ Validate response
    if res.status_code == 200 and "image" in res.headers.get("content-type", ""):
        return res.content

    # ❌ Debug if failed
    st.error(f"Failed: {res.status_code}")
    st.code(res.text[:500])

    return None


# -------------------------------
# 🔹 STREAM LOOP
# -------------------------------
if start:
    for i in range(10):  # simulate frames
        img = get_screenshot(url)

        if img:
            placeholder.image(img, use_container_width=True)
        else:
            break

        time.sleep(2)

    st.success("✅ Done")
