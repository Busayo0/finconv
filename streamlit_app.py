import streamlit as st
import requests
import os

API_URL = "http://localhost:8000/api/convert"  # Update if deploying

st.set_page_config(page_title="Financial File Converter", layout="centered")
st.title("📂 Financial File Converter")

st.markdown("Convert financial transaction files (CSV, JSON, XML, ISO 8583) to a standardized format.")

uploaded_file = st.file_uploader("Upload a transaction file", type=["csv", "json", "xml", "dat"])

processor = st.selectbox("Select the Processor Format", ["Visa", "Mastercard"])
output_format = st.selectbox("Choose Output Format", ["csv", "json"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    if st.button("Convert File"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"processor": processor, "output_format": output_format}

            response = requests.post(API_URL, files=files, data=data)

            if response.status_code == 200:
                out_filename = f"converted_{uploaded_file.name.split('.')[0]}.{output_format}"
                st.download_button(
                    label="📥 Download Converted File",
                    data=response.content,
                    file_name=out_filename,
                    mime="application/octet-stream"
                )
            else:
                st.error("Conversion failed. Please check the file or try again.")
else:
    st.info("Please upload a file to begin.")
