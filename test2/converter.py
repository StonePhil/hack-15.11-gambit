from pdf2image import convert_from_path
import os

def convert_pdf_to_jpg(pdf_path, output_folder):
    # Convert the PDF to a list of images (one per page)
    images = convert_from_path(pdf_path, 300)  # 300 DPI for good resolution
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save each page as a JPG image
    for i, img in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        img.save(image_path, 'JPEG')
        print(f"Saved page {i + 1} as {image_path}")
        
# Example usage
pdf_path = 'path_to_pdf/document.pdf'
output_folder = 'path_to_output_images'
convert_pdf_to_jpg(pdf_path, output_folder)
