import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Movie dataset
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


# Convert movie descriptions into numerical features
vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(movies["description"])


# Calculate similarity between movies
similarity_matrix = cosine_similarity(tfidf_matrix)


# Recommendation function
def recommend_movies(movie_title, number_of_recommendations=5):

    if movie_title not in movies["title"].values:
        return []

    movie_index = movies[movies["title"] == movie_title].index[0]

    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for index, score in similarity_scores[1:number_of_recommendations + 1]:
        recommended_movies.append(movies.iloc[index]["title"])

    return recommended_movies


# Test the recommendation system
if __name__ == "__main__":

    selected_movie = "Inception"

    recommendations = recommend_movies(
        selected_movie
    )

    print("Movie Recommendations for:", selected_movie)
    print()

    for movie in recommendations:
        print("-", movie)