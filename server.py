# Shania Ie
# CIS 41B
# Lab 5

# Description:
# This is a client-server application where the server can respond to a number of clients.
# Here, the each client will be assigned to a server where it shows the files and subdirectories under the current directory
# It also enables the client to enter a different path to look at the contents of different directories. The server handles
# all the commands needed to be done according to the user choice.

import socket
import os
import pickle
import threading
import sys

HOST = "localhost"      
PORT = 5551

def validateInput(args):
    '''calidateInput: checks whether the user enters the right number of clients. It must be less than 5 '''
    if len(args) == 1 or not args[1].isdigit():
        print("Usage: " + args[0] + " num of clients")
        exit()
    elif int(args[1]) > 5:
        print("Number of clients < 5 please")
        exit()    
        
def showFile(conn, directory):
    '''showFile: Shows all the files available in the current directory'''
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    data = pickle.dumps(files)
    conn.send(data)     

def subDir(conn, directory):
    '''subDir: Shows all the subdirectories available in the current directory'''
    subdirectories = [os.path.join(path,d) for (path, dirList, fileList) in os.walk(directory) for d in dirList]
    data = pickle.dumps(subdirectories)
    conn.send(data)    

def setPath(conn, directory):
    '''setPath: Changes the path according to the user entry, checks if path is available or not. If not, return invalid'''
    fromClient = conn.recv(4096).decode('utf-8')
    if os.path.isdir(fromClient):
        os.chdir(fromClient)
        newPath = curDir()
        conn.send(newPath.encode('utf-8'))
    else:
        fromClient = 'invalid path'
        conn.send(fromClient.encode('utf-8'))
        
def curDir():
    '''curDir: returns the current directory'''
    return os.getcwd()

def socketReceive(s, directory):
    '''socketReceive: Checks if there's any client available. If there is and user enters a choice, it will call the appropriate function'''
    try:
        (conn, addr) = s.accept()
        print("Sending", directory)
        conn.send(directory.encode('utf-8'))
        funcList = [showFile, subDir, setPath]
        d = {'f': 0, 'd': 1, 's': 2}
       
        while True:
            fromClient = conn.recv(4096).decode('utf-8')
            if fromClient[0] == 'q':
                break      
            directory = fromClient[1:]
            funcList[d[fromClient[0]]](conn, directory)
        
    except socket.timeout:
        print("Timed out")

def checkClient():
    '''checkClient: Creating threads to enable multiple clients in the server'''
    with socket.socket() as s:
        s.bind((HOST, PORT))
        validateInput(sys.argv)
        print("Server is up, hostname:", HOST, "port:", PORT)
        print(curDir())
        
        s.settimeout(30)
        s.listen()
        threads = []
        for i in range(int(sys.argv[1])):
            t = threading.Thread(target = socketReceive, args=(s, curDir()))
            threads.append(t)
            
        for t in threads:
            t.start()
            
        for t in threads:
            t.join()
                
       
def main():
    checkClient()
main()