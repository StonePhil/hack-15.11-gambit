# hack-15.11-gambit

This project is a small end-to-end web app that lets a user upload a **PDF document**, splits it into pages on the backend, runs **AI models** to detect **signatures, stamps and QR-codes** on each page, and then returns **per-page images with bounding boxes** drawn around all detections.

- **Frontend:** static HTML/CSS/JS (`index.html`, `process.html`)
- **Backend:** Flask API (`main.py`) that:
  - converts PDF → page images
  - runs Roboflow (signatures & stamps) + `qrdet` (QR codes)
  - returns URLs of processed images + raw detection metadata


## Features

- Upload one or more files from the browser (PDF focus).
- Live PDF preview in the browser before sending.
- Backend converts each PDF page to a JPEG image (300 DPI).
- For every page:
  - Roboflow model detects *stamps* and *signatures*.
  - `qrdet` model detects *QR codes*.
  - Bounding boxes and labels are drawn on a copy of the page.
- Frontend results viewer with:
  - full-page image preview
  - left/right arrow navigation (buttons + keyboard).
- JSON API returns both image URLs and raw detection data.


## Architecture

### Backend (Flask)

Backend logic lives in `main.py`:

- **Libraries used (core):**
  - `Flask`, `flask_cors` – web server and CORS
  - `pdf2image` – PDF → PIL images (requires Poppler)
  - `opencv-python` (`cv2`) – image IO and drawing bounding boxes
  - `requests`, `base64` – Roboflow REST API calls
  - `qrdet` – QR code detection model
  - `uuid`, `os` – file management

- **Key configuration constants:**

  ```python
  ROBOFLOW_API_KEY = "..."          # your Roboflow API key
  ROBOFLOW_MODEL_ID = "stamps-signatures-detection-oz2g3/2"
  UPLOAD_DIR = "uploads"            # where original PDFs & page images go
  RESULT_DIR = "results"            # where processed page images go
  POPPLER_PATH = r"C:\poppler-25.11.0\Library\bin"  # Poppler on Windows
