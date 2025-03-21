## converters/csv_converter.py
import pandas as pd
import json
from transaction_templates import TEMPLATES

class CSVTransactionConverter:
    def __init__(self, processor):
        if processor not in TEMPLATES:
            raise ValueError(f"Unsupported processor: {processor}")
        self.mapping = TEMPLATES[processor]

    def standardize_data(self, data):
        standardized_data = []
        for record in data:
            standardized_record = {
                "transaction_id": record.get(self.mapping["txn_id"], ""),
                "amount": float(record.get(self.mapping["amount"], 0)),
                "currency": record.get(self.mapping["currency"], ""),
                "timestamp": record.get(self.mapping["timestamp"], ""),
                "status": record.get(self.mapping["status"], ""),
                "processor": "CSV"
            }
            standardized_data.append(standardized_record)
        return standardized_data

    def convert(self, input_csv, output_format="json"):
        df = pd.read_csv(input_csv)
        data = df.to_dict(orient="records")
        standardized_data = self.standardize_data(data)

        output_file = input_csv.replace(".csv", f"_converted.{output_format}")
        if output_format == "json":
            with open(output_file, "w") as f:
                json.dump(standardized_data, f, indent=4)
        else:
            pd.DataFrame(standardized_data).to_csv(output_file, index=False)

        print(f"Converted file saved as {output_file}")