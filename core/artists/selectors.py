from django.db import DatabaseError, connection
from rest_framework import status

from core.utils.exceptions import CustomAPIException


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

            if not result:
                raise ValueError("Invalid artist ID")
            columns = []
            for col in c.description:
                columns.append(col[0])

            artist_dict = dict(zip(columns, result))

    except DatabaseError as e:
        raise CustomAPIException(
            error=str(e),
            detail="Database error occurred while fetching artist",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as e:
        raise CustomAPIException(
            error="Invalid ID",
            detail=str(e),
            code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        raise CustomAPIException(
            error="Unexpected Error",
            detail=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return artist_dict


def check_artist(id):
    try:
        with connection.cursor() as c:
            c.execute("SELECT name FROM artists_artist WHERE id=%s", [id])
            result = c.fetchone()

            if not result:
                raise ValueError("Invalid artist ID")

    except ValueError as e:
        raise CustomAPIException(
            error=str(e),
            detail=str(e),
            code=status.HTTP_400_BAD_REQUEST,
        )
