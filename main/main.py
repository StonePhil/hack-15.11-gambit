from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import uuid
from qrdet import QRDetector
import cv2
import base64
import requests
from pdf2image import convert_from_path

# ---------- CONFIG ----------

PLACEHOLDER_PDF = "placeholder.pdf"

ROBOFLOW_API_KEY = "69h5oA8TM54t3lL1GwQU"
ROBOFLOW_MODEL_ID = "stamps-signatures-detection-oz2g3/2"
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"

# ADD THIS:
POPPLER_PATH = r"C:\poppler-25.11.0\Library\bin"    # <- REQUIRED for Windows


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# Initialize QR code model
qr_detector = QRDetector(model_size="n")


# ---------- DETECTION FUNCS ----------
def roboflow_detect(image_path: str):
    """REST request to Roboflow."""
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    url = f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}?api_key={ROBOFLOW_API_KEY}"

    response = requests.post(
        url,
        data=img_base64,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    return response.json()


def run_both_models(image_path: str, output_path: str):
    """Run Roboflow + QR detector on one image."""
    image = cv2.imread(image_path)

    rf_data = roboflow_detect(image_path)
    rf_preds = rf_data.get("predictions", [])

    qr_preds = qr_detector.detect(image=image, is_bgr=True)

    out = image.copy()

    # Draw roboflow detections (green)
    for det in rf_preds:
        x, y = det["x"], det["y"]
        w, h = det["width"], det["height"]
        cls_name = det["class"]
        conf = det["confidence"]

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        cv2.rectangle(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(out, f"{cls_name} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Draw QR detections (blue)
    for det in qr_preds:
        x1, y1, x2, y2 = map(int, det["bbox_xyxy"])
        conf = det["confidence"]

        cv2.rectangle(out, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(out, f"qr {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imwrite(output_path, out)

    return rf_preds, qr_preds


# ---------- FLASK APP ----------
app = Flask(__name__)


@app.route("/process_pdf", methods=["GET", "POST"])
def process_pdf():
    """Receive PDF -> return processed images + detections."""

    pdf_path = PLACEHOLDER_PDF
    file_id = "placeholder"

    # Convert PDF to images (UPDATED with poppler_path)
    print(f"[INFO] Using placeholder PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    print(f"[INFO] Pages found: {len(pages)}")

    page_image_paths = []
    detections_output = []

    for i, page in enumerate(pages, start=1):
        img_path = os.path.join(UPLOAD_DIR, f"{file_id}_page_{i}.jpg")
        result_img_path = os.path.join(RESULT_DIR, f"{file_id}_result_{i}.jpg")

        page.save(img_path, "JPEG")

        # Run AI models
        rf, qr = run_both_models(img_path, result_img_path)

        detections_output.append({
            "page": i,
            "roboflow": rf,
            "qr": qr,
            "result_image": f"/result_image/{os.path.basename(result_img_path)}"
        })

        page_image_paths.append(result_img_path)

    return jsonify({
        "file_id": file_id,
        "pages": len(pages),
        "detections": detections_output
    })


@app.route("/result_image/<filename>")
def get_result_image(filename):
    """Serve processed image."""
    return send_from_directory(RESULT_DIR, filename)


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
