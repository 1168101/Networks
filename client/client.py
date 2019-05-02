from socket import *
from codecs import decode

def main():
	HOST = 'localhost'
	PORT = 12003
	BUFFERSIZE = 1024
	ADDRESS = (HOST,PORT)
	CODE = 'ascii'

	user = False
	server = socket(AF_INET, SOCK_STREAM)
	server.connect(ADDRESS)
	print(decode(server.recv(BUFFERSIZE),CODE))
	serverHandler(server, CODE, BUFFERSIZE)



def serverHandler(server, CODE, BUFFERSIZE):
	while True:

		#print('Waiting for connection.....')


		command = input('Enter command: \n')

		while len(command) == 0:
			command = input('Enter valid command: \n')


		if command == 'exit':
			server.close()
			break
		responseHandler(server, command, CODE, BUFFERSIZE)



def responseHandler(server, command, CODE, BUFFERSIZE):
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


if __name__ == '__main__':
    main()
