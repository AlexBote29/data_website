import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint('auth', __name__)

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123",
        database="project"
    )

# ------------------ INSERT Route ------------------
@auth.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        category_name = request.form.get('category_name')
        movie_id = request.form.get('movie_id')
        movie_title = request.form.get('movie_title')
        release_year = request.form.get('release_year')
        mc_category_id = request.form.get('mc_category_id')
        mc_movie_id = request.form.get('mc_movie_id')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if mc_category_id and mc_movie_id:
                cursor.execute(
                    "INSERT INTO movie_categories (movie_id, category_id, movie_title, category_name) VALUES (%s, %s, %s, %s)",
                    (mc_movie_id, mc_category_id, movie_title, category_name)
                )

            if category_id and category_name:
                cursor.execute(
                    "INSERT INTO categories (category_id, category_name) VALUES (%s, %s)",
                    (category_id, category_name)
                )

            if movie_id and movie_title and release_year:
                cursor.execute(
                    "INSERT INTO movies (movie_id, movie_title, release_year) VALUES (%s, %s, %s)",
                    (movie_id, movie_title, release_year)
                )

            conn.commit()
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('auth.insert'))

    return render_template("insert.html")

# ------------------ VIEW Route ------------------
@auth.route('/view', methods=['GET'])
def view():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT movie_id, movie_title, release_year FROM movies")
    movies = cursor.fetchall()

    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT movie_id, category_id, movie_title, category_name FROM movie_categories")
    movie_categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "view.html",
        movies=movies,
        categories=categories,
        movie_categories=movie_categories
    )

# ------------------ MODIFY Route ------------------
@auth.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        old_category_id = request.form.get('old_category_id')
        new_category_id = request.form.get('new_category_id')
        old_category_name = request.form.get('old_category_name')
        new_category_name = request.form.get('new_category_name')
        old_movie_id = request.form.get('old_movie_id')
        new_movie_id = request.form.get('new_movie_id')
        old_movie_title = request.form.get('old_movie_title')
        new_movie_title = request.form.get('new_movie_title')
        old_release_year = request.form.get('old_release_year')
        new_release_year = request.form.get('new_release_year')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if old_category_id and new_category_id:
                cursor.execute("UPDATE categories SET category_id=%s WHERE category_id=%s", (new_category_id, old_category_id))
            if old_category_name and new_category_name:
                cursor.execute("UPDATE categories SET category_name=%s WHERE category_name=%s", (new_category_name, old_category_name))
            if old_movie_id and new_movie_id:
                cursor.execute("UPDATE movies SET movie_id=%s WHERE movie_id=%s", (new_movie_id, old_movie_id))
            if old_movie_title and new_movie_title:
                cursor.execute("UPDATE movies SET movie_title=%s WHERE movie_title=%s", (new_movie_title, old_movie_title))
            if old_release_year and new_release_year:
                cursor.execute("UPDATE movies SET release_year=%s WHERE release_year=%s", (new_release_year, old_release_year))

            conn.commit()
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('auth.modify'))

    return render_template("modify.html")

# ------------------ DELETE Route ------------------
@auth.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        movie_title = request.form.get('movie_title')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if category_name:
                cursor.execute("DELETE FROM categories WHERE category_name=%s", (category_name,))
            if movie_title:
                cursor.execute("DELETE FROM movies WHERE movie_title=%s", (movie_title,))

            conn.commit()
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('auth.delete'))

    return render_template("delete.html")
