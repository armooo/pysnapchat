import requests
import time
from .util import timestamp, build_token
class Friend():
    def __init__(self, name, display, type, can_see_custom_stories):
        self.name = name
        self.display = display
        self.type = type
        self.can_see_custom_stories = can_see_custom_stories
    def __repr__(self):
        return "name:\"%s\" display:\"%s\" type:%d can_see_custom_stories: %s"\
                % (self.name, self.display, self.type, self.can_see_custom_stories)
class SnapChat():
    host = "https://feelinsonice-hrd.appspot.com"
    static_token = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.friends = None

    def connect(self):
        stamp = timestamp()
        params = {"username" : self.username, "password" : self.password, "timestamp": stamp}
        result = self.send_req("/bq/login", params, stamp).json()
        self.token = result['auth_token']
        self.login_data = result
        self._update(result)

    def _update(self, json):
        # update friends
        friends = set()
        for friend in json['friends']:
            friends.add(Friend(friend['name'], friend['display'], friend['type']\
                               ,friend['can_see_custom_stories']))
        self.friends = friends


    def update(self):
        if not self.token:
            raise Exception("Unauthenticated")
        stamp = timestamp()
        params = {"username" : self.username, "timestamp": stamp}
        result = self.send_req("/bq/all_updates", params, stamp).json()
        self._update(result['updates_response'])
        return result

    def send_req(self, path, params, when = None):
        if when is None:
            when = timestamp()
        if not "req_token" in params:
            params["req_token"] = self.req_token(when)

        r = requests.post(self.host+path,params)
        if r.status_code != 200:
            raise Exception("Request failed with status %d" % (r.status_code))
        return r

    def fetch(self, id):
        pass

    def req_token(self, when):
        if self.token is None:
            return build_token(self.static_token, when)
        else:
            return build_token(self.token, when)




