from django.db import models


class Favourite(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('episode', 'Episode'),
    ]

    title = models.CharField(max_length=250, default='Undefined', null=False, blank=False)
    year = models.CharField(max_length=250, default='Undefined', null=False, blank=False)
    imdb_id = models.CharField(max_length=16, default='Undefined', null=False, blank=False)
    type = models.CharField(choices=TYPE_CHOICES, max_length=7, default='Undefined', null=False, blank=False)
    poster = models.CharField(max_length=250, default='Undefined', null=False, blank=False)

    def __str__(self):
        return "Title: {}: year:{}, imdb_id: {}, movie type: {}, poster: {}".format(
            self.title,
            self.year,
            self.imdb_id,
            self.type,
            self.poster
        )
