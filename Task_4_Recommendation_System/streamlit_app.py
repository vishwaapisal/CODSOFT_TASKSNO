import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(126, 54, 180, 0.30), transparent 35%),
        radial-gradient(circle at 90% 90%, rgba(30, 130, 180, 0.25), transparent 35%),
        linear-gradient(135deg, #090914, #111124, #0b1825);
    color: white;
}

.block-container {
    max-width: 1000px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.badge {
    display: table;
    margin: 0 auto 18px auto;
    padding: 7px 18px;
    border-radius: 30px;
    background: linear-gradient(90deg, #ff4ecd, #7b61ff);
    color: white;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 0 25px rgba(255, 78, 205, 0.35);
}

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 800;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #ff4ecd, #9b7cff, #4dd9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #c9c9dc;
    font-size: 18px;
    margin-bottom: 45px;
}

.section-title {
    color: white;
    font-size: 27px;
    font-weight: 700;
    margin-bottom: 10px;
}

div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 12px;
}

div[data-baseweb="select"] span {
    color: white;
}

.stButton {
    margin-top: 25px;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(90deg, #ff4ecd, #7b61ff, #4dd9ff);
    color: white;
    font-size: 17px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(123, 97, 255, 0.30);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(255, 78, 205, 0.40);
}

.recommendation-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    margin-top: 55px;
    margin-bottom: 25px;
    color: white;
}

.selected-movie {
    color: #ff70d6;
}

.movie-card {
    padding: 20px 24px;
    margin: 14px 0;
    border-radius: 18px;
    background: linear-gradient(
        110deg,
        rgba(255, 78, 205, 0.15),
        rgba(123, 97, 255, 0.14),
        rgba(77, 217, 255, 0.10)
    );
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    transition: all 0.25s ease;
}

.movie-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 78, 205, 0.55);
    box-shadow: 0 12px 35px rgba(255, 78, 205, 0.18);
}

.movie-number {
    display: inline-block;
    width: 55px;
    font-size: 26px;
    font-weight: 800;
    color: #ff70d6;
}

.movie-name {
    display: inline-block;
    font-size: 19px;
    font-weight: 600;
    color: white;
}

.info-box {
    margin-top: 35px;
    padding: 18px 22px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.10);
    color: #c7c7d9;
    text-align: center;
    font-size: 14px;
}

.footer {
    text-align: center;
    margin-top: 55px;
    padding-top: 22px;
    border-top: 1px solid rgba(255, 255, 255, 0.10);
    color: #8888a8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="badge">🤖 AI POWERED • CONTENT-BASED FILTERING</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🎬 CineMatch AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Discover movies you might love based on what you already enjoy.</div>',
    unsafe_allow_html=True
)


# =========================================================
# MOVIE DATASET
# =========================================================

movies = pd.DataFrame({
    "title": [
        "Inception",
        "Interstellar",
        "The Dark Knight",
        "Titanic",
        "The Notebook",
        "Avengers: Endgame",
        "Iron Man",
        "Jurassic Park",
        "The Matrix",
        "Toy Story"
    ],

    "description": [
        "science fiction thriller dream technology action",
        "science fiction space adventure emotional technology",
        "action crime thriller superhero batman",
        "romance drama love emotional historical",
        "romance drama love relationship emotional",
        "action superhero adventure marvel science fiction",
        "action superhero technology marvel adventure",
        "science fiction adventure dinosaurs thriller",
        "science fiction action technology thriller",
        "animation comedy family adventure"
    ]
})


# =========================================================
# TF-IDF AND COSINE SIMILARITY
# =========================================================

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    movies["description"]
)

similarity_matrix = cosine_similarity(
    tfidf_matrix
)


# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================

def recommend_movies(movie_title, number_of_recommendations=5):

    movie_index = movies[
        movies["title"] == movie_title
    ].index[0]

    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, score in similarity_scores[
        1:number_of_recommendations + 1
    ]:
        recommendations.append(
            movies.iloc[index]["title"]
        )

    return recommendations


# =========================================================
# MOVIE SELECTION
# =========================================================

st.markdown(
    '<div class="section-title">🍿 What are you watching?</div>',
    unsafe_allow_html=True
)

st.write(
    "Choose a movie you like and our AI will find similar movies for you."
)

selected_movie = st.selectbox(
    "Choose a movie:",
    movies["title"]
)


# =========================================================
# RECOMMENDATIONS
# =========================================================

if st.button("✨ Get My Recommendations"):

    recommendations = recommend_movies(
        selected_movie
    )

    st.markdown(
        f'<div class="recommendation-title">'
        f'🍿 Because you liked '
        f'<span class="selected-movie">{selected_movie}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    for i, movie in enumerate(
        recommendations,
        start=1
    ):

        st.markdown(
            f'<div class="movie-card">'
            f'<span class="movie-number">#{i}</span>'
            f'<span class="movie-name">🎬 {movie}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="info-box">'
        '🧠 Recommendations are generated using '
        'TF-IDF Vectorization and Cosine Similarity.'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🎬 <b>CineMatch AI</b> &nbsp; | &nbsp; '
    'Built with Python, Scikit-learn & Streamlit'
    '<br><br>'
    'CodSoft Artificial Intelligence Internship '
    '• Task 4 – Recommendation System'
    '</div>',
    unsafe_allow_html=True
)