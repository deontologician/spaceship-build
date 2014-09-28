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

def pack(obj):
    '''Pack a simple object'''
    return blosc.compress(msgpack.dumps(obj), typesize=8)

def unpack(bytearray):
    '''Unpack a bytearray to a simple object'''
    return msgpack.loads(blosc.decompress(bytearray), encoding='utf-8')


class SpaceSocket(zmq.Socket):
    '''Subclass of socket that uses blosc and msgpack'''
    def send_packed(self, obj, flags=0):
        '''Send a packed object'''
        self.send(pack(obj), flags=flags)

    def recv_packed(self, flags=0):
        '''Receive a packed object and unpack it'''
        return unpack(self.recv(flags=flags))


class SpaceContext(zmq.Context):
    '''Subclass of Context that uses SpaceSockets'''

    @property
    def _socket_class(self):
        return SpaceSocket


class SpaceZMQStream(zmqstream.ZMQStream):
    '''ZMQStream that has the ability to send packed objects'''
    def send_packed(self, obj, flags=0, callback=None):
        '''Sends a packed message'''
        self.send(pack(obj), flags=flags, callback=callback)

    def on_recv_packed(self, callback, copy=True):
        '''The callback will receive an unpacked object'''
        if callback is None:
            self.stop_on_recv()
        else:
            self.on_recv(lambda msg: callback(unpack(msg[-1])), copy=copy)

    def on_recv_packed_stream(self, callback, copy=True):
        '''The callback will receive this stream and the unpacked object'''
        if callback is None:
            self.stop_on_recv()
        else:
            self.on_recv(lambda msg: callback(
                lambda msg: self.send_packed(msg),
                unpack(msg[-1])),
                         copy=copy)


class ClientConnection:
    def __init__(self,
                 private_key,
                 public_key,
                 server_key,
                 server_address,
                 socket_type=zmq.DEALER,
                 context=None):
        self.context = context or SpaceContext.instance()
        self.socket = self.context.socket(socket_type)
        self.socket.curve_secretkey = private_key
        self.socket.curve_publickey = public_key
        self.socket.curve_serverkey = server_key
        self.server_address = server_address
        self.stream = None

    def connect(self, recv_callback):
        '''Takes a callback for when messages are received on the
        socket'''
        self.socket.connect(self.server_address)
        self.stream = SpaceZMQStream(self.socket)
        self.stream.on_recv_packed(recv_callback)

    def send(self, msg):
        '''Sends a message on the socket'''
        self.stream.send_packed(msg)


class ServerConnection:
    def __init__(self,
                 private_key=None,
                 public_key=None,
                 endpoint=None,
                 socket_type=zmq.ROUTER,
                 context=None,
             ):
        self.context = context or SpaceContext.instance()
        self.socket = self.context.socket(socket_type)
        self.socket.curve_secretkey = private_key
        self.socket.curve_publickey = public_key
        self.socket.curve_server = True
        self.endpoint = endpoint

    def listen(self, listen_callback):
        '''Bind to the intended port and listen for connections. Pass
        connections to the given callback'''

        self.socket.bind(self.endpoint)
        stream = SpaceZMQStream(self.socket)
        stream.on_recv_packed_stream(listen_callback)
        return stream

    def send(self, msg):
        '''Sends a message on the socket'''
        self.stream.send_packed(msg)


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


if __name__ == '__main__':
    pass
