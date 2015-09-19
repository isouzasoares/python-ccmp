# -*- coding: utf-8 -*-

import requests

BASE_URL = "https://login.eccmp.com/services2/api/"
TOKEN_URL = "https://login.eccmp.com/services2/authorization/oAuth2/Token"


class OAuthCcmp(requests.auth.AuthBase):

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.access_token
        return r


class Ccmp(object):

    def __init__(self, username, password, grant_type="password",
                 base_url=None, token_url=None):
        """
        """
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.base_url = base_url or BASE_URL
        self.token_url = token_url or TOKEN_URL
        self.token = None
        self.refresh_token = None
        self.expires = None
        self.token_type = None
        self.session = None

    def get_session(self):
        """
        """
        data = {}
        data['username'] = self.username
        data['password'] = self.password
        data['grant_type'] = self.grant_type
        try:
            result = requests.post(self.token_url, data)
            result = result.json()
        except:
            return result
        self.token = result['access_token']
        self.expires = result['expires_in']
        self.token_type = result['token_type']
        self.refresh_token = result['refresh_token']
        auth = OAuthCcmp(self.token)
        self.session = requests.Session()
        self.session.auth = auth
        return self

    def get(self, method, **kwargs):
        """
        """
        url = self.base_url + method
        return self.session.get(url, params=kwargs).json()

    def post(self, method, data=None, json=None, **kwargs):
        """
        """
        url = self.base_url + method
        return self.session.post(url, data=kwargs, json=json, **kwargs)
