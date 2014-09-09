import zmq
from common import fprint


def main():
    context = zmq.Context()
    host, port = 'localhost', 6969
    fprint('Connecting to SpaceShip build server at {host} on port {port}',
           port=port, host=host)
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:{}'.format(host, port))
    print('Connection successful!')
    socket.send_string('Hello yall')

    motd = socket.recv_string()
    print(motd)
    to_be_echoed = input('>> ')
    socket.send_string(to_be_echoed)
    echo = socket.recv_string()
    print('Server sez:', echo)

    socket.close()
    print('Connection closed!')


if __name__ == '__main__':
    main()