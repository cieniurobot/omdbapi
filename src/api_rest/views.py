import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api_rest.data_providers import OmdbProvider

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
        logger.info('search:')
        logger.info(search)
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
