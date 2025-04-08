import { FileConverter, TransactionRecord } from './FileConverter';

export class MastercardConverter implements FileConverter {
  private readonly MC_LINE_REGEX = /^MC\|(\d{2}-\d{2}-\d{4})\|(\d+\.\d{2})\|(.{30})\|(\d{16})\|(\w{10})$/;

  validate(fileContent: string): boolean {
    const lines = fileContent.split('\n');
    return lines.every(line => this.MC_LINE_REGEX.test(line.trim()));
  }

  parse(fileContent: string): TransactionRecord[] {
    if (!this.validate(fileContent)) {
      throw new Error('Invalid Mastercard file format');
    }

    const lines = fileContent.split('\n');
    return lines.map(line => {
      const [_, date, amount, merchant, card, txId] = line.trim().match(this.MC_LINE_REGEX) || [];
      
      return {
        transactionDate: this.parseDate(date),
        amount: parseFloat(amount),
        merchantName: merchant.trim(),
        cardNumber: card,
        transactionId: txId
      };
    });
  }

  private parseDate(dateStr: string): Date {
    // Assuming date format is DD-MM-YYYY
    const [day, month, year] = dateStr.split('-').map(num => parseInt(num));
    return new Date(year, month - 1, day);
  }
} 