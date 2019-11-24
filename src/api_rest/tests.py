import json
from unittest import mock
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User

from api_rest.models import UserFavouriteMovie
from api_rest.views import MovieSearchView, MyUserFavouriteMovieCreateListView
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

    movie_exists_page2_response = {
        "Search": [
            {
                "Title": "Robot Chicken: Star Wars III",
                "Year": "2010",
                "imdbID": "tt1691338",
                "Type": "movie",
                "Poster": "https://m.media-amazon.com/images/M/MV5BMjAyNTYzODM3OF5BMl5BanBnXkFtZTcwMTY4ODM4NA@@._V1_SX300.jpg"
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
    if args[0] == f'{OmdbProvider.search_url}&s=star wars&page=2':
        return MockResponse(movie_exists_page2_response, 200)
    elif args[0] == f'{OmdbProvider.search_url}&s=bladerunner&page=1':
        return MockResponse(movie_not_found_response, 200)

    return MockResponse(None, 404)


class OmdbProviderTestCase(TestCase):

    @mock.patch('requests.get', side_effect=mocked_search_requests_get)
    def test_search_movie(self, mock_get):
        found_movie_expected_response = {
            "search": [
                {
                    "title": "Star Wars: Episode IV - A New Hope",
                    "year": "1977",
                    "imdb_id": "tt0076759",
                    "type": "movie",
                    "poster": "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"
                }
            ],
            "response": "True",
            "total_results": 1,
            "page": 1,
        }
        not_found_movie_expected_response = {
            "message": "Movie not found!"
        }
        found_movie_expected_response_page2 = {
            "search": [
                {
                    "title": "Robot Chicken: Star Wars III",
                    "year": "2010",
                    "imdb_id": "tt1691338",
                    "type": "movie",
                    "poster": "https://m.media-amazon.com/images/M/MV5BMjAyNTYzODM3OF5BMl5BanBnXkFtZTcwMTY4ODM4NA@@._V1_SX300.jpg"
                }
            ],
            "response": "True",
            "total_results": 190900909,
            "page": 2,
        }
        omdb_provider = OmdbProvider()

        found_movie_response = omdb_provider.search_movie('star wars', 1)
        self.assertEqual(json.dumps(found_movie_response['search']),
                         json.dumps(found_movie_expected_response['search']))

        found_movie_page2_response = omdb_provider.search_movie('star wars', 2)
        self.assertEqual(json.dumps(found_movie_page2_response['search']),
                         json.dumps(found_movie_expected_response_page2['search']))

        not_found_movie_response = omdb_provider.search_movie('bladerunner')
        self.assertEqual(not_found_movie_response, not_found_movie_expected_response)

        self.assertIn(mock.call(f'{OmdbProvider.search_url}&s=star wars&page=1'), mock_get.call_args_list)
        self.assertIn(mock.call(f'{OmdbProvider.search_url}&s=star wars&page=2'), mock_get.call_args_list)
        self.assertIn(mock.call(f'{OmdbProvider.search_url}&s=bladerunner&page=1'), mock_get.call_args_list)
        self.assertEqual(len(mock_get.call_args_list), 3)


class MovieSearchViewAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='tester', email='test@test.pl', password='top_secret')

    @mock.patch('requests.get', side_effect=mocked_search_requests_get)
    def test_get(self, mock_get):
        request_found = self.factory.get('/api/v1/movie', {
            "search": "star wars",
            "page": 1
        })
        request_found.user = self.user

        response = MovieSearchView.as_view()(request_found, '')
        self.assertEqual(response.status_code, 200)

        request_not_found = self.factory.get('/api/v1/movie', {
            "search": "bladerunner",
            "page": 1
        })
        request_not_found.user = self.user

        response = MovieSearchView.as_view()(request_not_found, '')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message": "Movie not found!"})

        bad_request = self.factory.get('/api/v1/movie', {
            "page": 1
        })
        bad_request.user = self.user

        response = MovieSearchView.as_view()(bad_request, None)
        self.assertEqual(response.status_code, 400)

        self.assertIn(mock.call(f'{OmdbProvider.search_url}&s=star wars&page=1'), mock_get.call_args_list)
        self.assertEqual(len(mock_get.call_args_list), 2)


class MyUserFavouriteMovieCreateListAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='tester', email='test@test.pl', password='top_secret')
        self.another_user = User.objects.create_user(username='another', email='test@test.pl', password='top_secret')

    def test_get(self):
        fav_movie_data = {
            "title": "test",
            "year": "1980",
            "imdb_id": "tt0080684",
            "type": "movie",
            "poster": "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "user": self.user
        }
        UserFavouriteMovie.objects.create(**fav_movie_data)
        request_found = self.factory.get('/api/v1/my-user-favourite-movie')
        request_found.user = self.user
        response_found = MyUserFavouriteMovieCreateListView.as_view()(request_found, '')
        self.assertEqual(response_found.status_code, 200)
        self.assertEqual(response_found.data[0]['title'], fav_movie_data['title'])
        self.assertEqual(response_found.data[0]['year'], fav_movie_data['year'])
        self.assertEqual(response_found.data[0]['imdb_id'], fav_movie_data['imdb_id'])
        self.assertEqual(response_found.data[0]['type'], fav_movie_data['type'])
        self.assertEqual(response_found.data[0]['poster'], fav_movie_data['poster'])
        self.assertEqual(response_found.data[0]['user'], self.user.id)

        request_bad_user = self.factory.get('/api/v1/my-user-favourite-movie')
        request_bad_user.user = self.another_user

        request_bad_user = MyUserFavouriteMovieCreateListView.as_view()(request_bad_user, '')
        self.assertEqual(request_bad_user.status_code, 200)
        self.assertEqual(request_bad_user.data, [])

    def test_post(self):
        fav_movie_data = {
            "title": "test",
            "year": "1980",
            "imdb_id": "tt0080684",
            "type": "movie",
            "poster": "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "user": self.user.id
        }

        request_not_auth = self.factory.post('/api/v1/my-user-favourite-movie/', fav_movie_data, format='json')
        response_not_auth = MyUserFavouriteMovieCreateListView.as_view()(request_not_auth)
        self.assertEqual(response_not_auth.status_code, 401)

        request_bad = self.factory.post('/api/v1/my-user-favourite-movie/', {}, format='json')
        request_bad.user = self.user
        response_bad = MyUserFavouriteMovieCreateListView.as_view()(request_bad)
        self.assertEqual(response_bad.status_code, 400)

        request_success = self.factory.post('/api/v1/my-user-favourite-movie/', fav_movie_data, format='json')
        request_success.user = self.user
        response_success = MyUserFavouriteMovieCreateListView.as_view()(request_success)
        self.assertEqual(response_success.status_code, 201)
        self.assertEqual(response_success.data['title'], fav_movie_data['title'])
        self.assertEqual(response_success.data['year'], fav_movie_data['year'])
        self.assertEqual(response_success.data['imdb_id'], fav_movie_data['imdb_id'])
        self.assertEqual(response_success.data['imdb_id'], fav_movie_data['imdb_id'])
        self.assertEqual(response_success.data['type'], fav_movie_data['type'])
        self.assertEqual(response_success.data['poster'], fav_movie_data['poster'])
        self.assertEqual(response_success.data['user'], fav_movie_data['user'])
