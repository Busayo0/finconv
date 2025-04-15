import pandas as pd
import re

def parse_ipm_text_dump(content):
    # Extract message chunks starting with '1240' (MTI)
    matches = re.findall(r'(1240.{200,500})', content)  # crude match, adjust size as needed

    messages = []
    for i, raw_msg in enumerate(matches):
        msg = {
            "Message #": i + 1,
            "MTI": raw_msg[0:4],
            "PAN": raw_msg[4:23].strip(),
            "Processing Code": raw_msg[23:29].strip(),
            "Amount": raw_msg[29:41].strip(),
            "RRN": re.search(r'\d{12}', raw_msg).group() if re.search(r'\d{12}', raw_msg) else None,
            "Merchant": re.search(r'[A-Z\s]{10,40}', raw_msg).group().strip() if re.search(r'[A-Z\s]{10,40}', raw_msg) else None
        }
        messages.append(msg)

    return pd.DataFrame(messages)
