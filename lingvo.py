import logging
from pprint import pprint
import requests
from private_settings import LINGVO_API_KEY

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class LingvoAPI:
    BASE_URL = 'https://developers.lingvolive.com'
    LNGSPR = {
        'en': 1033,
        'ru': 1049,
    }
    CACHE_TOKEN_FILE = 'token.txt'

    def __init__(self):
        self.s = requests.Session()
        self._token = None

    def _get_token(self):
        if self._token:
            return self._token
        try:
            with open(self.CACHE_TOKEN_FILE, 'r') as f:
                self._token = f.read()
        except FileNotFoundError:
            self._new_token()
        return self._token

    def _new_token(self):
        self.token = self.s.post(self.BASE_URL + '/api/v1.1/authenticate',
                                 headers={'Authorization': 'Basic ' + LINGVO_API_KEY}).text

    def _set_token(self, value):
        self._token = value
        with open(self.CACHE_TOKEN_FILE, 'w') as f:
            f.write(value)

    token = property(_get_token, _set_token)

    def translation(self, text):
        r = self.s.get(self.BASE_URL + '/api/v1/Translation', headers={'Authorization': 'Bearer ' + self.token},
                       params={
                           'text': text,
                           'srcLang': self.LNGSPR['en'],
                           'dstLang': self.LNGSPR['ru'],
                       })
        r.raise_for_status()
        return r.json()


def main():
    api = LingvoAPI()
    pprint(api.translation('groan'))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s():%(lineno)d: %(message)s',
                        level=logging.DEBUG)
    main()
