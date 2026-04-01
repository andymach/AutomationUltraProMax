import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🌐 Hybrid Browser Viewer (Best Approach)")

# 🔑 Your Browserless API key
TOKEN = "2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"

# -------------------------------
# 🔹 INPUT
# -------------------------------
url = st.text_input(
    "Enter URL",
    value="https://www.bajajfinserv.in/tnc-b2c-urban"
)

load_btn = st.button("Load Page")

# -------------------------------
# 🔹 FUNCTION: FETCH HTML
# -------------------------------
def fetch_html(target_url):
    try:
        api_url = f"https://production-sfo.browserless.io/unblock?token={TOKEN}"

        payload = {
            "url": target_url,
            "gotoOptions": {
                "waitUntil": "networkidle",
                "timeout": 60000
            }
        }

        res = requests.post(api_url, json=payload)

        if res.status_code == 200:
            return res.text

        st.error(f"❌ Request failed: {res.status_code}")
        st.code(res.text[:500])
        return None

    except Exception as e:
        st.error("🔥 Exception occurred")
        st.code(str(e))
        return None


# -------------------------------
# 🔹 MAIN LOGIC
# -------------------------------
if load_btn:
    if not url:
        st.warning("Please enter a URL")
    else:
        st.info("⏳ Loading via Browserless (unblock mode)...")

        html = fetch_html(url)

        if html:
            st.success("✅ Page loaded")

            # 🔹 Render HTML inside Streamlit
            st.components.v1.html(
                html,
                height=800,
                scrolling=True
            )

        else:
            st.error("❌ Could not load page")
