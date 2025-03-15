from users.services.user_profile import UserProfileService


def create_profile(artist, user, **kwargs):
    if user.get("role") == "ARTIST":
        # artist creation, call the service from here
        pass
    elif user.get("role") in ["ARTIST_MANAGER", "SUPER_ADMIN"]:
        user_profile_service = UserProfileService()
        user_profile_service.create(payload=artist, user_id=user.get("id"))
