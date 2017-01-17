#!/usr/bin/env python

import socket
import os, sys, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tell it to reuse the address, each server must have its own port
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Only root users can use ports under 1024, so here we use 8000
# 0.0.0.0 means every address on this machine
serverSocket.bind(("0.0.0.0", 8000))
serverSocket.listen(5)

while True:
	(incomingSocket, address) = serverSocket.accept()
	print "We got a connection from %s" % (str(address))

	if os.fork() != 0:
		continue

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(("www.google.com", 80))

	clientSocket.setblocking(0)
	incomingSocket.setblocking(0)

	while True:
		request = bytearray()
		while True:
			try:
				part = incomingSocket.recv(1024)
			except IOError, e:
				if e.errno == 11:
					part = None
				else:
					raise
			if (part):
				clientSocket.sendall(part)
				request.extend(part)
			elif part is None:
				break
			else:
				sys.exit(0)

		if len(request) > 0:
			print request

		response = bytearray()
		while True:
			try:
				part = clientSocket.recv(1024)
			except IOError, e:
				if e.errno == 11:
					part = None
				else:
					raise
			if (part):
				incomingSocket.sendall(part)
				response.extend(part)
			elif part is None:
				break
			else:
				sys.exit(0)
		if len(response) > 0:
			print response
		select.select(
			[incomingSocket, clientSocket], #read
			[],				#write
			[incomingSocket, clientSocket], #exceptions
			1.0) #timeout
