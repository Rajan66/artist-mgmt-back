from django.db import models
from users.models.user import CustomUser

from core.base.models import Profile


class UserProfile(Profile):
    user = models.OneToOneField(
        CustomUser,
        related_name="user",
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )  # add validation

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        db_table = "users_user_profile"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.user.email
