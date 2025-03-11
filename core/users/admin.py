from django.contrib import admin

from users.models import CustomUser as User

admin.site.register(User)
