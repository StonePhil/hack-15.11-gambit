from ultralytics import YOLO
import cv2
from pathlib import Path


# ---------- НАСТРОЙКИ ----------
# пока используем стандартную yolov8n, потом заменишь на свою best.pt
MODEL_PATH = "yolov8n.pt"        # позже: "runs/train/digital_inspector/weights/best.pt"
INPUT_IMAGE = "test_images/doc1.jpg"
OUTPUT_IMAGE = "runs/doc1_result.jpg"


def run_inference():
    input_path = Path(INPUT_IMAGE)
    output_path = Path(OUTPUT_IMAGE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Нет входного изображения: {input_path}")

    print(f"[INFO] Загружаю модель из {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)

    print(f"[INFO] Запускаю детекцию на {input_path}...")
    results = model(str(input_path))

    # берём первый результат
    result = results[0]

    # картинка с нарисованными боксами (numpy массив BGR)
    annotated_img = result.plot()

    # сохраняем результат
    cv2.imwrite(str(output_path), annotated_img)
    print(f"[INFO] Результат сохранён в {output_path}")

    # выводим инфу о предсказанных объектах
    print("\n[DETECTIONS]")
    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        print(f"Класс: {cls_id}, уверенность: {conf:.2f}")


if __name__ == "__main__":
    run_inference()
