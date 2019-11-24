from django.contrib.auth.models import User
from django.db import models


class UserFavouriteMovie(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('episode', 'Episode'),
    ]

    title = models.CharField(max_length=250, null=False, blank=False)
    year = models.CharField(max_length=250, null=False, blank=False)
    imdb_id = models.CharField(max_length=16, null=False, blank=False)
    type = models.CharField(choices=TYPE_CHOICES, max_length=7, null=False, blank=False)
    poster = models.CharField(max_length=250, null=False, blank=False)
    user = models.ForeignKey(
        User,
        related_name='user_favourite_movie',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "Title: {}: year:{}, imdb_id: {}, movie type: {}, poster: {}".format(
            self.title,
            self.year,
            self.imdb_id,
            self.type,
            self.poster
        )
