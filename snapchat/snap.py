from .util import timestamp
from Crypto.Cipher import AES
class Caption():
    def __init__(self, text, location, orientation):
        self.text = text
        self.location = location
        self.orientation = orientation

    @staticmethod
    def from_json(snap):
        if not snap.has_key('cap_text'):
            return None
        return Caption(snap['cap_text'],
                       snap['cap_pos'],
                       snap['cap_ori'])
class Snap():
    encryption_key = "M02cnQ51Ji97vwT4"

    class Type():
        """
        The media type of Snap
        """
        IMAGE = 0
        VIDEO = 1
        VIDEO_NO_AUDIO = 2
        FRIEND_REQ = 3
        FRIEND_REQ_IMAGE = 4
        FRIEND_REQ_VIDEO = 5
        FRIEND_REQ_VIDEO_NO_AUDIO = 6

    class State():
        """
        The state of the Snap.

        Snaps that are viewed are (claimed to be) deleted from the server
        """
        SENT = 0
        DELIVERED = 1
        VIEWED = 2
        SCREENSHOT = 3


    @property
    def viewable(self):
        return self.state == Snap.State.DELIVERED and self.type != Snap.Type.FRIEND_REQ

    def download(self, connection, when=None):
        """
        Download a snap from the server.
        @connection The SnapChat class to use for sending the request
        """
        if not self.viewable:
            raise Exception("Snap not viewable, cannot download")

        if when is None:
            when = timestamp()

        params = {'id' : self.id, 'timestamp' : when, 'username' : connection.username}
        result = connection.send_req("/bq/blob", params, when).content
        # test if result is unencrypted
        if result[:3] == '\x00\x00\x00' and results[5:12] == '\x66\x74\x79\x70\x33\x67\x70\x35':
            return result
        elif result[:3] == '\xFF\xD8\xFF':
            return result

        # otherwise encrypted, decrypt it.
        crypt = AES.new(self.encryption_key, AES.MODE_ECB)
        result = crypt.decrypt(result)
        return result

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class SentSnap(Snap):

    def __init__(self, id, recipient, type, state, timestamp, send_timestamp, view_time = 0, screenshots = 0, caption = None):
        self.id = id
        self.recipient = recipient
        self.user = recipient
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp
        self.screen_shots = screenshots
        self.caption = caption

    @staticmethod
    def from_json(snap):
        return SentSnap(snap['id'],
                        snap['rp'],
                        snap['m'],
                        snap['st'],
                        snap['ts'],
                        snap['sts'],
                        snap.get('t',0),
                        snap.get('ss', 0),
                        Caption.from_json(snap))
    @property
    def viewable(self):
        return False

class ReceivedSnap(Snap):

    def __init__(self, id, sender, type, state, timestamp, send_timestamp, view_time = 0, screenshots = 0, caption = None):
        self.id = id
        self.sender = sender
        self.user = sender
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp
        self.screen_shots = screenshots
        self.caption = caption

    @staticmethod
    def from_json(snap):
        return ReceivedSnap(snap['id'],
                        snap['sn'],
                        snap['m'],
                        snap['st'],
                        snap['ts'],
                        snap['sts'],
                        snap.get('t',0),
                        snap.get('ss', 0),
                        Caption.from_json(snap))
