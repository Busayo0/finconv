from converters import VisaConverter, MastercardConverter

def test_visa_converter():
    # Test VISA format data
    visa_data = """20230415,123.45,WALMART SUPERCENTER      ,4532123456789012,TXN123456789
20230416,67.89,TARGET STORES           ,4532123456789012,TXN987654321"""
    
    converter = VisaConverter()
    transactions = converter.parse(visa_data)
    
    print("\nVISA Transactions:")
    for tx in transactions:
        print(f"Date: {tx['transaction_date']}")
        print(f"Amount: ${tx['amount']}")
        print(f"Merchant: {tx['merchant_name']}")
        print(f"Card: {tx['card_number']}")
        print(f"Transaction ID: {tx['transaction_id']}")
        print("---")

def test_mastercard_converter():
    # Test Mastercard format data
    mc_data = """MC|15-04-2023|123.45|WALMART SUPERCENTER           |5412345678901234|MC12345678
MC|16-04-2023|67.89|TARGET STORES                |5412345678901234|MC98765432"""
    
    converter = MastercardConverter()
    transactions = converter.parse(mc_data)
    
    print("\nMastercard Transactions:")
    for tx in transactions:
        print(f"Date: {tx['transaction_date']}")
        print(f"Amount: ${tx['amount']}")
        print(f"Merchant: {tx['merchant_name']}")
        print(f"Card: {tx['card_number']}")
        print(f"Transaction ID: {tx['transaction_id']}")
        print("---")

if __name__ == "__main__":
    test_visa_converter()
    test_mastercard_converter() 