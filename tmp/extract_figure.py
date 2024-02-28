import fitz  # PyMuPDF
import cv2
import os
import PIL as Image
import numpy as np

# Image parser that detects framed sub-images in an input .png image
def extract_sub_images_by_contours(offset, image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    print(f"image file path: {image_path}")

    # Apply adaptive thresholding to handle different lighting conditions
    # and potentially different thicknesses of the black lines framing the sub-images
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours on the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out contours that do not meet the expected criteria (e.g., size, aspect ratio)
    min_area = 100  # Adjusted to be more inclusive of smaller areas, considering thin lines
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # Extract the bounding rectangles for each contour and sort them by position
    bounding_rects = [cv2.boundingRect(cnt) for cnt in contours]
    # Sort by top to bottom first (y coordinate), then by left to right (x coordinate)
    bounding_rects.sort(key=lambda x: (x[1], x[0]))

    # Extract the sorted sub-images
    sub_images = [img[y:y+h, x:x+w] for x, y, w, h in bounding_rects]

    # Save the sub-images and provide file paths for the saved images with correct indexing
    file_paths = []
    for i, sub_img in enumerate(sub_images):
        # Indexing starts at offset and goes from top left to bottom right
        path = f"/home/vcl/Desktop/workspace/nhp_lmc_amd/tmp/output_png/contour_sub_image_{offset+i+1}.png"

        cv2.imwrite(path, sub_img)
        file_paths.append(path)

    offset += len(sub_images)

    return file_paths, offset

# Takes an .pdf as input and converts it to .png images
def convert_pdf_to_png(pdf_path, output_folder):
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]
        
        # Render page to an image (pixmap)
        pix = page.get_pixmap()
        
        # Define the output image path
        output_image_path = f"{output_folder}/page_{page_number + 1}.png"
        
        # Save the pixmap as a PNG
        pix.save(output_image_path)
    
    # Close the PDF after processing
    pdf_document.close()

if __name__ == "__main__":

    # get the path to the folder where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Example usage
    pdf_file_path    = os.path.join(script_dir, "QUIZ-BASE.pdf")
    input_png_folder = os.path.join(script_dir, "input_png")
    output_png_folder = os.path.join(script_dir, "output_png")

    convert_pdf_to_png(pdf_file_path, input_png_folder)

    # Offset is needed to give a progressive index to the sub-images when changing pages
    offset = 0

    for filename in os.listdir(input_png_folder):
        
        print(f"Processing image {filename}")
        
        if filename.endswith(".png"):
            
            input_image_path = os.path.join(input_png_folder, filename)
            
            # Use the helper function to extract sub images from the uploaded image
            contour_sub_image_paths, offset = extract_sub_images_by_contours(offset, input_image_path)
            # Return the number of sub-images found and their paths
            print(len(contour_sub_image_paths), contour_sub_image_paths)
        else:
            continue
