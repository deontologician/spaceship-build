import enum
import getpass

import zmq
import msgpack
from common import fprint

DEFAULT_PORT = 6969

class Proto(enum.Enum):
    PROTOCOL_VERSION = 1
    HELLO = 1
    LOGIN = 2
    LOGIN_FAILED = 3

class Connection:
    def __init__(self, hostname='localhost', port=DEFAULT_PORT):
        self.hostname = hostname
        self.port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)

    def connect(self):
        '''Connect to the server'''
        self.connect('tcp://{}:{}'.format(self.hostname, self.port))
        self.send({'protocol': Proto.PROTOCOL_VERSION, 'type': Proto.HELLO})
        return self.recv()

    def close(self):
        '''Close the connection to the server'''
        self._socket.close()

    def send(self, msg):
        '''Send a JSON message to the server'''
        self._socket.send(msgpack.dumps(msg))

    def recv(self):
        '''Receive a message from the server'''
        msgpack.loads(self._socket.recv(), encoding='utf-8')

    def login(self, username, password):
        '''Log into the server'''
        self.send({'type': Proto.LOGIN,
                   'username': username,
                   'password': password})
        return self.recv()


def main():
    conn = Connection()
    fprint('Connecting to SpaceShip build server at {host} on port {port}',
           port=conn.port, host=conn.hostname)
    motd = conn.connect()['motd']
    print(motd)

    # Attempt to log in
    username = input('email: ')
    password = getpass.getpass()
    login_response = conn.login(username, password)
    if login_response['type'] == Proto.LOGIN_FAILED:
        print('Failed to login:', login_response['reason'])


if __name__ == '__main__':
    main()
