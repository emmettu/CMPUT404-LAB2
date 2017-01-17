#!/usr/bin/env python

import socket

#AF_INET indicates we want ipv4
#SOCK STREAM indicates we want TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#There is no http://
#Port 80 is the standard http port
clientSocket.connect(("www.google.com", 80))

request = "GET / HTTP/1.0\r\n\r\n"

clientSocket.sendall(request)

response = bytearray()

while True:
	part = clientSocket.recv(1024)
	if (part):
		response.extend(part)
	else:
		break

print response
