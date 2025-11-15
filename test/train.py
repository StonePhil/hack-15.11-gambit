from ultralytics import YOLO

def train_model():
    # Загружаем базовую модель для дообучения
    model = YOLO('yolov8n.pt')  # Модель YOLO

    # Запуск обучения
    model.train(
        data='data.yaml',          # Описание классов и путей к данным
        epochs=50,                 # Количество эпох
        imgsz=640,                 # Размеры изображений
        batch=8,                   # Размер батча
        project='runs/train',      # Папка для результатов
        name='document_model',     # Имя проекта
    )

    print("[INFO] Обучение завершено. Модель сохранена в 'runs/train/document_model/weights/best.pt'")

if __name__ == "__main__":
    train_model()
