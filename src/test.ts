import { ProcessorType, ConverterFactory } from './converters/ConverterFactory';

// Test data
const visaContent = `20230415,123.45,WALMART SUPERCENTER      ,4532123456789012,TXN123456789`;
const mcContent = `MC|15-04-2023|123.45|WALMART SUPERCENTER           |5412345678901234|MC12345678`;

try {
  // Test VISA conversion
  const visaConverter = ConverterFactory.getConverter(ProcessorType.VISA);
  console.log('VISA Transaction:', visaConverter.parse(visaContent));

  // Test Mastercard conversion
  const mcConverter = ConverterFactory.getConverter(ProcessorType.MASTERCARD);
  console.log('Mastercard Transaction:', mcConverter.parse(mcContent));
} catch (error) {
  console.error('Error:', error);
} 