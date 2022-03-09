# Messaging

### Package encryption 
it contain a ROT algorithm to shift character forward and another to shift it back to get original plain text from cipher.
It also contain the __RSA__ algorithm function which encrypt and decrypt the given message using the passed key.

# Server.py
This file is the server side of the socket connection and uses a hardcoded __RSA__ _public and private key_.

# Client.py
This file contain the client side code of the socket connection and also have __RSA__ hardcoded values.
