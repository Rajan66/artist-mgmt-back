# Generated by Django 5.1.7 on 2025-03-14 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_is_active_customuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_removed',
        ),
    ]
