import getpass
import platform
import os.path
import os
from pathlib import Path
import configparser

import zmq
from zmq.eventloop import ioloop, zmqstream
import zmq.auth
import blosc
import msgpack
from common import fprint

DEFAULT_PORT = 6969

class MegaConnection:
    def __init__(
            self, secret_file, server_public_key, host, port=DEFAULT_PORT):
        self.server_address = 'tcp://{}:{}'.format(host, port)
        self._socket = zmq.Context.instance().socket(zmq.REQ)
        public_key, private_key = zmq.auth.load_certificate(secret_file)
        self._socket.curve_secretkey = private_key
        self._socket.curve_publickey = public_key
        self._socket.curve_serverkey = server_public_key
        self.stream = None

    @staticmethod
    def deserialize(function):
        '''This is a decorator for recv callbacks. It uncompresses and
        deserializes the message'''
        def _wrapper(raw_msg):
            msg = msgpack.loads(blosc.decompress(raw_msg))
            return function(msg)
        return _wrapper

    def connect(self, msg_received):
        '''Takes a callback for when messages are received on the
        socket'''
        self._socket.connect(self.server_address)
        self.stream = zmqstream.ZMQStream(self._socket)
        self.stream.on_recv(self.deserialize(msg_received))

    def send(self, msg):
        '''Sends a message on the socket'''
        packed = blosc.compress(msgpack.dumps(msg), typesize=8)
        self.stream.send(packed)

class Configuration:
    '''Manages app configuration directory. One of these should be
    created per run of the server or the client
    '''

    def __init__(self, conn_type):
        self.conn_type = conn_type
        self.get_config_dir()
        self.get_key_dirs()
        self.get_config_file()
        self.create_keys()

    def get_config_dir(self):
        '''Returns the config dir. Creates it if necessary'''
        system = platform.system()
        if system == 'Linux':
            path = Path(os.getenv('HOME')) / '.config'
        elif system == 'Windows':
            path = Path(os.getenv('APPDATA'))
        self.config_dir = path / 'spaceship-build' / self.conn_type
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)

    def get_key_dirs(self):
        '''Get and create public and private key directories'''
        self.public_key_dir = self.config_dir / 'public_keys'
        self.private_key_dir = self.config_dir / 'private_keys'
        if not self.public_key_dir.exists():
            self.public_key_dir.mkdir()
        if not self.private_key_dir.exists():
            self.private_key_dir.mkdir()

    def get_config_file(self):
        '''Gets and creates the config file'''
        self.config_file = self.config_dir / 'config.conf'
        self.config_file.touch(exist_ok=True)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file.as_posix())

    def create_keys(self):
        '''Create server keys if needed'''
        pub_key_file = self.public_key_dir / (self.conn_type + '.key')
        priv_key_file = self.private_key_dir / (self.conn_type + '.key_secret')
        if not pub_key_file.exists() or not priv_key_file.exists():
            pub_path, priv_path = zmq.auth.create_certificates(
                self.config_dir.as_posix(), self.conn_type)
            # when regenerating, we unconditionally replace old files
            # if one is missing
            Path(pub_path).replace(pub_key_file)
            Path(priv_path).replace(priv_key_file)
        self.public_key = pub_key_file.open('b').read()
        self.private_key = priv_key_file.open('b').read()

    def __getitem__(self, key):
        return self.config[key]

    def save(self):
        '''Save the current configuration to the config file'''
        with self.config_file.open('w') as cf:
            self.config.write(cf)



def main():
    conn = MegaConnection()
    fprint('Connecting to SpaceShip build server at {host} on port {port}',
           port=conn.port, host=conn.hostname)
    motd = conn.connect()['motd']
    print(motd)

    # Attempt to log in
    username = input('email: ')
    password = getpass.getpass()
    login_response = conn.login(username, password)


if __name__ == '__main__':
    main()
