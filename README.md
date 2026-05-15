# 🖐️ HandTrack AI — YOLO Hand Detection & Trajectory Tracking

A full-stack AI system that detects human hands in uploaded videos using **YOLOv8**,
tracks the hand movement path frame-by-frame, and generates annotated outputs
including trajectory videos, CSV data, and analysis plots.

Built with **FastAPI** · **React + Vite** · **OpenCV** · **YOLOv8**

---

## 🚀 Features

- ✅ YOLOv8-powered hand detection on every frame
- ✅ Real hand movement trajectory — straight line, circle, oval, zigzag — drawn exactly as moved
- ✅ Annotated output video with bounding box + colour-gradient trajectory path
- ✅ Full trajectory CSV export (every frame + detected-only)
- ✅ 3-panel matplotlib analysis plot
- ✅ Dark-mode React dashboard with drag-and-drop upload
- ✅ Real upload progress bar with live inference status
- ✅ All results open in a new tab (video, CSV, plot)
- ✅ Docker + CI/CD support

---

## 🛠️ Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| FastAPI | REST API framework |
| YOLOv8 (Ultralytics) | Hand detection model |
| OpenCV | Video processing + drawing |
| Pandas | CSV export |
| Matplotlib | Trajectory analysis plots |
| Pydantic v2 | Settings + response validation |
| Uvicorn | ASGI server |

### Frontend
| Tool | Purpose |
|---|---|
| React 18 | UI framework |
| Vite 5 | Dev server + bundler |
| JavaScript (JSX) | Component language |
| HTML + CSS | Base layout + global styles |

---

## 📂 Project Structure

```
YOLO-Hand_Detection/
│
├── README.md
├── .gitignore
├── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml                     ← GitHub Actions CI/CD
│
├── Backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── best.pt                        ← YOLOv8 trained model (place here)
│   │
│   └── app/
│       ├── main.py                    ← FastAPI entry point
│       │
│       ├── core/
│       │   └── config.py              ← All settings from .env
│       │
│       ├── schemas/
│       │   └── detection.py           ← Pydantic request/response models
│       │
│       ├── api/
│       │   └── routes/
│       │       └── detection.py       ← POST /api/detect · GET /api/results/{id}
│       │
│       ├── services/
│       │   ├── yolo_service.py        ← Model loader + inference per frame
│       │   ├── video_service.py       ← Frame loop + trajectory drawing
│       │   └── trajectory_service.py  ← CSV export + matplotlib plot
│       │
│       ├── utils/
│       │   └── file_utils.py          ← File validation + UUID job dirs
│       │
│       ├── uploads/                   ← Incoming videos (auto-created)
│       └── outputs/                   ← Job results served as static files
│
└── Frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── index.html
    ├── vite.config.js
    ├── package.json
    ├── .env
    │
    └── src/
        ├── main.jsx                   ← React root
        ├── App.jsx                    ← App shell + header + global CSS
        │
        ├── services/
        │   └── api.js                 ← All backend HTTP calls
        │
        ├── hooks/
        │   ├── useDetection.js        ← Upload state machine
        │   └── useToast.js            ← Notification manager
        │
        ├── pages/
        │   └── Dashboard.jsx          ← Main page
        │
        └── components/
            ├── UploadZone.jsx         ← Drag-and-drop video picker
            ├── ProgressBar.jsx        ← Animated progress bar
            ├── StatCard.jsx           ← Single metric card
            ├── AnalyticsPanel.jsx     ← Stats grid
            ├── VideoPlayer.jsx        ← Output video player
            ├── TrajectoryPlot.jsx     ← Trajectory PNG viewer
            ├── DownloadButton.jsx     ← Opens files in new tab
            └── Toast.jsx              ← Success/error notifications
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or above
- Node.js 18 or above
- Your trained `best.pt` YOLOv8 model file

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/aryasohani/YOLO-Hand_Detection.git
cd YOLO-Hand_Detection
```

---

### 2️⃣ Backend Setup

```bash
cd Backend
```

#### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Place Your Model

```
Backend/
└── models/
    └── best.pt     ← place your trained model here
```

