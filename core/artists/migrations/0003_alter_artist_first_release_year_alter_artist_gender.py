# Generated by Django 5.1.7 on 2025-03-15 10:42

import artists.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_artist_first_name_artist_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='first_release_year',
            field=models.PositiveIntegerField(default=2025, validators=[django.core.validators.MinValueValidator(1980), artists.utils.max_value_current_year]),
        ),
        migrations.AlterField(
            model_name='artist',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True),
        ),
    ]
