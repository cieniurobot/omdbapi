import logging
import json
from django.conf import settings
from retrying import retry
import requests


class OmdbProvider:
    omdb_host = settings.OMDB_HOST
    api_key = settings.OMDB_API_KEY
    search_url = f'{omdb_host}?apikey={api_key}'

    def __init__(self):
        self.logger = logging.getLogger('app')

    @retry(wait_fixed=200, stop_max_attempt_number=2)
    def search_movie(self, search: str, page=1):
        url = f'{self.search_url}&s={search}&page={page}'
        self.logger.info(f'url: {url}')
        try:
            resp = requests.get(url)
            self.logger.info(resp)
            return json.loads(resp.text)
        except ConnectionError:
            self.logger.error("Can't connect to omdb service.")
            return None
