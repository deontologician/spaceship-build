
import zmq
from zmq.auth.ioloop import IOLoopAuthenticator
from zmq.eventloop import ioloop, zmqstream
import zmqclient as ZC

def test_connection():
    server_conf = ZC.Configuration('server')
    client_conf = ZC.Configuration('client')
    client_context = zmq.Context()
    server_context = zmq.Context()
    
    server = ZC.ServerConnection(
        server_conf.private_key,
        server_conf.public_key,
        context=server_context,
        endpoint='tcp://127.0.0.1:6969',
    )

    def echo_server(server, msg):
        print('Msg:', msg)
        server.send({'hi': 'dude'})

    client = ZC.ClientConnection(
        client_conf.private_key,
        client_conf.public_key,
        client_conf['server']['public_key'].encode('utf-8'),
        'tcp://127.0.0.1:6969',
        context=client_context,
    )

    def dumb_client(msg):
        print('Msg:', msg)

    loop = server.listen(echo_server)
    client.connect(dumb_client)
    auth = IOLoopAuthenticator()
    auth.allow('127.0.0.1')
    auth.configure_curve(
        domain='*',
        location=client_conf.public_key_dir.as_posix(),
    )
    client.send({"hiyas": "there"})
    auth.start()
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    test_connection()