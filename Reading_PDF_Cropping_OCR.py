from pdf2image import convert_from_path
import pytesseract
import re
import os
import glob

# Set the Tesseract OCR executable path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Folder containing the PDFs

folder_path = 'C:/Users/farza/OneDrive/Desktop/AIML/Associate Data Scientist In Python/Python_Projects_DataCamp/pythonProject1/'

pdf_files = glob.glob(os.path.join(folder_path, "Remote Desktop Redirected Printer Doc*.pdf"))

# Define the cropping coordinates (x1, y1, x2, y2) based on Piece # box position

# Adjust these values according to your template

crop_box = (2108, 392, 2187, 1209)  # Example coordinates (adjust as needed)

for pdf_path in pdf_files:

    print(f"Processing file: {pdf_path}")

    images = convert_from_path(pdf_path, dpi=300)  # Convert PDF to high-quality images

    valid_name = False  # Track if a valid name is found

    for page_num, image in enumerate(images, start=1):

        # Crop the region containing the Piece # value

        cropped_image = image.crop(crop_box)

        #cropped_image.save(f"{os.path.splitext(pdf_path)[0]}_cropped_page_{page_num}.png")  # Save for debugging

        # Perform OCR on the cropped region

        text = pytesseract.image_to_string(cropped_image)

        print(f"OCR Output for Cropped Region (Page {page_num}): {text}")

        # Extract the desired name using regex

        match = re.search(r'([A-Za-z0-9._\-]+)', text)  # Adjust pattern as needed

        if match:

            new_name = match.group(1).strip()

            print(f"Found Item Name: {new_name}")

            # Avoid duplicates

            new_pdf_name = os.path.join(folder_path, f"{new_name}.pdf")

            counter = 1

            while os.path.exists(new_pdf_name):
                new_pdf_name = os.path.join(folder_path, f"{new_name}_{counter}.pdf")

                counter += 1

            # Rename the PDF file

            os.rename(pdf_path, new_pdf_name)

            print(f"PDF renamed to: {new_pdf_name}")

            valid_name = True

            break

    if not valid_name:
        print(f"No valid name found for file: {pdf_path}")
