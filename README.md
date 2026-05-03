# 🖐️ AI Virtual Mouse 

An AI-based virtual mouse system that allows you to control your computer using **hand gestures** in real-time.
Built using computer vision and gesture recognition, this project replaces traditional mouse interaction with intuitive hand movements.

---

## 🚀 Features

* 🎯 **Cursor Movement** — Move mouse using index finger
* 🤏 **Left Click** — Pinch (thumb + index)
* 🖱️ **Right Click** — 3 fingers + pinch
* 🧲 **Drag & Drop** — Pinch and hold
* ✌️ **Scroll Up** — 2 fingers (smooth continuous scroll)
* 🖖 **Scroll Down** — 3 fingers
* 👍 **Pause Mode** — Fist stops all actions
* 🔊 **Volume Control** — Adjust volume using finger distance
* 🧊 **Smooth Cursor Movement** — Reduced jitter with interpolation
* 🎯 **Control Box** — Better accuracy and stability

---

## 🛠️ Technologies Used

* OpenCV
* MediaPipe
* PyAutoGUI
* Pycaw
* NumPy

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Virtual-Mouse.git
cd AI-Virtual-Mouse
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install opencv-python mediapipe pyautogui numpy
pip install pycaw==20181226 comtypes
```

---

### 4. Download model file

Download:
👉 https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task

Place it in project folder:

```
AI-Virtual-Mouse/
    main.py
    hand_landmarker.task
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🖐️ Gesture Controls

| Gesture            | Action         |
| ------------------ | -------------- |
| ☝️ Index finger    | Move cursor    |
| 🤏 Thumb + Index   | Left click     |
| 🤏 Hold pinch      | Drag & drop    |
| ✌️ Two fingers     | Scroll up      |
| 🖖 Three fingers   | Scroll down    |
| 🖖 + pinch         | Right click    |
| ✊ Fist             | Pause          |
| 🤏 Distance change | Volume control |

---

## ⚙️ Configuration

You can tweak sensitivity in code:

```python
smoothening = 7        # cursor smoothness
scroll_speed = 8       # scroll speed
scroll_decay = 0.92    # scroll smoothness
```

---

## ⚠️ Requirements

* Python 3.10 (recommended)
* Webcam
* Windows OS (for volume control support)

---

## 📌 Notes

* Ensure good lighting for accurate detection
* Keep hand inside camera frame
* Use plain background for best performance

---

## 📈 Future Improvements

* Gesture-based mode switching
* Custom gesture training
* GUI overlay interface
* Multi-hand support
* Performance optimization (FPS boost)

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* Google MediaPipe team
* OpenCV community

---

## 💼 Author

**Sarthak Kalyani**
B.Tech CSE | AI Enthusiast

---

⭐ If you like this project, give it a star!
