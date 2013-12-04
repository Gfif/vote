#!/usr/bin/python
# -*- encoding: utf-8 -*-

from sys import argv
from socket import socket
from random import randint as rand

from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from pickle import dumps, loads

from numpy import polynomial as poly

from config import *

def usage():
  print argv[0] + ":Usage " + argv[0] + "ID Voice(1 | -1)"

if __name__ == "__main__":
  if len(argv) < 3:
    usage()
    exit(1)

  # Голос берем из параметров, переданных на вход
  # Затемняющий элемент генерируем случайно
  a = int(argv[2])
  r = rand(1, P)

  Id = int(argv[1])
  
  
  # Генерируем случайные коэффициенты для поиномов A(x), R(x)
  A = [a]
  R = [r]
  for i in xrange(T):
    A.append(rand(1, P))
    R.append(rand(1, P))

  # Создаем полиномы
  Ax = poly.Polynomial(A)
  Rx = poly.Polynomial(R)
 
  # Импортируем приватный ключ для подписи
  keyfile = open(CLIENTKEYFILES[Id][0], "r")
  privkey = RSA.importKey(keyfile.read())
  keyfile.close()

  # Для каждого сервера из списка подключаемся к его серверу
  for i, sp in enumerate(zip(SERVERS, PORTS)):
    s = socket()
    s.connect((sp))

    # Берем значение полиномов в точке i + 1 и запаковываем
    ai = int(Ax(i + 1))
    ri = int(Rx(i + 1))
    print ai, ri
    bulletin = dumps((ai, ri))
    tosend = dumps((Id, bulletin, privkey.sign(bulletin, 0)))
    keyfile = open(SERVERKEYFILES[i][1], "r")
    publickey = RSA.importKey(keyfile.read())
    keyfile.close()

    # Отправляем i серверу подписанный бюллетень, зашифровав его
    b64tosend = b64encode(tosend)
    s.send(b64encode(publickey.encrypt(tosend, 0)[0]))
    s.close()

exit(0) 
