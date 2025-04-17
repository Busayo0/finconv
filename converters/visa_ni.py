import pandas as pd

def parse_visa_ni_file(uploaded_file):
    """
    Parse a Visa NI pipe-delimited file, mask the PANs (column 0), 
    and return a DataFrame with a blank first row and no headers.
    """
    # Read and clean each line
    lines = [line.strip() for line in uploaded_file.readlines() if line.strip()]

    def mask_pan(pan: str) -> str:
        """Mask PAN to show only first 4 and last 4 digits."""
        return pan[:4] + '*' * (len(pan) - 8) + pan[-4:] if len(pan) >= 10 else '*' * len(pan)

    parsed_rows = []
    for line in lines:
        parts = line.decode("utf-8", errors="ignore").split("|")
        if parts:
            parts[0] = mask_pan(parts[0])
        parsed_rows.append(parts)

    df = pd.DataFrame(parsed_rows)

    # Add a blank first row
    blank_row = pd.DataFrame([[""] * len(df.columns)])
    df_export = pd.concat([blank_row, df], ignore_index=True)

    return df_export
