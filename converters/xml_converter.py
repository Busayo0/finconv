## converters/xml_converter.py
import xmltodict
import pandas as pd
import json

class XMLTransactionConverter:
    def convert(self, input_xml, output_format="csv"):
        with open(input_xml, "r") as f:
            data = xmltodict.parse(f.read())

        transactions = []
        for record in data["Document"]["FIToFICustomerCreditTransfer"]["CdtTrfTxInf"]:
            transactions.append({
                "transaction_id": record["PmtId"]["EndToEndId"],
                "amount": float(record["Amt"]["InstdAmt"]["#text"]),
                "currency": record["Amt"]["InstdAmt"]["@Ccy"],
                "timestamp": record["PmtId"]["TxDtTm"],
                "status": "Processed",
                "processor": "ISO 20022"
            })

        output_file = input_xml.replace(".xml", f"_converted.{output_format}")
        if output_format == "json":
            with open(output_file, "w") as f:
                json.dump(transactions, f, indent=4)
        else:
            pd.DataFrame(transactions).to_csv(output_file, index=False)

        print(f"Converted file saved as {output_file}")
