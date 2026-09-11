# 🖼️ AI Image Captioning

## 📌 Project Overview

This project is developed as part of the CodSoft Artificial Intelligence Internship – Task 3: Image Captioning.

The application uses a pre-trained BLIP (Bootstrapping Language-Image Pre-training) model to analyze an uploaded image and automatically generate a meaningful text caption.

## 🚀 Features

- Upload JPG, JPEG, or PNG images
- AI automatically analyzes the image
- Generates a descriptive caption
- Simple and user-friendly Streamlit interface
- Uses a pre-trained BLIP image captioning model

## 🛠️ Technologies Used

- Python
- PyTorch
- Hugging Face Transformers
- BLIP Model
- Pillow
- Streamlit

## 🧠 How It Works

1. The user uploads an image.
2. The image is processed using the BLIP processor.
3. The pre-trained BLIP model analyzes the image.
4. The model generates a text description.
5. The generated caption is displayed on the screen.

## 📂 Project Structure

```text
Task_3_Image_Captioning/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── test.jpg
└── venv/