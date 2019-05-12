from socket import *
from codecs import decode
import pickle
import os, os.path

import time


#Main Function
def main():
	PORT = 12000
	BUFFERSIZE = 1024
	ADDRESS = connectionHandler() #Get IP info from PORT command
	CODE = 'ascii'
	fileType = 'wb'
	user = False
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)
	print(decode(server.recv(BUFFERSIZE),CODE))
	serverHandler(server, CODE, BUFFERSIZE, fileType)
#Function for PORT command. QUIT also works here.
def connectionHandler():
	while True:
		command = input('Enter PORT information: \n')
		while len(command) == 0:
			command = input('Enter valid PORT command: \n')
		commandType = command[0:4]
		commandValue = extractValue(command)
		if command == 'quit' or command=='QUIT':
			break
		if commandType == 'port' or command=='PORT':
			h1,h2,h3,h4,p1,p2 = commandValue.split(',') #FTP standard for PORT
			PORT1 = int(p1)
			PORT2 = int(p2)
			HOST = h1 + '.' + h2 + '.' + h3 + '.' + h4
			ADDRESS = (HOST,PORT1)
			return ADDRESS
			break
#Function for inputting commands after connection
def serverHandler(server, CODE, BUFFERSIZE, fileType):
	while True:

		#print('Waiting for connection.....')


		command = input('Enter command: \n')

		while len(command) == 0:
			command = input('Enter valid command: \n')


		if command == 'quit' or command=='QUIT':
			server.close()
			break
		responseHandler(server, command, CODE, BUFFERSIZE, fileType)


#Switch for various commands
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
			transferFile(fileName, fileType, BUFFERSIZE)
		else :
			print(os.getcwd() + os.sep +fileName,'does not exist')
	elif responseCode == '225':
		fileStructure()


#Function for RETR
def receiveFile(fileName, fileType, BUFFERSIZE):
	HOST = ''
	PORT = 13000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
	server.bind(ADDRESS)
	server.listen(5)
	client,address = server.accept()
	with open(fileName, 'wb') as f:

		while True:
			data = client.recv(BUFFERSIZE)
			if not data:
				f.close()
				break
			f.write(data)
		print('file received')

#Function for STOR
def transferFile(fileName, fileType, BUFFERSIZE):
	HOST = ''
	PORT = 15000
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	server = socket(AF_INET, SOCK_STREAM)
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
#Function for splitting command and argument
def extractValue(command):
    commandValue = ''

    if len(command) > 4:
        unstrippedCommand = command[4:]
        commandValue = unstrippedCommand.strip()
        return commandValue
    else:
        return commandValue
#Function for STRU
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
#Run MAIN
if __name__ == '__main__':
    main()
