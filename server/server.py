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
#If the database is connected
if mydb:
    print('Database Connected.....')

#Main function
def main():
    HOST = ''   #Use the current IP as host
    PORT = 12000    #Control port
    ADDRESS = (HOST,PORT)   #Address for binding
    CODE = 'ascii'  #FTP default
    server = socket(AF_INET,SOCK_STREAM) #Create socket obj
    IP=getIP() #Get the current IP of the computer
    print('HOST address:',IP,' port:',PORT) #Display info for connecting client
    server.bind(ADDRESS) #Bind address
    server.listen(5) #Listen for connections
    print('Waiting for client connection...')
    
    while True:
        client, address = server.accept() #Accept connection
        print('Connected from: ', address)
        handler = myThread(client) #Create a thread for each client
        handler.start()
#Function for getting IP address
def getIP():
    s = socket(AF_INET,SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)) #Connect to IANA
        IP = s.getsockname()[0] #Get IP
    except:
        IP = '127.0.0.1' #Default
    finally:
        s.close() #Disconnect from IANA
    return IP
#Function for creating threads and running them
class myThread (Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
    def run(self):
        self.client.send(bytes('Welcome user','ascii'))
        clientHandler (self.client)
#Function for handling commands received from client
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
#Capitalises commands.
def acceptCommand(command):
    commandType = command[0:4]
    return commandType.upper()
    client.send(bytes(command.upper(),'ascii'))
#Function for splitting messages into command and argument. 
def extractValue(command):
    commandValue = ''

    if len(command) > 4:
        unstrippedCommand = command[4:]
        commandValue = unstrippedCommand.strip()
        return commandValue
    else:
        return commandValue


#Function for checking username
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
#Function for checking password
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
#Check db for root folder
def rootNamer(username):
    cursor = mydb.cursor()
    sql = "select root from user where name = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]
#Switch for various commands
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
        client.send(bytes('150 File status okay; about to open data connection.','ascii'))
        clientIP = client.getpeername()[0]
        receiveFile(rootName, commandValue, fileType,clientIP)
    elif commandType == 'STRU':
        client.send(bytes('225 querying file structure', 'ascii'))
        clientIP = client.getpeername()[0]
        fileStructure(rootName,clientIP)
    else:
        client.send(bytes('502 command not implemented','ascii'))


#Function for RETR command
def transferFile(dirName, fileName, fileType,clientIP):
    HOST = clientIP
    PORT = 13000
    BUFFERSIZE = 1024
    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
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
#Function for STRU
def fileStructure(rootName,clientIP):

    HOST = clientIP
    PORT = 14000
    BUFFERSIZE = 1024
    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(ADDRESS)

    for root, dirs, files in os.walk("." + os.sep + rootName):
        for filename in files:
            client.send(bytes(filename,'ascii'))
            print(filename)
    client.close()


#Function for STOR
def receiveFile(dirName, fileName, fileType,clientIP):
    HOST = clientIP
    PORT = 15000

    ADDRESS = (HOST,PORT)
    CODE = 'ascii'
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

#Run Main function
if __name__ == '__main__':
    main()
