import sys
from os import path
import snapchat
def download_all(username, password, download_dir):
    connection = snapchat.Snapchat(username, password)
    connection.connect()
    downloadable = filter(lambda snap : snap.viewable, connection.snaps)
    for snap in downloadable:
        try:
            data = connection.download()
            with open(path.join(download_dir, snap.id), "w") as f:
                    f.write(data)
            print("Downloaded snap %s" % (snap.id))
        except Exception as e:
            print("Failed to download %s: %s" % (snap.id, e))

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    download_dir = sys.argv[3]
    download_all(username, password, download_dir)
