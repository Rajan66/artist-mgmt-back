# Generated by Django 5.1.7 on 2025-03-27 03:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("artists", "0004_alter_artist_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="artist",
            name="manager",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="manager",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]
