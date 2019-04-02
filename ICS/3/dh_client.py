from random import getrandbits
import socket
from __init__ import P, G

b = getrandbits(32)

s = socket.socket()
s.connect(('127.0.0.1', 8000))

B = pow(G, b, P)
s.send(str(B).encode())

A = int(s.recv(20))
secret = pow(A, b, P)

print(secret)
s.close()
