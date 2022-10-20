# pylint: disable=C0103, missing-docstring
import sqlite3

conn = sqlite3.connect('/Users/damlacidamkartal/code/cidamla/data-sql-queries/data/movies.sqlite')
db = conn.cursor()

def detailed_movies(db):
    query = '''SELECT
                movies.title,
                movies.genres,
                directors.name
                FROM movies
                JOIN directors ON movies.director_id = directors.id'''
    db.execute(query)
    results = db.fetchall()
    return results

def late_released_movies(db):
    query = '''SELECT
                movies.title
                FROM movies
                JOIN directors ON movies.director_id = directors.id
                WHERE directors.death_year < movies.start_year'''
    db.execute(query)
    results = db.fetchall()
    sol_list = []
    for i in results:
        sol_list.append(i[0])
    return sol_list

def stats_on(db, genre_name):
    query = f"SELECT COUNT(*), ROUND(AVG(minutes), 2), genres FROM movies WHERE genres = '{genre_name}'"
    db.execute(query)
    results = db.fetchall()
    sol_dict = {"genre": "",
                "number_of_movies": 0,
                "avg_length": 0
    }
    sol_dict["genre"] = results[0][2]
    sol_dict["number_of_movies"] = results[0][0]
    sol_dict["avg_length"] = results[0][1]
    return sol_dict

def top_five_directors_for(db, genre_name):
    query = """
        SELECT
            directors.name,
            COUNT(*) movie_count
        FROM movies
        JOIN directors ON movies.director_id = directors.id
        WHERE movies.genres = ?
        GROUP BY directors.name
        ORDER BY movie_count DESC, directors.name
        LIMIT 5
    """
    db.execute(query, (genre_name,))
    results = db.fetchall()
    return results

def movie_duration_buckets(db):
    query = """
        SELECT
            (minutes / 30 + 1)*30 time_range,
            COUNT(*)
        FROM movies
        WHERE minutes IS NOT NULL
        GROUP BY time_range
    """
    return db.execute(query).fetchall()


def top_five_youngest_newly_directors(db):
    query = """
        SELECT
            directors.name,
            movies.start_year - directors.birth_year age
        FROM directors
        JOIN movies ON directors.id = movies.director_id
        GROUP BY directors.name
        HAVING age IS NOT NULL
        ORDER BY age
        LIMIT 5
    """
    db.execute(query)
    directors = db.fetchall()
    return directors
