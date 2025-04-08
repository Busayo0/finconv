export interface FileConverter {
  parse(fileContent: string): TransactionRecord[];
  validate(fileContent: string): boolean;
}

export interface TransactionRecord {
  transactionDate: Date;
  amount: number;
  merchantName: string;
  cardNumber: string;
  transactionId: string;
  // Add more fields as needed
} 