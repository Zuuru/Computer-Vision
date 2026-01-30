# 🖐️ Realtime ASL Alphabet Detection (Web-Based)

A web-based application for **real-time American Sign Language (ASL) alphabet recognition** using **MediaPipe Hand Landmark** and **K-Nearest Neighbor (KNN)** algorithm.
The entire training and prediction process runs **directly in the browser** without any backend server.

---

## ✨ Features

* 🔍 Real-time hand detection using **MediaPipe Hands**
* 🧠 ASL alphabet classification using **KNN (K-Nearest Neighbor)**
* 🌐 Fully **web-based** (HTML, JavaScript, p5.js)
* 🎥 Supports **external webcam** (e.g., DroidCam)
* 📊 Dataset split **80:20** for training and testing
* 🧩 Uses **21 hand landmarks (42 features)** per sample

---

## 🧠 Tech Stack

* **JavaScript (ES6)**
* **p5.js** – rendering & webcam handling
* **MediaPipe Hands** – hand landmark extraction
* **KNN Algorithm** – classification
* **Python** – dataset landmark extraction (offline)

---

## 📂 Project Structure

```
project-root/
│
├── index.html          # Main web interface
├── sketch.js           # Realtime ASL detection logic (KNN + MediaPipe)
├── asl_landmarks.csv   # Extracted landmark dataset
├── landmark_extract.py # Python script for landmark extraction
└── README.md
```

---

## 📊 Dataset

* **Source**: ASL Alphabet Dataset (Kaggle)
* **Classes**: A–Z (static hand signs)
* **Features**: 21 hand landmarks (x, y) → 42 features

Each image is processed using MediaPipe Hands and stored in CSV format before being loaded into the browser.

---

## ⚙️ How It Works

1. ASL images are processed using **MediaPipe Hands** to extract hand landmarks
2. Landmark coordinates are **normalized** relative to the wrist and hand scale
3. Data is split into **80% training** and **20% testing**
4. KNN model is trained **directly in the browser**
5. Webcam input is classified in real-time

---

## 🚀 How to Run

### 1️⃣ Download Dataset
https://www.kaggle.com/datasets/grassknoted/asl-alphabet
### 2️⃣ Clone Repository

```bash
git clone https://github.com/Zuuru/Computer-Vision/tree/72e794f347ec799f51114da604754423c4748d09/ASL%20Handsign
cd ASL Handsign
```

### 3️⃣ Run with Live Server

Use **VS Code Live Server** or any local web server:

```bash
npx serve
```

> ⚠️ Webcam access requires **HTTP server** (not file://)

---

## 📷 Using External Camera (DroidCam)

1. Start **DroidCam** on your phone and PC
2. Open the web app in Chrome
3. Allow camera permission
4. Select **DroidCam Source** as the active camera

The app will automatically use it as the video input.

---

## 📈 Performance

* **Accuracy**: ~90% (static ASL letters)
* Best performance on: A, B, C, O, Y
* Challenging letters: M, N, R (similar hand shapes)
* Dynamic letters (J, Z) are **not supported**

---

## ⚠️ Limitations

* Only supports **static ASL alphabets**
* Sensitive to lighting and hand orientation
* KNN performance depends on dataset balance

---

## 🔮 Future Improvements

* Add temporal models (LSTM) for dynamic signs
* Improve prediction stability (temporal smoothing)
* Add confidence score visualization
* Extend to word and sentence recognition

---

## 📚 References

* Google MediaPipe Documentation
* Kaggle – ASL Alphabet Dataset
* Cover, T. & Hart, P. (1967). Nearest Neighbor Pattern Classification

---

## 👤 Author

**Name**: *Zulfikri Arya*
**Institution**: *Semarang State Polytechnics*
**Year**: 2025

---

Read Here
https://docs.google.com/document/d/17k_K_H_8d2mkQRR-Zj8_kErpMfTHJh53/edit?usp=sharing&ouid=114661000494467937234&rtpof=true&sd=true
