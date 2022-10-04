# Text Normalizer

This project implements text normalization for Farsi(Persian) language in the traditional way.  

  
it contains types below :
* normalizing numbers 
* normalizing dates
* normalizing times
* normalizing currency
* normalizing measurement (physical measurement)
* normalizing phone number and ID number
* normalizing punctuation
* normalizing miscellaneous abbreviations

for text-to-speech and speech-to-text (TTSv1(default) , TTSv2, STT).

## Usage  

```bash
python main.py [input file address] [output file address] [version] [type1, type2, ....]
```
### examples
normalize all types for text-to-speech version 1
```bash
python main.py inp.txt out.txt 
```
normalize time and date for speech-to-text
```bash       
python main.py inp.txt out.txt TTSv2 -t -d
```  

  
1. by declaring a type the normalizer Limited to the declared type !  
2. The difference between TTS version 1 and TTS version 2 is in the way the punctuations are normalized  



