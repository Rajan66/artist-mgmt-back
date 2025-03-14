# Generated by Django 5.1.7 on 2025-03-14 08:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(unique=True, verbose_name='artist name')),
                ('first_release_year', models.IntegerField(blank=True)),
                ('no_of_albums_released', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Artist Profile',
                'verbose_name_plural': 'Artist Profiles',
            },
        ),
    ]
