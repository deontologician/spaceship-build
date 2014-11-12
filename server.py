__author__ = 'xXxH3LIOSxXx'

from builtins import print
import socket
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to 6969
server_address = ('localhost', 6969)
print('\nSpaceShip build server starting up on %s port %s' % server_address)
sock.bind(server_address)

# Set queue depth for connections, not to be confused with allowed connections
sock.listen(3)
# Used to set threadID
perm_id = 0
# Used to store all client connections
threads = []

# Alright, lets do this!  Time to use the more recent Threading library...
# Overloading the threading class for our own purposes


class ClientThread (threading.Thread):
    def __init__(self, thread_id, client_connection):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.client_connection = client_connection

    def run(self):
        new_connection(self.client_connection)


def new_connection(client_connection):
        # Send MOTD when client first connects
        welcome = bytes('+++++++++++++++++++++++++++++++++++++++++++++++'
                        '\n++++++++++Welcome to SpaceShip build!++++++++++'
                        '\n+++++++++++++++++++++++++++++++++++++++++++++++'
                        '\n\nRight now all this server does is echo your input a single time!'
                        '\nType something now to try it out...', 'UTF-8')
        client_connection.send(welcome)

        while True:
            # Receive data from the client
            data = client_connection.recv(4096)
            reply = data
            if data.decode("utf-8") == '/q':
                print("\nClient disconnected from, ", client_connection)
                client_connection.close()
                break

            # Send response
            client_connection.send(reply)

while True:
    # Wait for a connection
    # Note: .accept() returns a connection between server/client and the clients IP to work with
    # This return is a DIFFERENT socket on another port defined by the kernel, it also is a blocking call
    print('\nWaiting for connections...')
    connection, client_address = sock.accept()

    print('\nClient connecting from', client_address)

    # Split off new threads for each connection
    threads.append(ClientThread(perm_id, connection))
    threads[perm_id].start()
    perm_id += 1
    #print('\nHere are the threads I currently have: %s' % threads)