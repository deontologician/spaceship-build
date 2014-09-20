import getpass
import platform
import os.path
import os
from pathlib import Path
import configparser
from collections import OrderedDict

import zmq
from zmq.eventloop import ioloop, zmqstream
import zmq.auth
import blosc
import msgpack
from common import fprint

DEFAULT_PORT = 6969


class ClientConnection:
    def __init__(self,
                 private_key,
                 public_key,
                 server_key,
                 server_address,
                 socket_type=zmq.DEALER,
                 context=None):
        self.context = context or zmq.Context.instance()
        self.socket = self.context.socket(socket_type)
        self.socket.curve_secretkey = private_key
        self.socket.curve_publickey = public_key
        self.socket.curve_serverkey = server_key
        self.server_address = server_address
        self.stream = None

    @staticmethod
    def from_socket(socket):
        return ClientConnection(
            socket.curve_secretkey,
            socket.curve_publickey,
            socket.curve_serverkey,
            socket_type=socket.socket_type,
            context=socket.context,
        )

    def connect(self, recv_callback):
        '''Takes a callback for when messages are received on the
        socket'''

        def deserialize(function):
            def _wrapper(raw_msg):
                msg = msgpack.loads(blosc.decompress(raw_msg.decode('utf-8')))
                return function(msg)
            return _wrapper

        self.socket.connect(self.server_address)
        self.stream = zmqstream.ZMQStream(self.socket)
        self.stream.on_recv(deserialize(recv_callback))

    def send(self, msg):
        '''Sends a message on the socket'''
        packed = blosc.compress(msgpack.dumps(msg), typesize=8)
        self.stream.send(packed)


class ServerConnection:
    def __init__(self,
                 private_key=None,
                 public_key=None,
                 endpoint=None,
                 socket_type=zmq.ROUTER,
                 context=None,
                 socket=None,
             ):
        if socket is not None:
            import ipdb
            ipdb.set_trace()
            self.socket = socket
            self.context = socket.context
        else:
            self.context = context or zmq.Context.instance()
            self.socket = self.context.socket(socket_type)
            self.socket.curve_secretkey = private_key
            self.socket.curve_publickey = public_key
            self.socket.curve_server = True
        self.endpoint = endpoint

    @staticmethod
    def from_socket(socket):
        return ServerConnection(socket=socket)

    def listen(self, listen_callback):
        '''Bind to the intended port and listen for connections. Pass
        connections to the given callback'''

        def deserialize(function):
            def _wrapper(raw_server, raw_msg):
                msg = msgpack.loads(blosc.decompress(raw_msg[1]))
                server = ServerConnection.from_socket(raw_server)
                return function(server, msg)
            return _wrapper

        self.socket.bind(self.endpoint)
        stream = zmqstream.ZMQStream(self.socket)
        stream.on_recv_stream(deserialize(listen_callback))
        return stream

    def send(self, msg):
        '''Sends a message on the socket'''
        packed = blosc.compress(msgpack.dumps(msg), typesize=8)
        self.stream.send(packed)


class Configuration:
    '''Manages app configuration directory. One of these should be
    created per run of the server or the client
    '''

    DEFAULTS = {
        'server': {
            'address': 'tcp://127.0.0.1:6969',
            'public_key': 'ND5YqX!CEE/*HpT+IEPbt*cfb)IE}yrLH}0srv-E',
            'bind_to': 'tcp://127.0.0.1:6969',
        },
    }
    
    def __init__(self, conn_type):
        self.conn_type = conn_type
        self.config_dir = None
        self.get_config_dir()
        self.public_key_dir = None
        self.private_key_dir = None
        self.get_key_dirs()
        self.config_file = None
        self.get_config_file()
        self.get_keys()
        self.save()

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
        self.config_file = self.config_dir / 'spaceship.conf'
        self.config_file.touch(exist_ok=True)
        self.config = configparser.ConfigParser()
        self.configurate(self.config)
        self.config.read(self.config_file.as_posix())

    def configurate(self, config):
        for section, keys in self.DEFAULTS.items():
            config[section] = keys

    def get_keys(self):
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
        self.public_key, self.private_key = zmq.auth.load_certificate(
            priv_key_file.as_posix())
        self.server_pub_key_file = self.public_key_dir / 'server.key'

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
