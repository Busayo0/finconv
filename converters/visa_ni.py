import pandas as pd

def parse_visa_ni_file(uploaded_file):
    '''
    Visa NI parser (fully tolerant):
    - Handles inconsistent column counts
    - Masks PAN (column 0)
    - Pads rows to max length
    - Returns:
        - df: parsed DataFrame
        - df_export: exportable version with blank first row
    '''
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    def mask_pan(pan: str) -> str:
        if len(pan) >= 10:
            return pan[:4] + '*' * (len(pan) - 8) + pan[-4:]
        return '*' * len(pan)

    masked_rows = []
    max_cols = 0

    for line in lines:
        if "|" not in line:
            continue
        parts = line.split("|")
        parts[0] = mask_pan(parts[0])
        masked_rows.append(parts)
        max_cols = max(max_cols, len(parts))

    # Pad rows to match max column count
    padded_rows = [row + [""] * (max_cols - len(row)) for row in masked_rows]

    # Create DataFrame
    df = pd.DataFrame(padded_rows)

    # Add blank first row for export
    df_export = pd.concat([pd.DataFrame([[""] * max_cols]), df], ignore_index=True)

    return df, df_export
