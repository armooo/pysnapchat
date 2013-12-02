This project is a simple python binding for connecting to Snapchat.

Features
=========

[x] Connect to your Snapchat account and fetch your friends and snaps

[x] Download snaps

[ ] Update state for snaps(Viewed, screenshot, etc)

[ ] Send snaps

[ ] Add/Remove friends

[ ] ????

Snapchat and encryption
=======================

Snapchat does some odd things when it comes to encryption and authentication.

Encryption
-----------------------

For encryption snaps are encrypted when the user sends them.
Unfortunately the key is a fixed key stored in the application APK,
so this encryption is completely useless in practice.

They also use AES-128 in _ECB_ mode. ECB mode is one of those encryption modes
that should _never_ be used.


Authentication/Session Management
---------------------------------

Snapchat also diverges from the norm in how they manage sessions in a weird and frankly worrisome way.

In a normal session based system on login the server provides an authentication token and on all subsequent requests
the client provides that token for authentication.

Snapchat however decided to implement a different system. While they send an authentication token on login they do not send it on
subsequent requests, instead they include a 'request id'. The goal, I presume, was to avoid the situation where if the token is stolen
an attacker can issue as many requests as they want. Unfortunately they failed completely at this.

This request id is a very odd creature, in any given session watching the request ids all of them will have the same value in certain
spots of the string, this is a pretty big red flag for a token.

The code for generating these tokens can be found [here](snapchat/util.py).

The pseudocode for generation is:

```Python
hash0 = sha256(secret + auth_token)
hash1 = sha256(timestamp + secret)
for i in range(len(hash0))
	if pattern[i] == '0'
		output[i] = hash0[i]
	else
		output[i] = hash1[i]
```

Both the pattern and the 'secret' are fixed and hardcoded into the application.

Because the pattern and secret are the same for every request it is not necessary to compute hash0. 
The parts of output that depend on the authentication token are fixed for an entire session.
Note that hash0[i] where pattern[i] != 0 has _no_ effect on the output, and all places where pattern[i] == 0 hash0[i] appears directly in the token.
Simply using the observed token in place of hash0 allows an attacker to generate new request ids.

In the end this entire request id setup is as secure as an authentication token for much more work and complexity.
