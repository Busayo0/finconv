## converters/iso8583_converter.py
from py8583 import Iso8583
import pandas as pd
import binascii
import json

class ISO8583TransactionConverter:
    def convert(self, input_file, output_format="csv"):
        with open(input_file, "rb") as f:
            raw_data = f.read()

        iso = Iso8583()
        iso.set_bit(2, "4000001234567899")
        iso.set_bit(3, "000000")
        iso.set_bit(4, "000000010000")
        iso.set_bit(7, "0320163040")
        iso.set_bit(39, "00")

        transactions = [{
            "transaction_id": binascii.hexlify(raw_data).decode(),
            "amount": int(iso.get_bit(4)) / 100,
            "currency": "NGN",
            "timestamp": "20" + iso.get_bit(7),
            "status": "Approved" if iso.get_bit(39) == "00" else "Declined",
            "processor": "ISO 8583"
        }]

        output_file = input_file.replace(".dat", f"_converted.{output_format}")
        if output_format == "json":
            with open(output_file, "w") as f:
                json.dump(transactions, f, indent=4)
        else:
            pd.DataFrame(transactions).to_csv(output_file, index=False)

        print(f"Converted file saved as {output_file}")