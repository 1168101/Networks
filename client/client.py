from socket import *
from codecs import decode
import pickle

import time


def main():
	HOST = 'localhost'
	PORT = 12000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	CODE = 'ascii'
	fileType = 'wb'
	user = False
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)
	print(decode(server.recv(BUFFERSIZE),CODE))
	serverHandler(server, CODE, BUFFERSIZE, fileType)



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
	elif responseCode == '205':
		print(responseCode)
		fileName = extractValue(command)
		#transferFile(fileName, fileType, BUFFERSIZE)
	elif responseCode == '225':
		fileStructure()



def receiveFile(fileName, fileType, BUFFERSIZE):
	HOST = 'localhost'
	PORT = 13000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)
	with open(fileName, 'wb') as f:

		while True:
			data = server.recv(BUFFERSIZE)
			if not data:
				f.close()
				break
			f.write(data)
		print('file received')

'''
def transferFile(fileName, fileType, BUFFERSIZE):
	HOST = 'localhost'
	PORT = 15000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)

	f = open(fileName,'rb')
	while True:
	    l = f.read(BUFFERSIZE)
	    while (l):
	        server.send(l)
	        l = f.read(BUFFERSIZE)
	    if not l:
	        f.close()
	        server.close()
	        break
	print('sent ')
'''
def extractValue(command):
    commandValue = ''

    if len(command) > 4:
        unstrippedCommand = command[4:]
        commandValue = unstrippedCommand.strip()
        return commandValue
    else:
        return commandValue

def fileStructure():
	HOST = 'localhost'
	PORT = 14000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)

	recvd_data = []

	while True:
		data = decode(server.recv(BUFFERSIZE),'ascii')

		if not data:
			break

		recvd_data.append(data)

	print('File structure\n', recvd_data)

if __name__ == '__main__':
    main()
