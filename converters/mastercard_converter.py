from datetime import datetime
import re

class MastercardConverter:
    def __init__(self):
        # Updated pattern to be more flexible with whitespace
        self.line_pattern = re.compile(r'^MC\|(\d{2}-\d{2}-\d{4})\|(\d+\.\d{2})\|(.+?)\|(\d{16})\|(\w{10})$')

    def parse(self, file_content: str) -> list:
        transactions = []
        for line in file_content.strip().split('\n'):
            match = self.line_pattern.match(line.strip())
            if not match:
                raise ValueError(f"Invalid Mastercard format: {line}")
            
            date_str, amount, merchant, card, tx_id = match.groups()
            
            # Parse date (DD-MM-YYYY format)
            date = datetime.strptime(date_str, '%d-%m-%Y')
            
            transactions.append({
                'transaction_date': date,
                'amount': float(amount),
                'merchant_name': merchant.strip(),
                'card_number': card,
                'transaction_id': tx_id
            })
        
        return transactions 