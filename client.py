__author__ = 'xXxH3LIOSxXx'

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6969)
print('\nConnecting to SpaceShip build server at %s on port %s' % server_address)
sock.connect(server_address)

# Need to add try for this later
print("Connection successful!"
      "\nEnter \"/q\" to quit")

# Checking buffer for any motd's
welcome = sock.recv(4096)
print('%s' % welcome.decode("utf-8"))

while True:

    # Prompt user, accept input, send to socket
    message = bytes(input('>> '), 'UTF-8')
    sock.send(message)

    # If the user inputs the escape sequence /q the socket closes cleanly
    cmd = message.decode("utf-8")
    cmd = cmd[:2]
    #print('%s' % cmd)

    if cmd == '/q':
        print("\nWe're quitting Bob.")
        break
    data = sock.recv(4096)
    print('<others> %s' % data.decode("utf-8"))

print('\nClosing connection...')
sock.close()
print('Connection closed!')
