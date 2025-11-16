# hack-15.11-gambit

This project provides a complete workflow for uploading a **PDF**, splitting it into pages, detecting **signatures**, **stamps**, and **QR codes** on each page using AI models, and returning processed page images with **bounding boxes** drawn on all detections.

It includes:

- A **Flask backend** (`main.py`) that handles PDF processing and AI detection.
- A **frontend** (`index.html` + `process.html`) for uploading files and viewing results.
- A simple **results viewer** with page-by-page navigation.

---

## ✨ Features

- Upload a single PDF from the browser  
- Backend converts PDF → images (one per page)  
- Each page is processed by:  
  - **Roboflow** model → detects signatures & stamps  
  - **QRdet** model → detects QR codes  
- Bounding boxes + labels drawn on the final output images  
- Frontend displays results with left/right navigation  
- All output images are served directly by Flask  

---

## 📁 Project Structure

```

.
├── main.py          # Flask backend (PDF → pages → AI detection → results)
├── index.html       # Upload page with PDF preview
├── process.html     # Result viewer (shows processed images)
├── uploads/         # Temporary storage for input PDFs + page images
└── results/         # Output images with bounding boxes

```

---

## ⚙️ How It Works

### 1. User uploads a PDF (`index.html`)
- Drag-and-drop or click to upload.
- Frontend generates a PDF preview.
- On submit, the PDF is sent via `FormData` to:

```

POST [http://localhost:5005/process_pdf](http://localhost:5005/process_pdf)

````

### 2. Backend receives the PDF (`main.py`)
For each upload:

1. Saves the PDF to `uploads/`.
2. Runs `pdf2image` to convert PDF → page images.
3. For each page:
   - Runs Roboflow API for **stamps/signatures**
   - Runs QRdet for **QR codes**
   - Draws bounding boxes on the page using OpenCV
4. Saves the processed page to `results/`.

### 3. Backend responds with JSON
Example:

```json
{
  "file_id": "uuid",
  "pages": 3,
  "images": [
    "http://localhost:5005/result_image/<id>_result_1.jpg",
    "http://localhost:5005/result_image/<id>_result_2.jpg"
  ],
  "detections": [
    {
      "page": 1,
      "roboflow": [...],
      "qr": [...],
      "result_image": "http://localhost:5005/result_image/<id>_result_1.jpg"
    }
  ]
}
````

The frontend saves `images` to `localStorage`.

### 4. Results displayed (`process.html`)

* Loads URLs from `localStorage.resultImages`
* Shows one page at a time
* Left/right buttons + keyboard arrows navigate pages

---

## 🧠 Backend Components

* **Flask + CORS** — API server
* **pdf2image** — convert PDF → images
* **OpenCV** — draw detections on page images
* **Roboflow API** — signature + stamp detection
* **qrdet** — QR detection
* **UUID** — file isolation
* **Static file serving** — annotated images served from `/result_image/<filename>`

---

## 📌 Installation

### 1. Install dependencies

```bash
pip install flask flask-cors pdf2image opencv-python requests qrdet
```

### 2. Install Poppler (required for pdf2image)

* Windows: download Poppler binaries and set the path in `main.py`:

```python
POPPLER_PATH = r"C:\path\to\poppler\bin"
```

---

## ▶️ Running the App

### Start backend

```bash
python main.py
```

Runs on:

```
http://localhost:5005
```

### Start frontend

Serve HTML files using any static server, e.g.:

```bash
python -m http.server 8000
```

Open:

```
http://localhost:8000/index.html
```

---

## 🔌 API Endpoints

### `POST /process_pdf`

Upload a single PDF.
Response: JSON with detection data + image URLs.

### `GET /result_image/<filename>`

Returns one processed JPEG page with bounding boxes.

---

## 📝 Notes / TODO

* Move API keys to environment variables
* Improve error UI on frontend
* Allow multi-PDF batch processing
* Make output image scaling responsive on all screen sizes

---

## 👍 Summary

This project forms a complete pipeline:

**PDF → page extraction → AI detection → bounding box drawing → per-page results → browser viewer**

Works perfectly for document forensics, automated auditing, or structured document analysis.

---

```
```

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
