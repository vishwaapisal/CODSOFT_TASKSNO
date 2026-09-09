# CODSOFT Task 5 — FaceVision AI Complete

This version implements the Task 5 workflow with:
- image face detection and recognition
- enrollment by upload OR browser camera
- test image by upload OR browser camera
- live webcam face recognition
- uploaded video analysis
- YuNet pretrained deep-learning face detector
- SFace pretrained face-recognition model
- persistent local reference face

## Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Allow camera permission for camera/live features.

## AI models

The app uses YuNet and SFace from OpenCV Zoo. On first AI use it downloads the ONNX models using fallback mirrors. If the network blocks model downloads, manually place these files in `models/`:
- `face_detection_yunet_2023mar.onnx`
- `face_recognition_sface_2021dec.onnx`

## Demo

1. Enroll: upload or capture one clear face, enter the name, click Enroll.
2. Test Image: upload/capture another image and compare.
3. Live Camera: start live camera for continuous frame sampling and recognition.
4. Video: choose an MP4/WebM/MOV and analyze sampled frames.

The browser camera is processed locally through the Flask server; frames are sent to the local app for inference. This is an educational project, not a security or identity-verification system.
