# Generated by Django 3.2.9 on 2023-02-05 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userdata_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='profile_photo',
        ),
    ]
