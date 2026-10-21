# A Raspberry Pi-Powered Computer Vision System for Real-Time People Counting

## Project Overview

An embedded computer vision system designed for real-time crowd detection, people counting, and occupancy monitoring using a Raspberry Pi 4B. Utilizing YOLOv8 object detection and OpenCV, the system detects human presence, tracks room capacity, triggers hardware alerts (LEDs and Buzzer) when thresholds are breached, and logs count changes to a local CSV dataset. An interactive Streamlit web dashboard provides real-time visualization of occupancy trends over time.

This project was developed for CPE0035L Embedded Systems Laboratory at Far Eastern University Alabang.

---

## Authors & Credits

- **Course Adviser:** Engr. Saturnino R. Perlas
- **Project Team:**
  - Balangue, John Paul P.
  - Dayao, Benedict C.
  - Llamas, Deo Raphael Miguel D.
  - Libay, Aaron Nathaniel M.
  - Tabor, Zian A.

---

## Features

- **Real-Time People Detection:** Leverages YOLOv8 (`yolov8n.pt`) with frame-skipping optimizations for smooth execution on edge hardware.
- **Interactive Capacity Setup:** Tkinter GUI prompt allowing users to set maximum occupancy limit on startup.
- **Hardware Alert System:**
  - **Green LED (GPIO 22):** Operational / Capacity Normal
  - **Red LED (GPIO 27) & Buzzer (GPIO 17):** Overcapacity Trigger
- **Smart Event Logging:** Logs timestamped data to `people_log.csv` only when occupancy count changes to prevent log bloat.
- **Analytics Dashboard:** Streamlit dashboard rendering data tables and line charts for occupancy trends.

---

## Hardware Pinout & Architecture

| Component | BCM GPIO Pin | Logic |
| :--- | :--- | :--- |
| **Active Buzzer** | `GPIO 17` | HIGH = Sound Alert |
| **Green LED** | `GPIO 22` | HIGH = Safe Capacity |
| **Red LED** | `GPIO 27` | HIGH = Over Capacity |
| **Webcam** | USB | Video Input Feed |

---

## Repository Structure

```text
.
├── people_count.py       # Main object detection, hardware alert & logging script
├── dashboard.py          # Streamlit visualization web interface
├── requirements.txt      # Python dependency manifest
├── .gitignore            # Git exclusion rules (logs, models, cache)
└── README.md             # Project documentation
```

---

## Installation & Setup

### 1. System Prerequisites
Ensure system dependencies (including Tkinter) are installed on your Raspberry Pi OS:
```bash
sudo apt update
sudo apt install python3-tk python3-pip python3-venv -y
```

### 2. Environment Setup
Clone the repository and create a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run

### Step 1: Start the People Counter
Run the detection script. A Tkinter window will pop up requesting the **Maximum People Capacity**:
```bash
python people_count.py
```
- Enter the maximum capacity limit and click **Submit**.
- The camera window will display the live stream with bounding boxes and real-time count.
- Press `q` while focused on the video window to exit.

### Step 2: Launch the Analytics Dashboard
In a separate terminal (with `.venv` activated), start Streamlit:
```bash
streamlit run dashboard.py
```
- Access the web dashboard at `http://localhost:8501`.

---

## Troubleshooting

- **`No module named 'RPi'`**: Ensure you are running inside the virtual environment where `RPi.GPIO` was installed (`source .venv/bin/activate`).
- **`AttributeError: module 'csv' has no attribute 'writer'`**: Ensure no file named `csv.py` exists in your project directory.
- **Laggy Video Stream**: The script uses frame skipping (`frame_skip = 5`) and reduced YOLO image resolution (`imgsz=320`) to maintain performance on Raspberry Pi.
