import streamlit as st
import requests
import base64

st.set_page_config(layout="wide")
st.title("🌐 Stealth Browser (BrowserQL)")

TOKEN = "2UG0iMlUmoTajm29c75d6592cf197f95ae42f88972d3c03a5"

url = st.text_input(
    "Enter URL",
    value="https://www.bajajfinserv.in/tnc-b2c-urban"
)

if st.button("Run"):
    api_url = f"https://production-sfo.browserless.io/stealth/bql?token={TOKEN}&proxy=residential&blockConsentModals=true"

    query = f"""
    mutation NewTab {{
      viewport(width: 1366, height: 768) {{
        width
        height
      }}
      goto(url: "{url}", waitUntil: networkIdle) {{
        status
      }}
      screenshot(fullPage: false) {{
        base64
      }}
    }}
    """

    payload = {
        "query": query,
        "variables": {},
        "operationName": "NewTab"
    }

    res = requests.post(api_url, json=payload)

    if res.status_code == 200:
        data = res.json()

        try:
            img_base64 = data["data"]["screenshot"]["base64"]
            img_bytes = base64.b64decode(img_base64)

            st.success("✅ Page loaded via stealth")
            st.image(img_bytes, use_container_width=True)

        except Exception as e:
            st.error("❌ Could not extract screenshot")
            st.code(str(data))

    else:
        st.error(f"❌ Request failed: {res.status_code}")
        st.code(res.text)
