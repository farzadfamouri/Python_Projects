from pdf2image import convert_from_path
import pytesseract
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to your PDF file

pdf_path = 'C:/Users/farza/OneDrive/Desktop/AIML/\
Associate Data Scientist In Python/Python_Projects_DataCamp/pythonProject1/Remote Desktop Redirected Printer Doc.pdf'

# Convert PDF to images

images = convert_from_path(pdf_path)

# Initialize Tesseract OCR

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Adjust based \
# on your Tesseract installation path

# Process the first image of the PDF (assuming the required info is on the first page)

for page_num, image in enumerate(images, start=1):

    text = pytesseract.image_to_string(image)

    print(f"Page {page_num} Text:\n{text}\n")

    # Look for the pattern in the extracted text

    match = re.search(r'Piece #\s*([A-Za-z0-9\-]+)', text)

    if match:
        new_name = match.group(1).strip()
        print(f"Found Item Name: {new_name}")

        # Rename the PDF
        new_pdf_name = f"{new_name}.pdf"
        os.rename(pdf_path, new_pdf_name)
        print(f"PDF renamed to: {new_pdf_name}")
        break

else:

    print("Item name not found in the PDF.")