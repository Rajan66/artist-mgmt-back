# Generated by Django 5.1.7 on 2025-03-18 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='type',
            new_name='album_type',
        ),
    ]
