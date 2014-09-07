__author__ = 'xXxH3LIOSxXx'

from builtins import print
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to 6969
server_address = ('localhost', 6969)
print('\nSpaceShip build server starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections, just 1 now for testing
sock.listen(1)

while True:
    # Wait for a connection
    print('\nWaiting for connections...')
    connection, client_address = sock.accept()

    # Pre-loading buffer with a MOTD
    welcome = bytes('+++++++++++++++++++++++++++++++++++++++++++++++\n++++++++++Welcome to SpaceShip build!++++++++++\n+++++++++++++++++++++++++++++++++++++++++++++++\n\nRight now all this server does is echo your input a single time!\nType something now to try it out...', 'UTF-8')
    connection.sendall(welcome)

    try:
        print('\nClient connecting from', client_address)

        # Receive the data and for the time being re-transmit it
        while True:
            data = connection.recv(1024)
            print('Received >> "%s"' % data.decode("utf-8"))
            if data:
                print('Sending data back to', client_address)
                connection.sendall(data)
            else:
                print('No more data from', client_address)
                break

    finally:
        # Clean up the connection
        print('Closing connection from', client_address)
        connection.close()
        print('Connection closed!')