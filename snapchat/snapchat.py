import requests
import time
from .util import timestamp, build_token
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
                snaps.append(SentSnap(snap['id'], snap['rp'], snap['m'], snap['st'], snap['ts'],\
                                      snap['sts'], snap.get('t', 0)))
            elif snap.has_key('sn'):
                snaps.append(ReceivedSnap(snap['id'], snap['sn'], snap['m'], snap['st'],\
                                          snap['ts'], snap['sts'], snap.get('t', 0)))
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
        result = self.send_req("/bq/all_updates", params, stamp).json()
        self._do_update(result['updates_response'])
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




