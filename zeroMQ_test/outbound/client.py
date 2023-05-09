# echo_client.py

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.17.136.52', 10000)
sock.connect(server_address)

try:
    message = b'This is our message. It is very long but will only be transmitted in chunks of 16 at a time'
    sock.sendall(message)
 
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))
finally:
    sock.close()