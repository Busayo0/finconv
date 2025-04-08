import { FileConverter } from './FileConverter';
import { VisaConverter } from './VisaConverter';
import { MastercardConverter } from './MastercardConverter';

export enum ProcessorType {
  VISA = 'VISA',
  MASTERCARD = 'MASTERCARD'
}

export class ConverterFactory {
  static getConverter(type: ProcessorType): FileConverter {
    switch (type) {
      case ProcessorType.VISA:
        return new VisaConverter();
      case ProcessorType.MASTERCARD:
        return new MastercardConverter();
      default:
        throw new Error(`Unsupported processor type: ${type}`);
    }
  }
} 