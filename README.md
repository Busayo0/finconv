# Transaction File Converter

A web application for converting transaction files between different formats (VISA, Mastercard, and ISO 8583).

## Features

- Convert VISA transaction files
- Convert Mastercard transaction files
- Convert ISO 8583 transaction files
- Web interface for easy conversion
- Example data for each format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/transaction-file-converter.git
cd transaction-file-converter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Select the file type and paste your transaction data
4. Click "Convert" to see the results

## Supported Formats

### VISA Format
```
YYYYMMDD,AMOUNT,MERCHANT_NAME,CARD_NUMBER,TRANSACTION_ID
```

### Mastercard Format
```
MC|DD-MM-YYYY|AMOUNT|MERCHANT_NAME|CARD_NUMBER|TRANSACTION_ID
```

### ISO 8583 Format
```
[ISO message format]
```

## License

MIT License