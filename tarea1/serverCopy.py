from socket import *
import socket
import _socket
#import xmlrpc
#from xmlrpc import parse_request, generate_response 

#from socket import *
#serverPort = 12000
#serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.bind((’’,serverPort))
#serverSocket.listen(1)
#print(’The server is ready to receive’)
#while True:
#self.connectionSocket, addr = serverSocket.accept()
#sentence = connectionSocket.recv(1024).decode()
#capitalizedSentence = sentence.upper()
#connectionSocket.send(capitalizedSentence.encode())
#connectionSocket.close()

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.master = None      
        #self.master.bind(("*", 0))
        self.server = None
        self.connectionSocket = None
        self.err = None
        self.methods = {}


    def add_method(self, method):
        self.methods[method.__name__] = method

    def serve(self):

        self.master = socket.socket(AF_INET,SOCK_STREAM)
        self.master.bind((self.address, self.port))
        self.master.listen(5)

        print("Pronto el server para recibir ravioles!")

        while True:
            self.connectionSocket, addr = self.master.accept()

            
        
            sentence = self.connectionSocket.recv(4096).decode()
            capitalizedSentence = sentence.upper()
            
            total_sent = 0
            while total_sent < len(capitalizedSentence):
              sent = self.connectionSocket.send(capitalizedSentence.encode()[total_sent:])
              total_sent += sent
            print(capitalizedSentence)
             
            self.connectionSocket.close()
            print("Ravioles servidos!")

