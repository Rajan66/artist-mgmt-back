from django.db import DatabaseError, connection
from rest_framework import status

from core.utils.exceptions import CustomAPIException


def fetch_songs():
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM songs_song;")
            results = c.fetchall()
            if not results:
                return []

            columns = [col[0] for col in c.description]

            songs_dicts = [dict(zip(columns, row)) for row in results]
            for song in songs_dicts:
                song["album"] = song["album_id"]

    except DatabaseError as e:
        raise CustomAPIException(
            error=str(e),
            detail="Database error occurred while fetching albums",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        raise CustomAPIException(
            error=str(e),
            detail="Failed to fetch songs",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return songs_dicts


def fetch_song(id):
    pass


def fetch_artist_songs(artist_id):
    pass
