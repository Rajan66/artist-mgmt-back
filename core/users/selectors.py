from django.db import DatabaseError, connection
from rest_framework import status

from core.utils.exceptions import CustomAPIException


def fetch_user(profile):
    try:
        with connection.cursor() as c:
            user_id = profile.get("user_id")
            c.execute("SELECT * FROM users_customuser WHERE id=%s", [user_id])
            result = c.fetchone()

            if not result:
                raise ValueError("Invalid user ID")

            columns = [col[0] for col in c.description]
            user_dicts = dict(zip(columns, result))

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

    return user_dicts


def fetch_user_profiles():
    try:
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_user_profile")
            results = c.fetchall()

            columns = [col[0] for col in c.description]

            user_dicts = [dict(zip(columns, row)) for row in results]

    except DatabaseError:
        raise Exception("Failed to fetch users")
    except Exception:
        raise Exception("Something went wrong...")

    return user_dicts
