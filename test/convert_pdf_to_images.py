from pdf2image import convert_from_path
import os

def convert_pdf(pdf_path, output_dir):
    # Преобразуем PDF в изображения
    pages = convert_from_path(pdf_path, 300)  # 300 dpi для хорошего качества

    for i, page in enumerate(pages):
        image_path = os.path.join(output_dir, f"{os.path.basename(pdf_path).replace('.pdf', '')}_page_{i+1}.jpg")
        page.save(image_path, 'JPEG')
        print(f"[INFO] Сохранена страница {i+1} как {image_path}")

# Путь к PDF и папка для изображений
pdf_folder = 'datasets/pdfs'
output_folder = 'datasets/images/train'

# Создаём папку для изображений
os.makedirs(output_folder, exist_ok=True)

# Обрабатываем каждый PDF файл
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        convert_pdf(os.path.join(pdf_folder, pdf_file), output_folder)

print("[INFO] Все PDF файлы преобразованы в изображения.")
