#! /usr/bin/python3

import colorama
# import json
import pyfiglet
# import subprocess
import socket
import sys

from encryption import encryption
from message import Message

colorama.init(autoreset=True)


IP = '127.0.0.1'
PORT = 9998
ADDRESS = (IP, PORT)
META_HEADER_SIZE = 5   # define the size of the header

SERVER_PUBLIC_KEY = (7, 713)

# Prime number are 19 and 29
CLIENT_PRIVATE_KEY = (5, 551)
CLIENT_PUBLIC_KEY = (101, 551)


class ClientNode:
    def __init__(self, ip, port):
        print(colorama.Fore.RED + pyfiglet.figlet_format('CLIENt', font='slant'))
        
        self._address = (ip,  port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = Message(self._socket, self._address)
    
    def initiate_connection(self):
        try:
            self._socket.connect(self._address)
        except ConnectionRefusedError:
            print('[Error] Check if the server is running on {}'.format(self._address))
            sys.exit(1)
        print('[+] Connected to {}:{}'.format(IP, PORT))
        print()
    
    # def execute(self, command):
    #     command = command.strip().split(' ')
    #     print(command)
    #     try:
    #         process = subprocess.Popen(command,
    #                                    stdin=subprocess.PIPE,
    #                                    stdout=subprocess.PIPE,
    #                                    stderr=subprocess.PIPE,
    #                                    text=True,)
    #     except FileNotFoundError as e:
    #         print('except block')
    #         ouput = 'Invalid command!'
    #     else:
    #         print('else blockk')
    #         output = '\n\n'.join([process.stdout.read(),process.stderr.read()])
    #     print(output)
    #     return output

    def chat(self):
        self.initiate_connection()
        
        print('waiting...', end='\n\n')
        cipher = self.message.receive()
        message = encryption.rsa(encryption.rsa(cipher, SERVER_PUBLIC_KEY), CLIENT_PRIVATE_KEY)
        while message != 'terminate':
            print('[message]: {}'.format(message))
            print('---received'.rjust(50, ' '), end='\n\n')

            # response = self.execute(message)
            response = input('[message]: ')
            
            # encrypt the text content using client Private key
            # encrypt the encrypted content using Server Public key
            # so only Server can open and be sure it was sent by 
            encrypted = encryption.rsa(encryption.rsa(response, SERVER_PUBLIC_KEY), CLIENT_PRIVATE_KEY) 
            self.message.send(encrypted, 'text/json', 'utf-8')
            
            print('---sent'.rjust(50, ' '), end='\n\n')

            print('waiting...', end='\n\n')
            try:
                cipher = self.message.receive()
                message = encryption.rsa(encryption.rsa(cipher, SERVER_PUBLIC_KEY), CLIENT_PRIVATE_KEY)
            except KeyboardInterrupt:
                sys.exit(0)

        print('[Disconnecting]'.center(50, '-'))
        self._socket.close()

c = ClientNode(IP, PORT)
c.chat()



    
