import zmq
import msgpack

import rethinkdb as r

from proto import Proto

BANNER = '\n'.join([
    '+' * width,
    'Welcome to SpaceShip build!'.center(width, '+'),
    '+' * width,
])

DEFAULT_PORT = 6969

class Connection:
    def __init__(self, bind_port=DEFAULT_PORT):
        self.port = bind_port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)

    def bind(self):
        self._socket.bind('tcp://*:{}'.format(self.port))

    def recv(self):
        return msgpack.loads(self._socket.recv(), encoding='utf-8')

    def send(self, msg):
        self._socket.send(msgpack.dumps(msg))

    def listen(self, consumer):
        next(consumer)  # initialize generator
        while True:
            consumer.send(self.recv())
            self.send(next(consumer))

def basic_server():
    hello = yield
    if hello['type'] != Proto.HELLO:
        raise Exception('improper introduction')
    login_request = yield BANNER
    if login_request['type'] != Proto.LOGIN:
        yield {'type': Proto.LOGIN_FAILED,
               'reason': 'Improper login request'}
        return
    
    
    


def main(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    
    while True:
        message = socket.recv()
        print("Received request:", message)
        welcome(socket)
        to_echo = socket.recv()
        print('Received >> "%s"' % to_echo.decode('utf-8'))
        socket.send(to_echo)

    
if __name__ == '__main__':
    main(6969)
