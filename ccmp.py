# -*- coding: utf-8 -*-

import requests
from requests.auth import AuthBase

BASE_URL = "https://login.eccmp.com/"
TOKEN_URL = BASE_URL + "services2/authorization/oAuth2/Token"


class OAuthCcmp(AuthBase):

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.access_token
        return r


class Ccmp(object):

    def __init__(self, username, password, grant_type,
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
        self.auth = None
        self.get_token()

    def get_token(self):
        """
        """
        data = {}
        data['username'] = self.username
        data['password'] = self.password
        data['grant_type'] = self.grant_type
        result = requests.post(self.token_url, data).json()
        self.token = result['access_token']
        self.expires = result['expires_in']
        self.token_type = result['token_type']
        self.refresh_token = result['refresh_token']
        self.auth = OAuthCcmp(self.token)

    def get_campaign(self, id_campaign):
        """
        """
        session = requests.Session()
        url = self.base_url + "services2/api/EmailCampaign"
        params = {'id': id_campaign}
        return session.get(url, params=params, auth=self.auth).json()
