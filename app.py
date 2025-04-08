from flask import Flask, render_template, request, jsonify
from converters import VisaConverter, MastercardConverter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    file_content = data.get('content', '')
    file_type = data.get('type', '')
    
    try:
        if file_type == 'visa':
            converter = VisaConverter()
        elif file_type == 'mastercard':
            converter = MastercardConverter()
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
        transactions = converter.parse(file_content)
        
        # Format transactions for display
        formatted_transactions = []
        for tx in transactions:
            formatted_transactions.append({
                'date': tx['transaction_date'].strftime('%Y-%m-%d'),
                'amount': f"${tx['amount']:.2f}",
                'merchant': tx['merchant_name'],
                'card': tx['card_number'][-4:],  # Only show last 4 digits
                'transaction_id': tx['transaction_id']
            })
            
        return jsonify({'transactions': formatted_transactions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 