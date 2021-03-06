# Generated by Django 2.2.7 on 2019-11-24 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_rest', '0002_auto_20191123_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavouriteMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Undefined', max_length=250)),
                ('year', models.CharField(default='Undefined', max_length=250)),
                ('imdb_id', models.CharField(default='Undefined', max_length=16)),
                ('type', models.CharField(choices=[('movie', 'Movie'), ('series', 'Series'), ('episode', 'Episode')], default='Undefined', max_length=7)),
                ('poster', models.CharField(default='Undefined', max_length=250)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_favourite_movie', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Favourite',
        ),
    ]
