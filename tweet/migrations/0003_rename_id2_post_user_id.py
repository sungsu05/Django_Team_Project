# Generated by Django 4.2 on 2023-04-11 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='id2',
            new_name='user_id',
        ),
    ]
