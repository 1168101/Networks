from socket import *
from codecs import decode
import pickle
import os, os.path

import time



def main():
	HOST = 'localhost'
	PORT = 12000
	BUFFERSIZE = 1024
	#ADDRESS = (HOST,PORT)
	ADDRESS = connectionHandler()
	CODE = 'ascii'
	fileType = 'wb'
	user = False
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)
	print(decode(server.recv(BUFFERSIZE),CODE))
	serverHandler(server, CODE, BUFFERSIZE, fileType)

def connectionHandler():
	while True:
		command = input('Enter PORT information: \n')
		while len(command) == 0:
			command = input('Enter valid PORT command: \n')
		commandType = command[0:4]
		commandValue = extractValue(command)
		if command == 'quit':
			break
		if commandType == 'port':
			h1,h2,h3,h4,p1,p2 = commandValue.split(',')
			PORT1 = int(p1)
			PORT2 = int(p2)
			HOST = h1 + '.' + h2 + '.' + h3 + '.' + h4
			ADDRESS = (HOST,PORT1)
			return ADDRESS
			break

def serverHandler(server, CODE, BUFFERSIZE, fileType):
	while True:

		#print('Waiting for connection.....')


		command = input('Enter command: \n')

		while len(command) == 0:
			command = input('Enter valid command: \n')


		if command == 'quit':
			server.close()
			break
		responseHandler(server, command, CODE, BUFFERSIZE, fileType)



def responseHandler(server, command, CODE, BUFFERSIZE, fileType):
	server.send(bytes(command, CODE))
	response = decode(server.recv(BUFFERSIZE),CODE)

	responseCode = response[0:3]

	if responseCode == '530':
		print(response)
	elif responseCode == '230':
		print(response)
	elif responseCode == '503':
		print(response)
	elif responseCode == '331':
		print(response)
	elif responseCode == '200':
		print(response)
	elif responseCode == '502':
		print(response)
	elif responseCode == '450':
		print(response)
	elif responseCode == '125':
		print(responseCode)
		fileName = extractValue(command)
		receiveFile(fileName, fileType, BUFFERSIZE)
	elif responseCode == '150':
		print(responseCode)
		fileName = extractValue(command)
		if os.path.exists(os.getcwd()+os.sep + fileName):
			fileName = extractValue(command)
			serverIP = server.getpeername()[0]
			transferFile(fileName, fileType, BUFFERSIZE,serverIP)
		else :
			print(os.getcwd() + os.sep +fileName,'does not exist')
	elif responseCode == '225':
		fileStructure()



def receiveFile(fileName, fileType, BUFFERSIZE):
	HOST = ''
	PORT = 13000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	#server.connect(ADDRESS)
	server.bind(ADDRESS)
	server.listen(5)
	client,address = server.accept()
	with open(fileName, 'wb') as f:

		while True:
			#data = server.recv(BUFFERSIZE)
			data = client.recv(BUFFERSIZE)
			if not data:
				f.close()
				break
			f.write(data)
		print('file received')


def transferFile(fileName, fileType, BUFFERSIZE,serverIP):
	HOST = serverIP
	PORT = 15000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	#server.connect(ADDRESS)
	server.bind(ADDRESS)
	server.listen(5)
	client,address = server.accept()

	f = open(fileName,'rb')
	while True:
	    l = f.read(BUFFERSIZE)
	    while (l):
		    client.send(l)
		    l = f.read(BUFFERSIZE)
	    if not l:
	        f.close()
	        client.close()
	        break
	print('sent ')

def extractValue(command):
    commandValue = ''

    if len(command) > 4:
        unstrippedCommand = command[4:]
        commandValue = unstrippedCommand.strip()
        return commandValue
    else:
        return commandValue

def fileStructure():
	HOST = ''
	PORT = 14000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	server.bind(ADDRESS)
	server.listen(5)
	client,address = server.accept()

	recvd_data = []

	while True:
		data = decode(client.recv(BUFFERSIZE),'ascii')

		if not data:
			break

		recvd_data.append(data)

	print('File structure\n', recvd_data)

if __name__ == '__main__':
    main()
