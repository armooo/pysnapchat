from .util import timestamp
from Crypto.Cipher import AES
class Snap():
    encryption_key = "M02cnQ51Ji97vwT4"

    class Type():
        """
        The media type of Snap
        """
        JPG = 0
        MP4 = 2

    class State():
        """
        The state of the Snap.

        Snaps that are viewed are (claimed to be) deleted from the server
        """
        viewable = 1
        viewed = 2

    @property
    def viewable(self):
        return self.state == Snap.State.viewable

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
        if self.type == Snap.Type.MP4 and result[:3] == '\x00\x00\x00'\
                     and results[5:12] == '\x66\x74\x79\x70\x33\x67\x70\x35':
            return result
        elif self.type == Snap.Type.JPG and result[:3] == '\xFF\xD8\xFF':
            return result

        # otherwise encrypted, decrypt it.
        crypt = AES.new(self.encryption_key, AES.MODE_ECB)
        result = crypt.decrypt(result)
        return result

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class SentSnap(Snap):

    def __init__(self, id, recipient, type, state, timestamp, send_timestamp, view_time = 0):
        self.id = id
        self.recipient = recipient
        self.user = recipient
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp

    @property
    def viewable(self):
        return False

class ReceivedSnap(Snap):

    def __init__(self, id, sender, type, state, timestamp, send_timestamp, view_time = 0):
        self.id = id
        self.sender = sender
        self.user = sender
        self.type = type
        self.state = state
        self.timestamp = timestamp
        self.send_timestamp = timestamp

