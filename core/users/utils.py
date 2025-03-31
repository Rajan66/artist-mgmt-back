from artists.services import ArtistService
from users.services.user_profile import UserProfileService


def create_profile(profile, user, **kwargs):
    if user.get("role") == "artist":
        artist_service = ArtistService()
        response = artist_service.create(payload=profile, user_id=user.get("id"))
        if response.status_code == 201:
            return True
        else:
            return False
    elif user.get("role") in ["artist_manager", "super_admin"]:
        user_profile_service = UserProfileService()
        response = user_profile_service.create(payload=profile, user_id=user.get("id"))
        if response.status_code == 201:
            return True
        else:
            return False
