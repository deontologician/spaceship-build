import zmq
import msgpack

BANNER = '\n'.join([
    '+' * width,
    'Welcome to SpaceShip build!'.center(width, '+'),
    '+' * width,
])

DEFAULT_PORT = 6969

class Connection:
    def __init__(self, bind_port=DEFAULT_PORT):
        

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
