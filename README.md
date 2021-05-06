# ing-pdf-to-csv.py
Transforms a ING DIBA pdf (Kontoauszug) into a CSV file.
Import works fine with [MoneyMoney](https://moneymoney-app.com/)

# Installation
## MacOS

```bash
brew install pdftotext python3
python3 ing-pdf-to-csv.py *.pdf
```

## Windows
Please install pdftotext and add it to your PATH.

# Limitation
Uses only the first two lines of every transaction.

