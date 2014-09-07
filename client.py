__author__ = 'xXxH3LIOSxXx'

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6969)
print('\nConnecting to SpaceShip build server at %s on port %s' % server_address)
sock.connect(server_address)

# Need to add try for this later
print('Connection successful!\n')

# Checking buffer for any motd's
welcome = sock.recv(1024)
print('%s' % welcome.decode("utf-8"))

try:

    # Prompt user, accept input, send to socket
    message = bytes(input('>> '), 'UTF-8')
    print('\nSending >> "%s"' % message.decode("utf-8"))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('Received >> "%s"' % data.decode("utf-8"))

finally:
    print('\nClosing connection...')
    sock.close()
    print('Connection closed!')
