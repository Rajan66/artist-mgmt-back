from django.db import connection
from users.serializers import UserOutputSerializer


def get_user(profile):
    with connection.cursor() as c:
        user_id = profile.get("user_id")
        c.execute("SELECT * FROM users_customuser WHERE id=%s", [user_id])
        result = c.fetchone()

        if not result:
            raise Exception("Invalid user ID")  # TODO Custom exception

        columns = [col[0] for col in c.description]
        user_dicts = dict(zip(columns, result))
        serializer = UserOutputSerializer(user_dicts)
        profile["user"] = serializer.data

    return profile
