import streamlit as st
import pandas as pd
import os
from io import StringIO, BytesIO

def parse_t057_fixed_width(lines):
    parsed_data = []
    for line in lines:
        if not line.startswith("D"):
            continue
        record = {
            "RecordCode": line[0],
            "LocationCode": line[1:9],
            "RateType": line[9:11],
            "OpeningRate": line[11:24],
            "MiddayRate": line[24:37],
            "ClosingRate": line[37:50],
            "AverageRate": line[50:63],
            "StandardRate": line[63:76],
            "ChecksumOrFiller": line[76:].strip()
        }
        parsed_data.append(record)

    df = pd.DataFrame(parsed_data)
    for col in ["OpeningRate", "MiddayRate", "ClosingRate", "AverageRate", "StandardRate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce") / 100000
    return df

st.set_page_config(page_title="T057 File Converter", layout="centered")
st.title("📄 T057 File Converter")

uploaded_file = st.file_uploader("Upload a .T057 or .001 file", type=["001", "txt"])

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        lines = content.splitlines()
        df = parse_t057_fixed_width(lines)

        st.success("File parsed successfully!")
        st.dataframe(df)

        # Download buttons
        csv = df.to_csv(index=False).encode("utf-8")
        json = df.to_json(orient="records", indent=2).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="t057_converted.csv",
            mime="text/csv"
        )
        st.download_button(
            label="⬇️ Download JSON",
            data=json,
            file_name="t057_converted.json",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
