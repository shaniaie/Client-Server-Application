# Shania Ie
# CIS 41B
# Lab 5

# Description:
# This is a client-server application where the server can respond to a number of clients.
# Here, the each client will be assigned to a server where it shows the files and subdirectories under the current directory
# It also enables the client to enter a different path to look at the contents of different directories.

import socket
import pickle
import os

HOST = '127.0.0.1'
PORT = 5551

def checkMesg(mesg, directory): 
    '''checkMesg: Checks whether user enters a valid option, if not keep looping'''
    while mesg not in ('f','d','s','q'):
        print("Invalid input, re-enter")
        mesg = input("Enter choice: ")            
    return mesg + directory
    
def main():
    '''main: Connect client to the server, here happens the exchange of messages between server and client. Client will get the current directory
             of server. Then it will prompt the options where clients get to choose one of the following options. Will print an output according
             to the client's choice. If client enters 'q', it will exit from server.
    '''
    with socket.socket() as s :
        s.connect((HOST, PORT))
        print("Client connect to:", HOST, "port:", PORT)
        directory = s.recv(1024).decode('utf-8')
        print("Current directory:", directory)
        print("\ns.set path\nf.show files\nd.showdirs\nq.quit\n")
        mesg = input("Enter choice: ")         
        info = checkMesg(mesg, directory)
        s.send(info.encode('utf-8')) 

        checkFile = {'f': "No Files", 'd':"No subdirectories"}
        while mesg != 'q':
            choiceDict = {'f': 'Files found under ' + directory, 'd': 'Directories found under ' + directory, 's': "Enter a path, starting from current directory: "}
            if mesg in checkFile.keys():
                print(choiceDict[mesg])
                fromServer = pickle.loads(s.recv(4096))
                if not fromServer:
                    print(checkFile[mesg])
                else:
                    print('\n'.join(fromServer))
            else:
                path = input(choiceDict[mesg])
                newPath = os.path.join(directory, path)
                s.send(newPath.encode('utf-8'))
                receivedDir = s.recv(1024).decode('utf-8')
                if receivedDir == 'invalid path':
                    directory = directory           # this keeps the original directory as the path is invalid
                else:
                    directory = receivedDir
                print("new path:", receivedDir)

            print("\ns.set path\nf.show files\nd.showdirs\nq.quit\n")
            mesg = input("Enter choice: ")         
            info = checkMesg(mesg, directory)
            s.send(info.encode('utf-8')) 
main()