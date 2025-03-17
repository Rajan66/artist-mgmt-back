from django.db import DatabaseError, connection


def fetch_artists():
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM artists_artist;")
            results = c.fetchall()

            columns = []
            for col in c.description:
                columns.append(col[0])

            artist_dicts = [dict(zip(columns, row)) for row in results]

    except DatabaseError:
        raise Exception("Failed to fetch user profile")

    return artist_dicts


def fetch_artist(id):
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM artists_artist WHERE id=%s", [id])
            result = c.fetchone()

            columns = []
            for col in c.description:
                columns.append(col[0])

            artist_dict = dict(zip(columns, result))

    except DatabaseError:
        raise Exception("Failed to fetch user profile")

    return artist_dict