#### Create Environment File

```bash
cp .env.example .env
```

Open `.env` and configure:

```
MODEL_PATH=models/best.pt
CONF_THRESHOLD=0.25
UPLOAD_DIR=app/uploads
OUTPUT_DIR=app/outputs
MAX_FILE_SIZE_MB=500
DEBUG=false
```

#### Run Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000` | Backend base URL |
| `http://127.0.0.1:8000/docs` | Swagger API documentation |
| `http://127.0.0.1:8000/health` | Health check |

---

### 3️⃣ Frontend Setup

Open a **new terminal**:

```bash
cd Frontend
```

#### Create Environment File

Create a `.env` file inside `Frontend/`:

```
VITE_API_URL=http://127.0.0.1:8000
```

#### Install Dependencies

```bash
npm install
```

#### Run Frontend

```bash
npm run dev
```

Frontend runs on: `http://localhost:5173`

---

## 🖥️ How to Use

1. Open `http://localhost:5173` in your browser
2. Header shows **🟢 API Online** when backend is connected
3. Drag and drop a video OR click to browse
4. Click **Analyze Video**
5. Watch the progress bar — upload then inference
6. Results appear automatically:
   - Trajectory analysis plot
   - Annotated video (plays inline)
   - Download buttons → open video, CSV, and plot in a new tab

---

## 📊 Output Files

| File | Description |
|---|---|
| `output_trajectory.mp4` | Annotated video with bounding box + movement path |
| `trajectory_full.csv` | All frames including undetected ones |
| `trajectory_clean.csv` | Detected frames only — clean coordinate data |
| `trajectory_plot.png` | 3-panel: 2D map · X/Y over time · confidence |

---

## 🎯 Trajectory Drawing

The trajectory is the **exact real path** the hand moved:

| Hand Movement | Trajectory Shape |
|---|---|
| Straight left to right | Straight line |
| Circle motion | Circle |
| Oval motion | Oval |
| Zigzag | Zigzag |
| L-shape | L-shape |

Colour gradient shows direction:
- 🔴 **Red** = where the hand started
- 🟡 **Yellow** = middle of the path
- 🟢 **Green** = current / most recent position

---

## 🌐 API Reference

### `POST /api/detect`
Upload a video and run hand detection.

**Request:** `multipart/form-data` — field name: `file`

**Response:**
```json
{
  "success": true,
  "job_id": "uuid",
  "output_video_url": "/outputs/{id}/output_trajectory.mp4",
  "csv_full_url":     "/outputs/{id}/trajectory_full.csv",
  "csv_clean_url":    "/outputs/{id}/trajectory_clean.csv",
  "graph_url":        "/outputs/{id}/trajectory_plot.png",
  "stats": {
    "total_frames": 450,
    "detected_frames": 423,
    "detection_pct": 94.0,
    "processing_time": 38.5,
    "avg_confidence": 0.882
  }
}
```

### `GET /api/results/{job_id}`
Get output file URLs for a completed job.

### `GET /health`
Returns `{ "status": "ok", "service": "HandTrack AI", "version": "1.0.0" }`.

---

## 📦 CSV Schema

```
frame, timestamp, detected, cx_px, cy_px, cx_norm, cy_norm,
bbox_x1, bbox_y1, bbox_x2, bbox_y2, confidence
```

---

## 🐳 Docker Deployment

```bash
cp /path/to/best.pt Backend/models/best.pt
docker compose up --build

# Frontend → http://localhost:80
# Backend  → http://localhost:8000
```

---

## 📊 Applications

- Gesture Recognition
- Sign Language Detection
- Hand Trajectory Analysis
- Human Computer Interaction
- Virtual Mouse Systems
- AI Surveillance
- Sports Motion Analysis

---

## 🔥 Future Improvements

- Hand Gesture Classification
- Multi-Hand Tracking
- Real-time Webcam Support
- Cloud Deployment
- Mobile Integration
- Gesture-to-text Translation

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

### Arya Sohani

GitHub: https://github.com/aryasohani

Repository: https://github.com/aryasohani/YOLO-Hand_Detection