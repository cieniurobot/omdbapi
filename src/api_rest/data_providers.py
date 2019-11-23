import logging
import json
from django.conf import settings
from retrying import retry
import requests
from api_rest.serializers import OmdbMovieSearchResponseSerializer


class OmdbProvider:
    omdb_host = settings.OMDB_HOST
    api_key = settings.OMDB_API_KEY
    search_url = f'{omdb_host}?apikey={api_key}'
    not_found_message = 'Movie not found!'

    def __init__(self):
        self.logger = logging.getLogger('django')

    def map_movies(self, movies):
        mapped_movies = []
        for movie in movies:
            mapped_movies.append({
                "title": movie.pop('Title', None),
                "year": movie.pop('Year', None),
                "imdb_id": movie.pop('imdbID', None),
                "type": movie.pop('Type', None),
                "poster": movie.pop('Poster', None),
            })

        return mapped_movies

    def map_response(self, response):
        response['search'] = self.map_movies(response.pop('Search', []))
        response['total_results'] = int(response.pop('totalResults', 0))
        res = response.pop('Response', 'False')
        response['response'] = True if res == 'True' else False
        return response

    @retry(wait_fixed=200, stop_max_attempt_number=2)
    def search_movie(self, search: str, page=1):
        url = f'{self.search_url}&s={search}&page={page}'
        try:
            resp = requests.get(url)
            resp_obj = json.loads(resp.text)
            err = resp_obj.get('Error', None)

            if err == self.not_found_message:
                return {
                    "message": resp_obj['Error']
                }

            if err:
                return None

            mapped_resp = self.map_response(resp_obj)
            serializer = OmdbMovieSearchResponseSerializer(data=mapped_resp)
            if not serializer.is_valid():
                self.logger.error(f'Serialization error! Errors: {json.dumps(serializer.errors)}')
                return None

            return serializer.validated_data
        except ConnectionError:
            self.logger.error("Can't connect to omdb service.")
            return None
