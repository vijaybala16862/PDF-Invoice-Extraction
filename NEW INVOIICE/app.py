from flask import Flask, request, render_template, redirect, url_for, flash
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import json
import pyodbc

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load environment variables
load_dotenv()

# Google Gemini API setup
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# SQL Server Connection
def get_db_connection():
    try:
        return pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=VIJAYBALA\\SQLEXPRESS01;"
            "DATABASE=Overall Invoice;"
            "Trusted_Connection=yes;"
        )
    except Exception as e:
        print("DB error:", e)
        return None

# PDF to text extraction
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    print("Extracted Text:\n", text)

    return text

# Gemini AI extraction with all required fields
def extract_invoice_data_with_gemini(text):
    prompt = f"""
You are an intelligent invoice extraction assistant.

Extract the following fields from the raw invoice text. The layout may vary. Use context to identify fields.

Always output only clean JSON.

Extract:
- Shipper Name
- Billing Customer Name
- Consignee
- Invoice Number
- Invoice Date (DD.MM.YYYY)
- Buyers Order No
- IE CODE
- GSTIN
- Port of Loading
- Port of Discharge and Final Destination
- Notify Party
- Mode of Delivery
- Terms
- Container No (Packages)
- Style No
- Total Amount
- Total Net Weight (KGs) → If the text contains 'Net Weight' or 'Total Net Weight', extract the number with units as Net Weight.
- Total Gross Weight (KGs) → If the text contains 'Gross Weight', 'Total Gross Weight', or 'Gross Wt', extract the number with units as Gross Weight.
- Total CBM
- Product Table: description, quantity, rate, amount as an array of objects

If a field is missing, leave its value as empty string. Do not generate random information.

Example JSON:

{{
  "Shipper_Name": "ABC Exports",
  "Billing_Customer_Name": "ABC Exports",
  "Consignee": "XYZ Pvt Ltd",
  "Invoice_No": "INV/123/2025",
  "Invoice_Date": "29.04.2025",
  "Buyers_Order_No": "PO123456",
  "IE_CODE": "3293012124",
  "GSTIN": "33AAEFA9584D1ZI",
  "Port_Loading": "Chennai",
  "Port_Discharge_Final": "Sydney/Australia",
  "Notify_Party": "Toll Global",
  "Mode_of_Delivery": "FOB by Sea",
  "Terms": "TT Payment",
  "Container_No": "20 CARTONS",
  "Style_No": "CE02202E",
  "Total_Amount": "1818.00",
  "Total_Net_Wt": "85.000",
  "Total_Grs_Wt": "109.000",
  "Total_CBM": "1.44",
  "Products": [
    {{"description": "Garment", "quantity": "360", "rate": "1.95", "amount": "702.00"}}
  ]
}}

Text:
{text}
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text

# Index Route
@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = {}
    if request.method == "POST":
        pdf_file = request.files.get("pdf")
        if pdf_file:
            pdf_path = "uploaded_invoice.pdf"
            pdf_file.save(pdf_path)

            text = extract_text_from_pdf(pdf_path)
            ai_response = extract_invoice_data_with_gemini(text)

            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                try:
                    extracted_data = json.loads(json_match.group())
                    flash("Extraction successful!", "success")
                except json.JSONDecodeError:
                    extracted_data = {"raw_response": ai_response}
                    flash("AI responded, but JSON format invalid.", "danger")
            else:
                extracted_data = {"raw_response": ai_response}
                flash("AI responded, but no JSON detected.", "danger")

    return render_template("index.html", data=extracted_data)

# Save Route
@app.route("/save", methods=["POST"])
def save():
    descriptions = request.form.getlist('description[]')
    quantities = request.form.getlist('quantity[]')
    rates = request.form.getlist('rate[]')
    amounts = request.form.getlist('amount[]')

    products = []
    for i in range(len(descriptions)):
        products.append({
            "description": descriptions[i],
            "quantity": quantities[i],
            "rate": rates[i],
            "amount": amounts[i]
        })

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Duplicate Check
        cursor.execute("SELECT COUNT(*) FROM TABLEINVOICE WHERE Invoice_No = ? AND Invoice_Date = ?", (
            request.form.get("Invoice_No"),
            request.form.get("Invoice_Date")
        ))
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            flash("Duplicate Invoice! This Invoice No and Date already exists.", "danger")
            return redirect(url_for("index"))

        # Insert Invoice
        params = (
            request.form.get("Shipper_Name"),
            request.form.get("Billing_Customer_Name"),
            request.form.get("Consignee"),
            request.form.get("Invoice_No"),
            request.form.get("Invoice_Date"),
            request.form.get("Buyers_Order_No"),
            request.form.get("IE_CODE"),
            request.form.get("GSTIN"),
            request.form.get("Port_Loading"),
            request.form.get("Port_Discharge_Final"),
            request.form.get("Notify_Party"),
            request.form.get("Mode_of_Delivery"),
            request.form.get("Terms"),
            request.form.get("Container_No"),
            request.form.get("Style_No"),
            request.form.get("Total_Amount"),
            request.form.get("Total_Net_Wt"),
            request.form.get("Total_Grs_Wt"),
            request.form.get("Total_CBM")
        )

        cursor.execute("{CALL InsertInvoiceData (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)}", params)

        for product in products:
            cursor.execute("{CALL InsertProductDetails (?,?,?,?)}", (
                product["description"],
                product["quantity"],
                product["rate"],
                product["amount"]
            ))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Data saved to database!", "success")

    except Exception as e:
        print("Database Error:", e)
        flash("Database error occurred!", "danger")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
