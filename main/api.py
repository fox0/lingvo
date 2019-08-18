import logging
import time
import requests

log = logging.getLogger(__name__)

BASE_URL = 'https://developers.lingvolive.com'
LNGSPR = {
    'en': 1033,
    'ru': 1049,
}
CACHE_TOKEN_FILE = 'token.txt'


class LingvoAPI:
    def __init__(self, api_key):
        # https://developers.lingvolive.com/en-us/Applications
        self.API_KEY = api_key
        self.s = requests.Session()
        self._token = None

    def translation(self, text, src='en', dest='ru'):
        return self._api('/api/v1/Translation', text, src, dest)

    def minicard(self, text):
        """
        {'Heading': 'spend',
         'SeeAlso': [],
         'SourceLanguage': 1033,
         'TargetLanguage': 1049,
         'Translation': {'DictionaryName': 'LingvoUniversal (En-Ru)',
                         'Heading': 'spend',
                         'OriginalWord': '',
                         'SoundName': 'spend.wav',
                         'Translation': 'тратить, расходовать',
                         'Type': 1}}
        """
        return self._api('/api/v1/Minicard', text)

    def _api(self, url, text, src='en', dest='ru'):
        for _ in range(3):
            r = self.s.get(BASE_URL + url, headers={'Authorization': 'Bearer ' + self.token},
                           params=dict(text=text, srcLang=LNGSPR[src], dstLang=LNGSPR[dest]))
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 401:
                self._new_token()
                continue
            elif r.status_code == 404:
                return None
            elif r.status_code == 429:
                time.sleep(5)
                continue
        raise ValueError(r.status_code)

    def _get_token(self):
        if self._token:
            return self._token
        try:
            with open(CACHE_TOKEN_FILE, 'r') as f:
                self._token = f.read()
        except FileNotFoundError:
            self._new_token()
        return self._token

    def _new_token(self):
        log.debug('new token')
        self.token = self.s.post(BASE_URL + '/api/v1.1/authenticate',
                                 headers={'Authorization': 'Basic ' + self.API_KEY}).text

    def _set_token(self, value):
        self._token = value
        with open(CACHE_TOKEN_FILE, 'w') as f:
            f.write(value)

    token = property(_get_token, _set_token)
