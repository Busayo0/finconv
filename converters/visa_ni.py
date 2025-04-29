import pandas as pd

def parse_visa_ni_file(uploaded_file):
    """
    Parse a pipe-delimited Visa NI file, mask PANs (column 0), and return:
    - df: the cleaned DataFrame
    - df_export: the export-ready DataFrame (with blank row, no headers)
    """
    lines = [line.strip() for line in uploaded_file.readlines() if line.strip()]

    def mask_pan(pan: str) -> str:
        return pan[:4] + '*' * (len(pan) - 8) + pan[-4:] if len(pan) >= 10 else '*' * len(pan)

    parsed_rows = []
    for line in lines:
        parts = line.decode("utf-8", errors="ignore").split("|")
        if parts:
            parts[0] = mask_pan(parts[0])
        parsed_rows.append(parts)

    df = pd.DataFrame(parsed_rows)
    df_export = pd.concat([pd.DataFrame([[""] * len(df.columns)]), df], ignore_index=True)

    return df, df_export
