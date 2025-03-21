## converters/json_converter.py
import json
import pandas as pd
from transaction_templates import TEMPLATES

class JSONTransactionConverter:
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
                "processor": "JSON"
            }
            standardized_data.append(standardized_record)
        return standardized_data

    def convert(self, input_json, output_format="csv"):
        with open(input_json, "r") as f:
            data = json.load(f)

        standardized_data = self.standardize_data(data)

        output_file = input_json.replace(".json", f"_converted.{output_format}")
        if output_format == "csv":
            pd.DataFrame(standardized_data).to_csv(output_file, index=False)
        else:
            with open(output_file, "w") as f:
                json.dump(standardized_data, f, indent=4)

        print(f"Converted file saved as {output_file}")
