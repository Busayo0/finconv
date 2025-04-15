import pandas as pd

def parse_t113_fixed_width(lines):
    parsed_data = []
    for line in lines:
        if not line.strip().startswith("D"):  # Adjust if there's a header marker
            continue
        record = {
            "RecordType": line[0],
            "MessageID": line[1:13].strip(),
            "AckCode": line[13:15].strip(),
            "Timestamp": line[15:27].strip(),
            "Originator": line[27:47].strip(),
            "Receiver": line[47:67].strip(),
            "StatusFlag": line[67:77].strip()
        }
        parsed_data.append(record)

    return pd.DataFrame(parsed_data)
