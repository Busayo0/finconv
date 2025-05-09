import pandas as pd

def parse_visa_ni_file(uploaded_file):
    '''
    Visa NI parser:
    ✅ Masks PAN in column 0
    ✅ Strips leading zeros (after trimming) from all other columns
    ✅ Pads ragged rows
    ✅ Returns df and df_export
    '''
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    def mask_pan(pan: str) -> str:
        return pan[:4] + '*' * (len(pan) - 8) + pan[-4:] if len(pan) >= 10 else '*' * len(pan)

    def strip_leading_zeros(val) -> str:
        val = str(val).strip()
        return val.lstrip("0") if val.isdigit() else val

    masked_rows = []
    max_cols = 0

    for line in lines:
        if "|" not in line:
            continue
        parts = line.split("|")
        parts[0] = mask_pan(parts[0])
        masked_rows.append(parts)
        max_cols = max(max_cols, len(parts))

    padded_rows = [row + [""] * (max_cols - len(row)) for row in masked_rows]
    df = pd.DataFrame(padded_rows, dtype=str)

    # ✅ Strip zeros only from col[1:] after trimming
    for col in df.columns[1:]:
        df[col] = df[col].apply(strip_leading_zeros)

    # Add blank row to df_export
    df_export = pd.concat([pd.DataFrame([[""] * max_cols], dtype=str), df], ignore_index=True)

    return df, df_export
