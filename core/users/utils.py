from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser as User
from users.services.user_profile import UserProfileService


@receiver(post_save, sender=User)
def create_profile(sender, artist, created, user, **kwargs):
    if created:
        if user.get("role") == "ARTIST":
            # artist creation, call the service from here
            pass
        elif user.get("role") in ["ARTIST_MANAGER", "SUPER_ADMIN"]:
            user_profile_service = UserProfileService()
            user_profile_service.create(payload=artist, user_id=user.get("id"))
