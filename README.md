Instructions on running the code:
Before the code can be run, MySQL needs to be installed.
1.) Install MySQL.
2.) At line 17 in the server.py file: change the host, username password and database name to reflect the details being used in MySQL.
3.) Create a table in MySQL using the following commands:

create table user (id int NOT NULL AUTO_INCREMENT,name char(50), password char(50), root char(50),PRIMARY KEY (id));

insert into user (name,password,root) values ('sauce1','juice1','files');

You can use other name, password and root values if you wish.

3.5) Create a folder called "files" in the server directory. This will act as the server's root folder.
4.) The code server.py should be able to run now. It will display the IP and port number.
5.) Run client.py
6.) Enter the following command:

port 127,0,0,1,12000,13000

or if using a remote P.C

port xxx,xxx,xxx,xxx,12000,13000

where xxx are the colon separated fields of the IP address shown in the server console.
7.) If the connection is successful enter:
user sauce1
8.)If successful enter:
pass juice1
9.) If successful the following commands can be used:

STRU - returns the list of files contained in the root folder of the server.
RETR <filename> - Downloads a file from the root folder of the server.
STOR <filename> - Uploads a file from the "client" folder to the root folder of the server.
NOOP - No operation.
QUIT - Closes the client session.