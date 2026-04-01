import streamlit as st
from playwright.sync_api import sync_playwright

st.title("Simple Browser Automation")

url = st.text_input("Enter website URL")

if st.button("Run Automation"):
    if url:
        with st.spinner("Running browser..."):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                page.goto(url)
                
                # Example actions (your "xyz job")
                title = page.title()
                content = page.content()
                
                browser.close()

        st.success("Done!")

        st.subheader("Page Title")
        st.write(title)

        st.subheader("HTML Preview")
        st.code(content[:1000])  # first 1000 chars
