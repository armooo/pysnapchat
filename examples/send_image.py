import sys
import snapchat
def send_to(username, password, recipient, fname):
    with open(fname) as f:
        data = f.read()
    connection = snapchat.Snapchat(username, password)
    connection.connect()
    media_id = connection.upload(data, snapchat.Snap.Type.IMAGE)
    connection.send_to(recipient, media_id, snapchat.Snap.Type.IMAGE)

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    recipient = sys.argv[3]
    fname = sys.argv[4]
    send_to(username, password, recipient, fname)
