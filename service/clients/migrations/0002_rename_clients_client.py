# Generated by Django 4.2 on 2024-06-16 08:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Clients',
            new_name='Client',
        ),
    ]
