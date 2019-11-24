import logging
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api_rest.data_providers import OmdbProvider
from api_rest.models import UserFavouriteMovie
from api_rest.serializers import UserFavouriteMovieSerializer

logger = logging.getLogger('django')


class Index(APIView):
    """ OMDb API """

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome in OMDb API."})


class MovieSearchView(APIView):
    """
        Search view
    """
    permission_classes = (IsAuthenticated,)
    omdb_provider = OmdbProvider()

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        if search is None:
            return Response(
                {"message": "Please type search value(search=movie name)!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        page = kwargs.get('page', 1)
        movie_data = self.omdb_provider.search_movie(search, page)
        if movie_data is None:
            return Response(
                {"message": "Something went wrong!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if movie_data.get('message', None) == "Movie not found!":
            return Response(
                {
                    "message": "Movie not found!"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(movie_data)


class MyUserFavouriteMovieCreateListView(APIView):
    """ My UserFavouriteMovie create, list."""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = UserFavouriteMovie.objects.filter(user=request.user)
        serializer = UserFavouriteMovieSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = UserFavouriteMovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyUserFavouriteMovieDeleteView(APIView):
    """ My UserFavouriteMovie delete."""
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, *args, **kwargs):
        fav_movie = get_object_or_404(UserFavouriteMovie, pk=self.kwargs.get('pk'))
        if not fav_movie:
            return Response(
                {
                    "message": "User favourite movie not found!"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if fav_movie.user.id != request.user.id:
            return Response(
                {
                    "message": "You don't have permissions to remove that favourite movie!"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        fav_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
