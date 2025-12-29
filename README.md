# PDF-Invoice-Extraction

## Overview
PDF-Invoice-Extraction is a Python-based project for automatically extracting structured data from PDF invoices. It reads invoice PDFs (including scanned or image-based invoices), extracts relevant header and tabular fields (like invoice number, date, exporter/importer details, item lines, quantities, amounts, weights, etc.), and outputs the cleaned data suitable for further processing or storage (e.g. saving into a database).

## Key Goals
- Automate extraction of invoice metadata (invoice number, date, exporter/consignee, order number, etc.)  
- Extract detailed line-item data: product/style, quantity, unit price/rate, amount, weights (net, gross), CBM if present  
- Handle both text-based and scanned PDF invoices (via OCR when needed)  
- Output data in structured format (e.g. JSON, CSV, or direct database insertion)  

## Features
- PDF processing using reliable libraries (e.g. PyMuPDF, pdfplumber, or others)  
- Optional OCR support for scanned PDFs (e.g. via Tesseract)  
- Accurate field extraction using regex / parsing logic / AI-assisted extraction (if configured)  
- Tabular data extraction for product line-items  
- Flexibility to map fields according to your schema (exporter name & address, invoice no/date, container no, weights, etc.)  
- Extensible — easy to adapt for new invoice layouts or custom fields  

## Prerequisites
- Python 3.8 or higher  
- pip (Python package manager)  
- If OCR support is needed: Tesseract OCR installed on system + relevant language packs  
- (Optional) A relational database or storage mechanism if you plan to save extracted data  

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/vijaybala16862/PDF-Invoice-Extraction.git
cd PDF-Invoice-Extraction

# (Optional) create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # On Linux / macOS
# venv\Scripts\activate          # On Windows

# Install dependencies
pip install -r requirements.txt

#OCR is used, ensure Tesseract is installed.
sudo apt-get update
sudo apt-get install tesseract-ocr

# Example command to process a single invoice
python app.py --input path/to/invoice.pdf --output output/data.json

# Or to process all invoices in a directory
python app.py --input path/to/invoices_folder/ --output output/
