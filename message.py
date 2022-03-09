import json


class Message:
    """A class to represent the message sent and receive"""

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self._recvd_buffer = b''
        self._send_buffer = b''
        self._json_header = None 
        self._json_header_length = None   # fixed bytes to get the header length 

    def _json_decode_header(self, header: bytes) -> dict:
        self._json_header = header.decode('utf-8')
        return json.loads(self._json_header)

    def _json_encode_header(self, json_header, encoding='utf-8'):
        header = json.dumps(json_header)
        return header.encode(encoding)

    def _decode_message(self, message, encoding='utf-8'):
        return message.decode(encoding)

    def _encode_message(self, message, encoding='utf-8'):
        return message.encode(encoding)

    def _parse_header(self, header: bytes) -> tuple:
        self._json_header = self._json_decode_header(header)
        
        content_type = self._json_header['content_type']
        content_length = self._json_header['content_length']
        content_encoding = self._json_header['content_encoding']

        return content_length, content_type, content_encoding
    
    def _create_message(self, message, content_type, content_encoding):
        self._json_header = {'content_type': content_type,
                             'content_encoding': content_encoding,
                             'content_length': len(message),}
        
        header = self._json_encode_header(self._json_header)
        self._json_header_length = len(header)
        
        header_length = str(self._json_header_length)
        header_length = self._encode_message(header_length)
        
        message_bytes = self._encode_message(message)
        content = b''.join([header_length,  header,  message_bytes])
        return content

    def _parse_message(self):
        if self._recvd_buffer:
            header_length = 2
        
            self._json_header_length = self._recvd_buffer[: header_length]
            self._json_header_length = int(self._decode_message(self._json_header_length))
            
            self._recvd_buffer = self._recvd_buffer[header_length :]  # slice empty the buffer as we parse it

            header = self._recvd_buffer[: self._json_header_length]
            content_length, content_type, content_encoding = self._parse_header(header)
        
            self._recvd_buffer = self._recvd_buffer[self._json_header_length :]
        
            return self._decode_message(self._recvd_buffer)
        else:
            return None
    
    def send(self, message, content_type='text/json', content_encoding='utf-8'):
        self._send_buffer =  self._create_message(message, content_type, content_encoding)
        self.connection.sendall(self._send_buffer)

    def receive(self):
        self._recvd_buffer = self.connection.recv(4096)
        message = self._parse_message()
        
        if message is not None:
            return message
        else:
            raise ValueError('empty buffer')


