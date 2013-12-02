import requests
import time
from .util import timestamp, build_token, ecb_encrypt
from .friend import Friend
from .snap import Snap, SentSnap, ReceivedSnap
class Snapchat():
    host = "https://feelinsonice-hrd.appspot.com"
    static_token = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.friends = None
        self.snaps = None

    def connect(self):
        stamp = timestamp()
        params = {"username" : self.username, "password" : self.password, "timestamp": stamp}
        # clear the token to support reconnecting
        self.token = None
        result = self.send_req("/bq/login", params, stamp).json()
        self.token = result['auth_token']
        self.login_data = result
        self._do_update(result)

    def _do_update(self, json):
        # update friends
        friends = []
        for friend in json['friends']:
            friends.append(Friend(friend['name'], friend['display'], friend['type']\
                               ,friend['can_see_custom_stories']))
        self.friends = friends

        # update snaps
        snaps = []
        for snap in json['snaps']:
            if snap.has_key('rp'):
                snaps.append(SentSnap.from_json(snap))
            elif snap.has_key('sn'):
                snaps.append(ReceivedSnap.from_json(snap))
            else:
                raise Exception("Unknown snap, no sender or receiver")
        self.snaps = snaps


    def download(self, snap):
        return snap.download(self)

    def update(self):
        if not self.token:
            raise Exception("Unauthenticated")
        stamp = timestamp()
        params = {"username" : self.username, "timestamp": stamp}
        result = self.send_req("/bq/updates", params, stamp).json()
        self._do_update(result)
        return result

    def update_all(self):
        if not self.token:
            raise Exception("Unauthenticated")
        stamp = timestamp()
        params = {"username" : self.username, "timestamp": stamp}
        result = self.send_req("/bq/all_updates", params, stamp).json()
        self._do_update(result['updates_response'])
        return result

    def upload(self, data, type, media_id = None, when = None, encrypt = True, key = None):
        if key is None:
            key = Snap.encryption_key
        if when is None:
            when = timestamp()
        if media_id is None:
            media_id = self.username.upper() + when
        if encrypt:
            data = ecb_encrypt(data, key)
            print len(data)
        params = {"username" : self.username, "timestamp": when\
                , "media_id" : media_id, "type" : type}
        files = {'data' : ('file', data)}
        self.send_req("/bq/upload", params, when, files)

        return media_id

    def send_to(self, recipient, media_id, type, time = 10, country_code = "US", when = None):
        if when is None:
            when = timestamp()
        params = {"username" : self.username, "timestamp": when\
                , "media_id" : media_id, "type" : type\
                , "country_code" : country_code, "recipient" : recipient\
                , "time" : time}
        self.send_req("/bq/send", params, when)

    def send_req(self, path, params, when = None, files = None):
        if when is None:
            when = timestamp()
        if not "req_token" in params:
            params["req_token"] = self.req_token(when)

        r = requests.post(self.host+path,params, files = files)
        if r.status_code != 200:
            raise Exception("Request failed with status %d" % (r.status_code))
        return r

    def req_token(self, when):
        if self.token is None:
            return build_token(self.static_token, when)
        else:
            return build_token(self.token, when)




