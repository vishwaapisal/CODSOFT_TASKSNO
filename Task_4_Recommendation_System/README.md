# 🎬 CineMatch AI - Movie Recommendation System

## 📌 Project Overview

CineMatch AI is a simple content-based movie recommendation system developed as part of the CodSoft Artificial Intelligence Internship.

The system recommends movies similar to a movie selected by the user. It uses **TF-IDF Vectorization** and **Cosine Similarity** to compare movie descriptions and find similar movies.

## ✨ Features

- 🎬 Select a movie from the available list
- 🤖 AI-based movie recommendations
- 🔍 Content-based filtering
- 📊 TF-IDF Vectorization
- 📐 Cosine Similarity
- 🎨 Interactive and colorful Streamlit interface
- ⭐ Displays the top 5 recommended movies

## 🧠 How It Works

1. Movie descriptions are stored in a dataset.
2. TF-IDF converts the descriptions into numerical vectors.
3. Cosine Similarity calculates how similar the movies are.
4. The selected movie is compared with all other movies.
5. The top 5 most similar movies are displayed as recommendations.

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit

## 📂 Project Structure

```text
Task_4_Recommendation_System/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
└── venv/