from random import getrandbits
import socket
from __init__ import P, G

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8000))
s.listen()

try:
    while True:
        a = getrandbits(32)

        conn, addr = s.accept()

        A = pow(G, a, P)
        conn.send(str(A).encode())

        B = int(conn.recv(20))
        secret = pow(B, a, P)

        print(secret)
        conn.close()
except KeyboardInterrupt:
    s.close()
