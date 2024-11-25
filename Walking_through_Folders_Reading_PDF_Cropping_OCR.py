import os
import re
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Set the Tesseract OCR executable path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Root folder containing all subfolders and PDFs

root_folder = 'C:/Users/farza/OneDrive/Desktop/AIML/Associate Data Scientist In Python/Python_Projects_DataCamp/pythonProject1/'

# Define the cropping coordinates (x1, y1, x2, y2) based on Piece # box position

crop_box = (2108, 392, 2187, 1209)  # Example coordinates (adjust as needed)

# Pattern to match PDF names

pdf_name_pattern = re.compile(r'^Remote Desktop Redirected Printer Doc(\s*\(\d+\))?\.pdf$', re.IGNORECASE)


# Function to recursively process all folders

def process_folders(folder_path):
    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if pdf_name_pattern.match(file):  # Check if the file matches the naming pattern
                pdf_path = os.path.join(root, file)
                print(f"Processing file: {pdf_path}")
                process_pdf(pdf_path)


# Function to process a single PDF

def process_pdf(pdf_path):
    try:

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

                new_pdf_name = os.path.join(os.path.dirname(pdf_path), f"{new_name}.pdf")
                counter = 1

                while os.path.exists(new_pdf_name):
                    new_pdf_name = os.path.join(os.path.dirname(pdf_path), f"{new_name}_{counter}.pdf")
                    counter += 1

                # Rename the PDF file

                os.rename(pdf_path, new_pdf_name)
                print(f"PDF renamed to: {new_pdf_name}")
                valid_name = True

                break

        if not valid_name:
            print(f"No valid name found for file: {pdf_path}")


    except Exception as e:

        print(f"Error processing file {pdf_path}: {e}")


# Run the recursive processing

process_folders(root_folder)