#!/usr/bin/python

from numpy import polynomial as poly
from numpy import polyfit as fit

from socket import socket, SO_REUSEADDR, SOL_SOCKET
from pickle import loads
from base64 import b64decode
from threading import Thread, RLock

from config import *

def Handler(ss):
  data = ss.recv(100)
  Id, u, w = loads(b64decode(data))
  ss.send("OK\n")
  ss.close()
  A.append(u)
  R.append(w)
  x.append(Id + 1)

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
s.bind((MAINSERVER, MAINPORT))
s.listen(100)
global A, R, x
A = []
R = []
x = []
for i in xrange(T):
  ss = s.accept()[0]
  Handler(ss)

print A, R, x
Ax = poly.Polynomial(fit(x, A, T))
print Ax(0)
