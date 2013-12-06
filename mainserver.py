#!/usr/bin/python

from numpy import poly1d as poly
from numpy import polyfit as fit

from socket import socket, SO_REUSEADDR, SOL_SOCKET
from pickle import loads
from base64 import b64decode
from threading import Thread
from time import sleep

from config import *

def Handler(ss):
  global A, R, x
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
for i in xrange(T + 1):
  ss = s.accept()[0]
  t = Thread(target=Handler, args=(ss, ))
  t.setDaemon(True)
  t.start()

sleep(5)
print A, R, x
Ax = poly(fit(x, A, T))
print Ax
print Ax(0)
