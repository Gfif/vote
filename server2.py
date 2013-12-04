#!/usr/bin/python
# -*- encoding: utf-8 -*-

from sys import argv
from socket import socket
from mutex import mutex

from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from pickle import loads, dumps

from numpy import polynomial
from config import *

def usage():
  print argv[0] + ":Usage " + argv[0] + "ID Voice(1 | -1)"

Id = int(argv[1])

# Загружаем приватный ключ этого сервера
keyfile = open(SERVERKEYFILES[Id][0], "r")
privatekey = RSA.importKey(keyfile.read())
keyfile.close()

# Глобальные переменные для суммирования голосов
global u, w
u = 0
w = 0

# Функция для учета голосов
def addVoice(uj, wj):
  global u, w
  u += uj
  w += wj

# Эта функция отвечает за работу с отдельным клиентом
def Handler(ss):
  data = ss.recv(100500)
  clientId, bulletin, signature = loads(privatekey.decrypt(b64decode(data)))
  clientId = int(clientId)
  
  # Загружаем публичный ключ этого клиента
  keyfile = open(CLIENTKEYFILES[clientId][1], "r")
  publickey = RSA.importKey(keyfile.read())
  keyfile.close()

  # Проверяем подпись
  isTrue = publickey.verify(bulletin, signature)
  if isTrue:
    uj, wj = loads(bulletin)
    addVoice(uj, wj)
    print uj, wj


if __name__ == "__main__":
  s = socket()
  print SERVERS[Id], PORTS[Id]
  s.bind((SERVERS[Id], PORTS[Id]))
  s.listen(100)
  for i in xrange(M):
    ss = s.accept()[0]
    Handler(ss)

  print u, w
  s.close()
  import time
  time.sleep(1)
  s = socket()
  s.connect((MAINSERVER, MAINPORT))
  s.send(b64encode(dumps((Id, u, w))))
  print s.recv(100)
  s.close()
  exit(0)
