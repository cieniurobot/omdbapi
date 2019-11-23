import json
from django.test import TestCase
from unittest import mock
from .data_providers import OmdbProvider


def mocked_search_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.text = json.dumps(data)
            self.status_code = status_code

    movie_exists_response = {
        "Search": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "Year": "1977",
                "imdbID": "tt0076759",
                "Type": "movie",
                "Poster": "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"
            }
        ],
        "Response": "True",
        "totalResults": "1"
    }

    movie_not_found_response = {
        "Response": "False",
        "Error": "Movie not found!"
    }

    if args[0] == f'{OmdbProvider.search_url}&s=star wars&page=1':
        return MockResponse(movie_exists_response, 200)
    elif args[0] == f'{OmdbProvider.search_url}&s=bladerunner&page=1':
        return MockResponse(movie_not_found_response, 200)

    return MockResponse(None, 404)


class OmdbProviderTestCase(TestCase):

    @mock.patch('requests.get', side_effect=mocked_search_requests_get)
    def test_search_movie(self, mock_get):
        found_movie_expected_response = {
            "Search": [
                {
                    "Title": "Star Wars: Episode IV - A New Hope",
                    "Year": "1977",
                    "imdbID": "tt0076759",
                    "Type": "movie",
                    "Poster": "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"
                }
            ],
            "Response": "True",
            "totalResults": "1"
        }
        not_found_movie_expected_response = {
            "Response": "False",
            "Error": "Movie not found!"
        }

        omdb_provider = OmdbProvider()

        found_movie_response = omdb_provider.search_movie('star wars')
        self.assertEqual(found_movie_response, found_movie_expected_response)

        not_found_movie_response = omdb_provider.search_movie('bladerunner')
        self.assertEqual(not_found_movie_response, not_found_movie_expected_response)

        self.assertIn(mock.call(f'{OmdbProvider.search_url}&s=star wars&page=1'), mock_get.call_args_list)
        self.assertEqual(len(mock_get.call_args_list), 2)
