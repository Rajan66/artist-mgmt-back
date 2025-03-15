import uuid

from django.db import connection
from django.utils import timezone
from rest_framework import status

from core.base.choices import GenderChoices
from core.utils.response import success_response


class UserProfileService:
    def get_profiles(self):
        pass

    def get_profile(self):
        pass

    def create(self, payload, user_id):
        try:
            payload = payload or {}
            id = payload.get("id") if payload.get("id") else uuid.uuid4()
            first_name = payload.get("first_name") if payload.get("first_name") else ""
            last_name = payload.get("last_name") if payload.get("last_name") else ""
            dob = payload.get("dob") if payload.get("dob") else None
            gender = (
                payload.get("gender") if payload.get("gender") else GenderChoices.MALE
            )
            address = payload.get("address") if payload.get("address") else ""
            phone = payload.get("phone") if payload.get("phone") else ""
            created_at = (
                payload.get("created_at")
                if payload.get("created_at")
                else timezone.now()
            )
            updated_at = timezone.now()
            print("User profile creation is running.........")

            with connection.cursor() as c:
                c.execute(
                    """INSERT INTO users_user_profile (id, first_name, last_name, dob, gender, address, phone, created_at, updated_at, user_id)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        id,
                        first_name,
                        last_name,
                        dob,
                        gender,
                        address,
                        phone,
                        created_at,
                        updated_at,
                        user_id,
                    ],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("User profile creation failed")

                print("Profile rows==========>", result)
                columns = []
                for col in c.description:
                    columns.append(col[0])

            profile_dicts = dict(zip(columns, result))
            print("Profile dict ==============>", profile_dicts)

            return success_response(
                "something is getting sent..",
                message="User profile created succesfully",
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)

    def update(self):
        pass

    def delete(self):
        pass
