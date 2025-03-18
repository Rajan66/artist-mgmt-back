from django.contrib import admin
from users.models.user import CustomUser as User

admin.site.register(User)
