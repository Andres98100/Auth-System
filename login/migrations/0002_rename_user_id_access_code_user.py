# Generated by Django 4.2.4 on 2023-08-21 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='access_code',
            old_name='user_id',
            new_name='user',
        ),
    ]
