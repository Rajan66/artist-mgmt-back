# Generated by Django 5.1.7 on 2025-03-14 09:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('album_name', models.CharField(max_length=255)),
                ('genre', models.CharField(choices=[('rnb', 'Rnb'), ('country', 'Country'), ('classic', 'Classic'), ('rock', 'Rock'), ('jazz', 'Jazz')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
