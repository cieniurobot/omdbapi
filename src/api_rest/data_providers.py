import logging
import json
from django.conf import settings
from retrying import retry
import requests


class OmdbProvider:
    omdb_host = settings.OMDB_HOST
    api_key = settings.OMDB_API_KEY
    search_url = f'{omdb_host}?apikey={api_key}&s='

    def __init__(self):
        self.logger = logging.getLogger('app')

    @retry(wait_fixed=200, stop_max_attempt_number=2)
    def search_movie(self, q: str):
        url = f'{self.search_url}{q}'

        try:
            resp = requests.get(url)
            self.logger.info(resp)
            return json.loads(resp.text)
        except ConnectionError:
            self.logger.error("Can't connect to omdb service.")
            return None
        except Exception as e:
            print(e)
            raise
