import streamlit as st
import requests
import time
import base64

st.set_page_config(layout="wide")
st.title("🌐 Browser Streaming (via Browserless API)")

TOKEN = "2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"

url = st.text_input("Enter URL", value="https://www.bajajfinserv.in/tnc-b2c-urban")

start = st.button("Start Streaming")

placeholder = st.empty()

def get_screenshot(scroll_y=0):
    api_url = f"https://production-sfo.browserless.io/screenshot?token={TOKEN}"

    payload = {
        "url": url,
        "options": {
            "fullPage": False
        },
        "gotoOptions": {
            "waitUntil": "domcontentloaded",
            "timeout": 60000
        },
        "viewport": {
            "width": 1280,
            "height": 800
        },
        "scripts": [
            f"window.scrollTo(0, {scroll_y})"
        ]
    }

    res = requests.post(api_url, json=payload)

    return res.content


if start:
    scroll = 0

    while True:
        try:
            img = get_screenshot(scroll)

            placeholder.image(img, use_container_width=True)

            scroll += 400  # scroll step
            time.sleep(1)

        except Exception as e:
            st.error(str(e))
            break
