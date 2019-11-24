# Generated by Django 2.2.7 on 2019-11-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_auto_20191124_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavouritemovie',
            name='imdb_id',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='userfavouritemovie',
            name='poster',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='userfavouritemovie',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='userfavouritemovie',
            name='type',
            field=models.CharField(choices=[('movie', 'Movie'), ('series', 'Series'), ('episode', 'Episode')], max_length=7),
        ),
        migrations.AlterField(
            model_name='userfavouritemovie',
            name='year',
            field=models.CharField(max_length=250),
        ),
    ]
