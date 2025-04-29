
import streamlit as st
import pandas as pd
from converters.t057 import parse_t057_fixed_width
from converters.iso8583 import parse_iso8583_xml, decode_field_48
from converters.t113 import parse_t113_fixed_width
from converters.ipm import parse_ipm_text_dump
from converters.visa_ni import parse_visa_ni_file

# ---------------- Binary Fallback -------------------
def parse_binary_file(uploaded_file):
    binary_data = uploaded_file.read()
    return pd.DataFrame([{
        "Hex Dump": binary_data.hex(),
        "Size (bytes)": len(binary_data)
    }])

# ---------------- ISO Field Name Mapper -------------------
def get_iso_field_name(field_id):
    iso_field_names = {
        "0": "MTI", "1": "Bitmap", "2": "Primary Account Number", "3": "Processing Code",
        "4": "Transaction Amount", "5": "Settlement Amount", "6": "Cardholder Billing Amount",
        "7": "Transmission Date and Time", "8": "Cardholder Fee", "9": "Settlement Conversion Rate",
        "10": "Cardholder Billing Conversion Rate", "11": "STAN", "12": "Local Time",
        "13": "Local Date", "14": "Expiration Date", "15": "Settlement Date",
        "18": "Merchant Category Code", "22": "POS Entry Mode", "23": "Card Sequence Number",
        "24": "Function Code", "25": "POS Condition Code", "26": "POS Capture Code",
        "28": "Amount, Transaction Fee", "30": "Amount, Processing Fee", "31": "Acquirer Reference Data",
        "32": "Acquiring Institution ID", "33": "Forwarding Institution ID", "35": "Track 2 Data",
        "37": "Retrieval Reference Number", "38": "Authorization ID", "39": "Response Code",
        "41": "Terminal ID", "42": "Merchant ID", "43": "Card Acceptor Name/Location",
        "44": "Additional Response Data", "48": "Additional Data", "49": "Transaction Currency Code",
        "52": "PIN Data", "54": "Additional Amounts", "55": "EMV Data", "56": "Reserved ISO",
        "59": "E-commerce Indicator", "60": "Advice Reason Code", "61": "POS Data",
        "63": "Private Reserved", "70": "Network Management Information Code", "71": "Message Number",
        "72": "Data Record", "73": "Date Action", "90": "Original Data Elements",
        "94": "Replacement Amounts or Response Indicator", "95": "Replacement Amounts",
        "100": "Receiving Institution ID", "102": "Account Identification 1",
        "103": "Account Identification 2"
    }
    return iso_field_names.get(field_id, f"Field {field_id}")

# ---------------- Streamlit App -------------------
st.set_page_config(page_title="File Format Analyzer", layout="centered")
st.title("📁 File Format Analyzer")

uploaded_file = st.file_uploader("Upload a file (.xml, .dat, .bin, .001, .txt)", type=["xml", "dat", "bin", "001", "txt"])

if uploaded_file:
    filename = uploaded_file.name.lower()
    try:
        # ISO 8583
        if filename.endswith(".xml"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            df = parse_iso8583_xml(content)

            if "Field ID" not in df.columns or "Value" not in df.columns:
                st.error("❌ File does not contain expected ISO 8583 fields.")
            else:
                df["Field Name"] = df["Field ID"].apply(get_iso_field_name)
                df = df[["Message #", "Field Name", "Value"]]
                df_pivot = df.pivot(index="Message #", columns="Field Name", values="Value").reset_index()

                st.success("✅ ISO 8583 fields extracted successfully")
                st.dataframe(df_pivot)

                if "Additional Data" in df_pivot.columns:
                    for i, row in df_pivot.iterrows():
                        if pd.notna(row.get("Additional Data")):
                            st.subheader(f"🔍 Decoded Field 48 (Message #{row['Message #']})")
                            decoded = decode_field_48(row["Additional Data"])
                            st.dataframe(pd.DataFrame(decoded))

                csv = df_pivot.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download CSV", csv, file_name="iso8583_fields.csv", mime="text/csv")

        # T057
        elif filename.endswith(".001") or filename.startswith("t057"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = content.splitlines()
            df = parse_t057_fixed_width(lines)

            st.success("✅ T057 file parsed successfully")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, file_name="t057_parsed.csv", mime="text/csv")

        # T113
        elif "t113" in filename:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = content.splitlines()
            df = parse_t113_fixed_width(lines)

            st.success("✅ T113 acknowledgment file parsed successfully")
            st.dataframe(df)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), "t113_parsed.csv")

        # IPM
        elif "ipm" in filename and filename.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            df = parse_ipm_text_dump(content)

            st.success("✅ IPM message dump parsed successfully")
            st.dataframe(df)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), "ipm_parsed.csv")

        # Visa NI / KUDA
        elif "kuda" in filename or "visa" in filename:
            df, df_export = parse_visa_ni_file(uploaded_file)

            st.success("✅ Visa NI file parsed successfully (PANs masked)")
            st.dataframe(df_export)

            st.download_button("⬇️ Export CSV", df_export.to_csv(index=False, header=False).encode("utf-8"), "visa_ni.csv", mime="text/csv")
            st.download_button("⬇️ Export JSON", df_export.to_json(orient="records"), "visa_ni.json", mime="application/json")

            st.subheader("📊 Transaction Summary")
            category_map = {
                "05": "POS", "06": "Merchant Refunds", "07": "ATM",
                "25": "POS Reversal", "27": "ATM Reversal",
                "CradJ": "Credit Adjustment", "TFee": "Transaction Fee"
            }

            df[5] = df[5].str.strip()
            df[10] = pd.to_numeric(df[10], errors="coerce") / 100

            summary = []
            for key, label in category_map.items():
                matched = df[df[5] == key]
                count = len(matched)
                total = matched[10].sum()
                summary.append({"Transaction Type": label, "Count": count, "Total Amount": total})

            df_summary = pd.DataFrame(summary)

            cols = st.columns(len(df_summary))
            for i, row in enumerate(df_summary.itertuples()):
                with cols[i]:
                    st.metric(label=row._1, value=f"₦{row._3:,.2f}", delta=f"{row._2} txns")

            st.dataframe(df_summary)

        # Fallback
        else:
            st.subheader("📦 Binary File Summary")
            df_bin = parse_binary_file(uploaded_file)
            st.dataframe(df_bin)

    except Exception as e:
        st.error(f"❌ An error occurred while parsing the file: {e}")
