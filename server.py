#! /usr/bin/python3

import colorama
import json
import pyfiglet
import socket
import sys

from message import Message
from encryption import encryption


colorama.init(autoreset=True)

IP = '127.0.0.1'
PORT = 9998
ADDRESS = (IP, PORT)
META_HEADER_SIZE = 5

# Prime number are 23 and 31
SERVER_PRIVATE_KEY = (283, 713)
SERVER_PUBLIC_KEY = (7, 713)

CLIENT_PUBLIC_KEY = (101, 551)


class ServerNode:
    def __init__(self, ip, port):
        print(colorama.Fore.RED + pyfiglet.figlet_format('SERVER', font='slant'))

        self._address = (ip, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self._connection = None
        self._connection_address = None
        self.message = None

        try:
            self._socket.bind(self._address)
        except OSError as e:
            print(e)
            sys.exit(1)
    
    def initiate_connection(self):
        self._socket.listen(5)
        print('[+] server running at {}:{}'.format(self._address[0], self._address[1]))
        print()
        
        self._connection, self._connection_address = self._socket.accept()
        self.message = Message(self._connection, self._connection_address)

        print('[+] {} Connected!'.format(self._connection_address[0]))
        print()
    
    def chat(self):
        self.initiate_connection()
        connected = True

        while connected:
            message = input('[message]: ')
            encrypted = encryption.rsa(encryption.rsa(message, CLIENT_PUBLIC_KEY), SERVER_PRIVATE_KEY)
            self.message.send(encrypted)
            print('---sent'.rjust(50, ' '))
            if message == 'terminate':
                connected = False
                break
            print('waiting...')
            print()

            try:
                # output = self.message.receive()
                cipher = self.message.receive()
                output = encryption.rsa(encryption.rsa(cipher, CLIENT_PUBLIC_KEY), SERVER_PRIVATE_KEY)
            except KeyboardInterrupt:
                sys.exit(0)

            print('[{}]: {}'.format(self._connection_address[0], output))
            print('---received'.rjust(50, ' '))
            print()

        self._connection.close()
        self._socket.close()
        print('[DISCONNECTED]'.center(50, '-'))

s = ServerNode(IP, PORT)
s.chat()



