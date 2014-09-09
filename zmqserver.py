import zmq

def welcome(socket):
    width = 60
    banner = '\n'.join([
        '+' * width,
        'Welcome to SpaceShip build!'.center(width, '+'),
        '+' * width,
        'Right now all this server does is echo your input a single time!',
        '',
        'Type something now to try it out...',
    ])

    socket.send_string(banner)


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
