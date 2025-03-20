from flask import Blueprint, render_template
import mysql.connector

views = Blueprint('views', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123",
        database="project"
    )

@views.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries for easier access

    # Fetch movies
    cursor.execute("SELECT movie_id, movie_title, release_year FROM movies")
    movies = cursor.fetchall()

    # Fetch categories
    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()

    # Fetch movie categories directly from the table (it already contains movie_title and category_name)
    cursor.execute("SELECT movie_id, category_id, movie_title, category_name FROM movie_categories")
    movie_categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "home.html",
        movies=movies,
        categories=categories,
        movie_categories=movie_categories
    )
