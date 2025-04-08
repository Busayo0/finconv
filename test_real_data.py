from converters import VisaConverter, MastercardConverter

def test_real_visa_data():
    # Real-world VISA transaction data
    visa_data = """20240315,299.99,AMAZON.COM              ,4532123456789012,TXN123456789
20240316,45.50,STARBUCKS COFFEE        ,4532123456789012,TXN987654321
20240317,150.00,WALMART SUPERCENTER    ,4532123456789012,TXN456789123"""
    
    converter = VisaConverter()
    transactions = converter.parse(visa_data)
    
    print("\nReal VISA Transactions:")
    for tx in transactions:
        print(f"Date: {tx['transaction_date'].strftime('%Y-%m-%d')}")
        print(f"Amount: ${tx['amount']:.2f}")
        print(f"Merchant: {tx['merchant_name']}")
        print(f"Card: {tx['card_number'][-4:]}")  # Only show last 4 digits for security
        print(f"Transaction ID: {tx['transaction_id']}")
        print("---")

def test_real_mastercard_data():
    # Real-world Mastercard transaction data
    mc_data = """MC|15-03-2024|299.99|AMAZON.COM                    |5412345678901234|MC12345678
MC|16-03-2024|45.50|STARBUCKS COFFEE              |5412345678901234|MC98765432
MC|17-03-2024|150.00|WALMART SUPERCENTER         |5412345678901234|MC45678912"""
    
    converter = MastercardConverter()
    transactions = converter.parse(mc_data)
    
    print("\nReal Mastercard Transactions:")
    for tx in transactions:
        print(f"Date: {tx['transaction_date'].strftime('%Y-%m-%d')}")
        print(f"Amount: ${tx['amount']:.2f}")
        print(f"Merchant: {tx['merchant_name']}")
        print(f"Card: {tx['card_number'][-4:]}")  # Only show last 4 digits for security
        print(f"Transaction ID: {tx['transaction_id']}")
        print("---")

if __name__ == "__main__":
    test_real_visa_data()
    test_real_mastercard_data() 