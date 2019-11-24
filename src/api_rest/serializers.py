import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from api_rest.models import UserFavouriteMovie

logger = logging.getLogger('django')


class OmdbMovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250, required=True)
    year = serializers.CharField(max_length=16, required=True)
    imdb_id = serializers.CharField(max_length=16, required=True)
    type = serializers.CharField(max_length=250, required=True)
    poster = serializers.CharField(max_length=250, required=True)


class OmdbMovieSearchResponseSerializer(serializers.Serializer):
    search = OmdbMovieSerializer(many=True, required=True)
    total_results = serializers.IntegerField()
    response = serializers.BooleanField()


class UserFavouriteMovieSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = UserFavouriteMovie
        fields = (
            'id',
            'title',
            'year',
            'imdb_id',
            'type',
            'poster',
            'user',
        )

    def create(self, validated_data):
        return UserFavouriteMovie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.year = validated_data.get("year")
        instance.imdb_id = validated_data.get("imdb_id")
        instance.type = validated_data.get("type")
        instance.poster = validated_data.get("poster")
        instance.save()
        return instance
