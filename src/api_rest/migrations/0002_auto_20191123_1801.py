# Generated by Django 2.2.7 on 2019-11-23 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourite',
            old_name='imdbId',
            new_name='imdb_id',
        ),
    ]
