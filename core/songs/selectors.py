from albums.models.album import Album
from albums.selectors import check_album
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
                album = Album.objects.filter(id=song["album_id"]).first()
                print(album)
                song["album"] = album

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
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM songs_song WHERE id=%s", [id])
            result = c.fetchone()

            if not result:
                raise ValueError("Invalid song ID")

            columns = [col[0] for col in c.description]

            songs_dict = dict(zip(columns, result))
            songs_dict["album"] = songs_dict["album_id"]

    except ValueError as e:
        raise CustomAPIException(
            error=str(e),
            detail="Invalid ID",
            code=status.HTTP_400_BAD_REQUEST,
        )
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

    return songs_dict


def fetch_artist_songs(artist_id):
    try:
        with connection.cursor() as c:
            c.execute(
                """
                SELECT s.id,s.title, s.genre, s.release_date,s.created_at,s.updated_at, a.id AS album_id 
                FROM songs_song s
                JOIN albums_album a ON a.id = s.album_id
                JOIN artists_artist ar ON ar.id = a.artist_id
                WHERE ar.id=%s;
                """,
                [artist_id],
            )
            results = c.fetchall()

            if not results:
                return []

            columns = [col[0] for col in c.description]

            songs_dicts = [dict(zip(columns, row)) for row in results]
            album_ids = {song["album_id"] for song in songs_dicts}

            # Fetch all required albums in a single query
            albums = {
                album.id: album for album in Album.objects.filter(id__in=album_ids)
            }

            # Assign albums to songs using dictionary lookup (O(1) operation)
            for song in songs_dicts:
                song["album"] = albums.get(song["album_id"]).id
                song["cover_image"] = albums.get(song["album_id"]).cover_image
                print(song)

            return songs_dicts

    except DatabaseError as e:
        raise CustomAPIException(
            error=str(e),
            detail="Database error occurred while fetching songs",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        raise CustomAPIException(
            error=str(e),
            detail=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def fetch_album_songs(album_id):
    try:
        with connection.cursor() as c:
            check_album(album_id)
            c.execute("SELECT * FROM songs_song WHERE album_id=%s;", [album_id])
            results = c.fetchall()
            if not results:
                return []

            columns = [col[0] for col in c.description]

            songs_dicts = [dict(zip(columns, row)) for row in results]
            for song in songs_dicts:
                song["album"] = song["album_id"]

        return songs_dicts

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
