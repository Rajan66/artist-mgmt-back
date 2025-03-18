from django.db import DatabaseError, connection
from rest_framework import status

from core.utils.exceptions import CustomAPIException


def fetch_albums():
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM albums_album")
            results = c.fetchall()

            columns = []
            for col in c.description:
                columns.append(col[0])

            albums_dicts = [dict(zip(columns, row)) for row in results]

    except DatabaseError as e:
        raise CustomAPIException(
            error_type=str(e),
            detail="Database error occurred while fetching albums",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        raise CustomAPIException(
            error_type=str(e),
            detail="Failed to fetch albums",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return albums_dicts


# artist gets to add a new album not manager
def fetch_user_albums(self, id):
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM albums_song where artist_id=%s", [id])

    except Exception as e:
        return CustomAPIException(
            error_type=str(e),
            detail="Failed to retrieve albums",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def fetch_album(id):
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM albums_album where id=%s", [id])

            result = c.fetchone()

            if not result:
                raise ValueError("Invalid album ID")

            columns = []
            for col in c.description:
                columns.append(col[0])

            album_dict = dict(zip(columns, result))

    except DatabaseError as e:
        raise CustomAPIException(
            error_type=str(e),
            detail="Database error occurred while fetching album",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as e:  # Catch invalid ID specifically
        raise CustomAPIException(
            error_type="Invalid ID",
            detail=str(e),
            code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        raise CustomAPIException(
            error_type="Unexpected Error",
            detail=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return album_dict
