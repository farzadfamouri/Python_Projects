from pdf2image import convert_from_path
import pytesseract
import re
import os
import glob

# Initialize Tesseract OCR

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Folder containing the PDFs

folder_path = 'C:/Users/farza/OneDrive/Desktop/AIML/\
Associate Data Scientist In Python/Python_Projects_DataCamp/pythonProject1/'

# Get a list of all PDF files starting with "Remote Desktop Redirected Printer Doc"

pdf_files = glob.glob(os.path.join(folder_path, "Remote Desktop Redirected Printer Doc*.pdf"))

# Process each file
for pdf_path in pdf_files:

    print(f"Processing file: {pdf_path}")

    images = convert_from_path(pdf_path)

    valid_name = False  # Track if a valid name is found

    for page_num, image in enumerate(images, start=1):

        text = pytesseract.image_to_string(image)

        with open(f"{os.path.splitext(pdf_path)[0]}_ocr_debug.txt", "w") as debug_file:

            debug_file.write(text)  # Save OCR output for debugging

        # Improved pattern for Piece #

        match = re.search(r'Piece\s+#\s+([A-Za-z0-9._\-]+)', text, re.IGNORECASE)

        if match:

            new_name = match.group(1).strip()

            if "Batch" in new_name or len(new_name) < 5:  # Sanity check

                print(f"Invalid name detected: {new_name}, skipping...")

                continue

            # Avoid duplicates

            new_pdf_name = os.path.join(folder_path, f"{new_name}.pdf")

            counter = 1

            while os.path.exists(new_pdf_name):
                new_pdf_name = os.path.join(folder_path, f"{new_name}_{counter}.pdf")

                counter += 1

            os.rename(pdf_path, new_pdf_name)

            print(f"PDF renamed to: {new_pdf_name}")

            valid_name = True

            break

    if not valid_name:
        print(f"No valid name found for file: {pdf_path}")