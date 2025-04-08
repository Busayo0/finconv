import pandas as pd
import sys
import os


def parse_t057_fixed_width(lines):
    """
    Parse T057 fixed-width currency/fee band file into a structured DataFrame.
    """
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

    # Convert to numeric and scale appropriately
    for col in ["OpeningRate", "MiddayRate", "ClosingRate", "AverageRate", "StandardRate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce") / 100000

    return df


def parse_t057_file(file_path):
    """
    Reads a T057 file from disk and returns a parsed DataFrame.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return parse_t057_fixed_width(lines)


def export_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


def export_to_json(df, output_path):
    df.to_json(output_path, orient="records", indent=2)


# Example Usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python t057.py <path_to_T057_file>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)

    df = parse_t057_file(input_path)

    # Save output next to input file
    base_name = os.path.splitext(input_path)[0]
    export_to_csv(df, base_name + ".csv")
    export_to_json(df, base_name + ".json")

    print(f"Converted successfully to {base_name}.csv and {base_name}.json")
