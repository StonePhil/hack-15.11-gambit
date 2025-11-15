import json
import os

# Загружаем аннотации
with open("selected_annotations.json", "r") as f:
    selected_annotations = json.load(f)

with open("masked_annotations.json", "r") as f:
    masked_annotations = json.load(f)

# Создаём директории для изображений и меток
os.makedirs("datasets/images/train", exist_ok=True)
os.makedirs("datasets/labels/train", exist_ok=True)

# Процесс для каждого PDF
def prepare_annotations(annotations_data, dataset_type="train"):
    for pdf_file, pdf_data in annotations_data.items():
        for page, page_data in pdf_data.items():
            # Получаем размеры страницы
            page_width = page_data["page_size"]["width"]
            page_height = page_data["page_size"]["height"]

            # Создаём файл для меток
            label_file = f"datasets/labels/{dataset_type}/{pdf_file.replace('.pdf', '')}_page_{page}.txt"
            
            with open(label_file, "w") as label_f:
                # Обрабатываем аннотации
                for annotation in page_data["annotations"]:
                    for key, ann in annotation.items():
                        category = ann["category"]
                        bbox = ann["bbox"]
                        # Нормализуем координаты (от 0 до 1)
                        x_center = (bbox["x"] + bbox["width"] / 2) / page_width
                        y_center = (bbox["y"] + bbox["height"] / 2) / page_height
                        width = bbox["width"] / page_width
                        height = bbox["height"] / page_height
                        
                        # Пишем метку для YOLO
                        label_f.write(f"{category} {x_center} {y_center} {width} {height}\n")

# Обрабатываем данные для обоих файлов
prepare_annotations(selected_annotations, "train")
prepare_annotations(masked_annotations, "train")

print("[INFO] Аннотации подготовлены для обучения.")
