#For the socket
from socket import *
from codecs import decode
from threading import Thread
import pickle
import os, os.path

#for the database
import mysql.connector

BUFFERSIZE = 1024

COMMANDS = ['USER']

#Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="heavens1",
    database="networks"
)

if mydb:
    print('Database Connected.....')


def main():


    HOST = ''
    PORT = 12000

    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    server = socket(AF_INET,SOCK_STREAM)
    IP=getIP()
    print('HOST address:',IP,' port:',PORT)
    server.bind(ADDRESS)
    server.listen(5)
    print('Waiting for client connection...')

    while True:
        client, address = server.accept()
        print('Connected from: ', address)
        handler = myThread(client)
        handler.start()

def getIP():
    s = socket(AF_INET,SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class myThread (Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
    def run(self):
        self.client.send(bytes('Welcome user','ascii'))
        clientHandler (self.client)






def clientHandler (client):
    isUsername = False
    username = ''
    isPassword = False
    password = ''
    command = ''
    rootName = ''
    fileType = 'rb'
    while True:
        message = decode(client.recv(BUFFERSIZE), 'ascii')


        print('Received message is', message)
        if not message:
            print('Client disconnected')
            client.close()
            break
        else:
            commandType = acceptCommand(message)
            commandValue = extractValue(message)
            print('command type: ', commandType)
            print('command value: ', commandValue)
            if isUsername == False:
                isUsername = userNameConfirmation(client, commandType, commandValue)
                if isUsername == True:
                    username = commandValue
            elif isPassword == False:
                isPassword = passwordConfirmation(client, commandType, commandValue, username)
                if isPassword == True:
                    rootName = rootNamer(username)
                    print('current working directory ', rootName)
            elif isUsername == True and isPassword == True:
                processCommand(client, commandType, commandValue, username, password, rootName, fileType)

            #processCommand(client, commandType, commandValue)

def acceptCommand(command):
    commandType = command[0:4]
    return commandType.upper()
    #print('first four ', comandType)
    client.send(bytes(command.upper(),'ascii'))

def extractValue(command):
    commandValue = ''

    if len(command) > 4:
        unstrippedCommand = command[4:]
        commandValue = unstrippedCommand.strip()
        return commandValue
    else:
        return commandValue



def userNameConfirmation(client, commandType, commandValue):
    if commandType != 'USER':
        client.send(bytes('530 Enter user name','ascii'))
        return False

    elif commandType == 'USER':
        cursor = mydb.cursor()
        sql = "select count(*) as counter from user where name =  '%s'" % (commandValue)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result[0][0] == 0:
            client.send(bytes('530 Enter user name','ascii'))
            return False
        elif result[0][0] == 1:
            client.send(bytes('331 User name accepted, please enter your password','ascii'))
            return True

def passwordConfirmation(client, commandType, commandValue, username):

    if commandType != 'PASS':
        client.send(bytes('503 Please use correct command,  which is "PASS"','ascii'))
        return False

    if commandType == 'PASS':
        cursor = mydb.cursor()
        sql = "select count(*) from user where name = '%s' and password = '%s'" % (username, commandValue)
        cursor.execute(sql)
        result = cursor.fetchall()

        if result[0][0] == 0:
            print('the result ', result)
            client.send(bytes('530 Not logged in.','ascii'))
            return False
        elif result[0][0] == 1:
            client.send(bytes('230 User logged in, proceed.','ascii'))
            return True

def rootNamer(username):
    cursor = mydb.cursor()
    sql = "select root from user where name = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]

def processCommand(client, commandType, commandValue, username, password, rootName, fileType):
    message = commandType + ' ' + commandValue
    if commandType == 'NOOP':
        client.send(bytes('200 OK', 'ascii'))
    elif commandType == 'RETR':
        if os.path.exists(os.getcwd() + os.sep + rootName +os.sep +commandValue):
            client.send(bytes('125 Data connection already open; transfer starting.', 'ascii'))
            clientIP = client.getpeername()[0]
            transferFile(rootName, commandValue, fileType,clientIP)
        else :
            #print(os.getcwd() + os.sep + rootName +os.sep +commandValue,'does not exist')
            client.send(bytes('450 file not found', 'ascii'))
    elif commandType == 'STOR':
        #client.send(bytes('502 command not implemented','ascii'))
        client.send(bytes('150 File status okay; about to open data connection.','ascii'))
        clientIP = client.getpeername()[0]
        receiveFile(rootName, commandValue, fileType,clientIP)
    elif commandType == 'STRU':
        client.send(bytes('225 querying file structure', 'ascii'))
        clientIP = client.getpeername()[0]
        fileStructure(rootName,clientIP)
    else:
        client.send(bytes('502 command not implemented','ascii'))



def transferFile(dirName, fileName, fileType,clientIP):
    HOST = clientIP
    PORT = 13000
    BUFFERSIZE = 1024
    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    #server = socket(AF_INET,SOCK_STREAM)
    #server.bind(ADDRESS)
    #server.listen(5)
    #client, address = server.accept()
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(ADDRESS)
    theFile = dirName + os.sep + fileName

    f = open(theFile,'rb')
    while True:
        l = f.read(BUFFERSIZE)
        while (l):
            client.send(l)
            l = f.read(BUFFERSIZE)
        if not l:
            f.close()
            client.close()
            break

def fileStructure(rootName,clientIP):

    HOST = clientIP
    PORT = 14000
    BUFFERSIZE = 1024
    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    #server = socket(AF_INET,SOCK_STREAM)
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(ADDRESS)
    #server.bind(ADDRESS)
    #server.listen(5)
    #client, address = server.accept()

    for root, dirs, files in os.walk("." + os.sep + rootName):
        for filename in files:
            client.send(bytes(filename,'ascii'))
            print(filename)
    client.close()



def receiveFile(dirName, fileName, fileType,clientIP):
    HOST = clientIP
    PORT = 15000

    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    #server = socket(AF_INET,SOCK_STREAM)
    #server.bind(ADDRESS)
    #server.listen(5)
    #client, address = server.accept()
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(ADDRESS)
    theUser = os.getcwd() + os.sep + dirName + os.sep + fileName

    with open(theUser, 'wb') as f:

        while True:
        	data = client.recv(BUFFERSIZE)
        	if not data:
        		f.close()
        		break
        	f.write(data)
        print('file received')


if __name__ == '__main__':
    main()
