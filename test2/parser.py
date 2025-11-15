import json
import cv2
import numpy as np
import os

def load_annotations(json_file):
    # Load the selected_annotations.json file
    with open(json_file, 'r') as f:
        annotations_data = json.load(f)
    return annotations_data

def process_annotations(annotations_data, image_folder):
    images = []
    labels = []
    image_paths = []

    for pdf, pdf_data in annotations_data.items():
        for page, page_data in pdf_data.items():
            if 'annotations' in page_data:
                # Load the image for the current page
                image_path = os.path.join(image_folder, f"{page}.jpg")  # Assuming images are named as page_1.jpg, page_2.jpg, etc.
                img = cv2.imread(image_path)
                image_paths.append(image_path)

                # Process each annotation on this page
                for annotation in page_data['annotations']:
                    for ann_id, ann_data in annotation.items():
                        category = ann_data['category']
                        bbox = ann_data['bbox']
                        x, y, width, height = int(bbox['x']), int(bbox['y']), int(bbox['width']), int(bbox['height'])

                        # Crop the image using the bounding box
                        cropped_image = img[y:y+height, x:x+width]

                        # Resize to a fixed size (e.g., 224x224)
                        cropped_resized = cv2.resize(cropped_image, (224, 224))

                        # Normalize the image and add to list
                        cropped_resized = cropped_resized / 255.0
                        images.append(cropped_resized)

                        # Append the label corresponding to the category
                        labels.append(category)

    return np.array(images), np.array(labels), image_paths

# Example usage:
annotations_data = load_annotations('selected_annotations.json')
image_folder = 'path_to_output_images'
images, labels, image_paths = process_annotations(annotations_data, image_folder)

print(f"Processed {len(images)} images with labels {labels[:5]}")
