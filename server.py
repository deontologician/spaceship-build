__author__ = 'xXxH3LIOSxXx'

from builtins import print
import socket

from _thread import *


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to 6969
server_address = ('localhost', 6969)
print('\nSpaceShip build server starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections, just 1 now for testing
# More specifically, this sets the socket as a 'server' type socket
sock.listen(3)

# First work at creating individual threads per connected client
def clientthread(clientconnection):

    # Send MOTD when client first connects
    welcome = bytes('+++++++++++++++++++++++++++++++++++++++++++++++\n++++++++++Welcome to SpaceShip build!++++++++++\n+++++++++++++++++++++++++++++++++++++++++++++++\n\nRight now all this server does is echo your input a single time!\nType something now to try it out...', 'UTF-8')
    connection.sendall(welcome)

    while True:

        # Receive data from the client
        data = clientconnection.recv(1024)
        reply = data
        if not data:
            break

        # Send response
        clientconnection.sendall(reply)

    # Clean up the connections
    clientconnection.close()

while True:
    # Wait for a connection
    # Note: .accept() returns a connection between server/client and the clients IP to work with
    # This return is a DIFFERENT socket on another port defined by the kernel, it also is a blocking call
    print('\nWaiting for connections...')
    connection, client_address = sock.accept()

    print('\nClient connecting from', client_address)

    # Split off new threads for each connection
    start_new_thread(clientthread, (connection,))

# Close out the servers listening socket
sock.close()

    ######## Legacy code, kept for reference
    #try:
        #print('\nClient connecting from', client_address)

        # Receive the data and for the time being re-transmit it
        #while True:
            #data = connection.recv(1024)
            #print('Received >> "%s"' % data.decode("utf-8"))
            #if data:
                #print('Sending data back to', client_address)
                #connection.sendall(data)
            #else:
               # print('No more data from', client_address)
                #break

    #finally:
        # Clean up the connection
        #print('Closing connection from', client_address)
        #connection.close()
        #print('Connection closed!')