import { FileConverter, TransactionRecord } from './FileConverter';

export class VisaConverter implements FileConverter {
  private readonly VISA_LINE_REGEX = /^(\d{8}),(\d+\.\d{2}),(.{25}),(\d{16}),(\w{12})$/;

  validate(fileContent: string): boolean {
    const lines = fileContent.split('\n');
    return lines.every(line => this.VISA_LINE_REGEX.test(line.trim()));
  }

  parse(fileContent: string): TransactionRecord[] {
    if (!this.validate(fileContent)) {
      throw new Error('Invalid VISA file format');
    }

    const lines = fileContent.split('\n');
    return lines.map(line => {
      const [date, amount, merchant, card, txId] = line.trim().split(',');
      
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
    // Assuming date format is YYYYMMDD
    const year = parseInt(dateStr.substring(0, 4));
    const month = parseInt(dateStr.substring(4, 6)) - 1;
    const day = parseInt(dateStr.substring(6, 8));
    return new Date(year, month, day);
  }
} 