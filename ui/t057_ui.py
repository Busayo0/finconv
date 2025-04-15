import streamlit as st
import pandas as pd
from converters import parse_t057_fixed_width, parse_iso8583_xml, decode_field_48

# ---------------- Binary Fallback -------------------
def parse_binary_file(uploaded_file):
    binary_data = uploaded_file.read()
    return pd.DataFrame([{
        "Hex Dump": binary_data.hex(),
        "Size (bytes)": len(binary_data)
    }])

# ---------------- Streamlit App -------------------
st.set_page_config(page_title="File Format Analyzer", layout="centered")
st.title("📁 File Format Analyzer")

uploaded_file = st.file_uploader("Upload a file (.xml, .dat, .bin, .001)", type=["xml", "dat", "bin", "001", "txt"])

if uploaded_file:
    filename = uploaded_file.name.lower()
    try:
        if filename.endswith(".xml"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            df = parse_iso8583_xml(content)

            st.success("✅ ISO 8583 fields extracted successfully")
            st.dataframe(df)

            for msg_id in df["Message #"].unique():
                field_48_row = df[(df["Message #"] == msg_id) & (df["Field ID"] == "48")]
                if not field_48_row.empty:
                    st.subheader(f"🔍 Decoded Field 48 (Message #{msg_id})")
                    decoded = decode_field_48(field_48_row.iloc[0]["Value"])
                    st.dataframe(pd.DataFrame(decoded))

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, file_name="iso8583_fields.csv", mime="text/csv")

        elif filename.endswith(".001") or filename.startswith("t057"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = content.splitlines()
            df = parse_t057_fixed_width(lines)

            st.success("✅ T057 file parsed successfully")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, file_name="t057_parsed.csv", mime="text/csv")

        else:
            st.subheader("📦 Binary File Summary")
            df_bin = parse_binary_file(uploaded_file)
            st.dataframe(df_bin)

    except Exception as e:
        st.error(f"An error occurred while parsing the file: {e}")

