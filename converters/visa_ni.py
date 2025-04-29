import pandas as pd
from io import StringIO

def parse_visa_ni_file(uploaded_file):
    '''
    Optimized Visa NI parser:
    - Reads and decodes file fast
    - Masks PAN (column 0)
    - Returns:
        - df: clean working DataFrame
        - df_export: version with blank row, no headers
    '''
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    def mask_pan(pan: str) -> str:
        if len(pan) >= 10:
            return pan[:4] + '*' * (len(pan) - 8) + pan[-4:]
        return '*' * len(pan)

    # Inline transformation
    masked_lines = []
    for line in lines:
        if "|" not in line:
            continue
        parts = line.split("|", maxsplit=15)
        parts[0] = mask_pan(parts[0])
        masked_lines.append("|".join(parts))

    # Load to DataFrame via StringIO
    buffer = StringIO("\n".join(masked_lines))
    df = pd.read_csv(buffer, sep="|", header=None, dtype=str)

    # Add blank row for export version
    df_export = pd.concat([pd.DataFrame([[""] * df.shape[1]]), df], ignore_index=True)

    return df,
