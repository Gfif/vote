#!/usr/bin/python

from numpy import polynomial as poly
from numpy import polyfit as fit

from socket import socket, SO_REUSEADDR, SOL_SOCKET
from pickle import loads
from base64 import b64decode
from threading import Thread, RLock

from config import *

def Handler(ss, rl):
  data = ss.recv(100)
  Id, u, w = loads(b64decode(data))
  ss.send("OK\n")
  ss.close()
  rl.acquire()
  A.append(u)
  R.append(w)
  x.append(Id + 1)
  rl.release()

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
s.bind((MAINSERVER, MAINPORT))
s.listen(100)
global A, R, x
A = []
R = []
x = []
rl = RLock()
for i in xrange(T):
  ss = s.accept()[0]
  t = Thread(targer=Handler, args=(ss, rl))
  t.setDaemon(True)
  t.start()

print A, R, x
Ax = poly.Polynomial(fit(x, A, T))
print Ax(0)
