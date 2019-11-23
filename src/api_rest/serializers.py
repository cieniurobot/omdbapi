import logging
from rest_framework import serializers

from api_rest.models import Favourite

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


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def create(self, validated_data):
        favourite = Favourite()
        favourite.title = validated_data.get('title')
        favourite.year = validated_data.get('year')
        favourite.imdb_id = validated_data.get('imdb_id')
        favourite.type = validated_data.get('type')
        favourite.poster = validated_data.get('poster')
        favourite.save()
        return favourite

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.year = validated_data.get("year")
        instance.imdb_id = validated_data.get("imdb_id")
        instance.type = validated_data.get("type")
        instance.poster = validated_data.get("poster")
        instance.save()
        return instance
