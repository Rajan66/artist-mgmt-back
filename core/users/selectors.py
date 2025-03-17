from django.db import DatabaseError, connection


def fetch_user(profile):
    try:
        with connection.cursor() as c:
            user_id = profile.get("user_id")
            c.execute("SELECT * FROM users_customuser WHERE id=%s", [user_id])
            result = c.fetchone()

            if not result:
                raise Exception("Invalid user ID")  # TODO Custom exception

            columns = [col[0] for col in c.description]
            user_dicts = dict(zip(columns, result))

    except DatabaseError:
        raise Exception("Failed to fetch user")
    except Exception:
        raise Exception("Something went wrong...")

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
