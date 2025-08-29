from socket import *
import socket
import xml.etree.ElementTree as ET


    #serverName = ’servername’
    #serverPort = 12000
    #clientSocket = socket(AF_INET, SOCK_STREAM)
    #clientSocket.connect((serverName,serverPort))
    #sentence = input(’Input lowercase sentence:’)
    #clientSocket.send(sentence.encode())
    #modifiedSentence = clientSocket.recv(1024)
    #print(’From Server: ’, modifiedSentence.decode())
    #clientSocket.close()

class Client:

    #acorde al curso--------------------
    def __init__(self):
        self.master = None
        #self.master.bind(("*", 0))
        self.client = None
        self.err = None

    def connect(self, address, port):
        self.master = socket.socket(AF_INET, SOCK_STREAM)
        self.master.connect((address, port))
        self.client = self.master
        self.err = None
    #-----------------------------------

    def andar(self):
        sentence = input('Input lowercase sentence:')

        remain = sentence
        total_sent = 0
        while total_sent < len(sentence):
          sent = self.client.send(sentence.encode()[total_sent:])
          total_sent += sent
          

        modifiedSentence = self.client.recv(10)
        print('From Server: ', modifiedSentence.decode())
        self.client.close()