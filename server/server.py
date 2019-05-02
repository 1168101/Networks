#For the socket
from socket import *
from codecs import decode
from threading import Thread

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


    HOST = 'localhost'
    PORT = 12003

    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    server = socket(AF_INET,SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(5)
    print('Waiting for client connection...')

    while True:
        client, address = server.accept()
        print('Connected from: ', address)
        handler = myThread(client)
        handler.start()


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
            elif isUsername == True and isPassword == True:
                processCommand(client, commandType, commandValue)

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

def processCommand(client, commandType, commandValue):
    message = commandType + ' ' + commandValue
    client.send(bytes(message,'ascii'))

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
            print('the result ', result)
            client.send(bytes('230 User logged in, proceed.','ascii'))
            return True


if __name__ == '__main__':
    main()
