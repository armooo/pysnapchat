import requests
import time
from .util import timestamp, build_token
class SnapChat():
    host = "https://feelinsonice-hrd.appspot.com"
    static_token = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def connect(self):
        stamp = timestamp()
        params = {"username" : self.username, "password" : self.password, "timestamp": stamp}
        result = self.send_req("/bq/login", params, stamp).json()
        self.token = result['auth_token']
        self.login_data = result

    def all_updates(self):
        if not self.token:
            raise Exception("Unauthenticated")
        stamp = timestamp()
        params = {"username" : self.username, "timestamp": stamp}
        result = self.send_req("/bq/all_updates", params, stamp).json()
        return result['updates_response']['snaps']

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




