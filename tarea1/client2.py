from socket import *
import socket
import _socket
import xml.etree.ElementTree as ET
from xmlrpc.client import loads, dumps, Fault


#from socket import *
#serverPort = 12000
#serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.bind((’’,serverPort))
#serverSocket.listen(1)
#print(’The server is ready to receive’)
#while True:
#self.client, addr = serverSocket.accept()
#sentence = client.recv(10).decode()
#capitalizedSentence = sentence.upper()
#client.send(capitalizedSentence.encode())
#client.close()

class Client:

    def __init__(self):
        self.master = None
        #self.master.bind(("*", 0))
        self.client = None
        self.err = None
        self.address = None
        self.port = None 


    #capaz que el connect es init Y connect, lo q pide la letra
    def connect(self, address, port):
        self.master = socket.socket(AF_INET, SOCK_STREAM)
        self.master.connect((address, port))
        self.client = self.master
        self.err = None
        self.address = address
        self.port = port
    #---------------/\ REVISAR /\---------------------



    def __getattr__(self, name): #checkear si es lo mas conveniente, si no pudeo directamente implementar todo en el getattr o su alternativa
        def method(*args):
            return self.call_method(name, *args)
        return method #entiendo que la idea es terminarlo dps de un solo uso, no se si es asi, pero iria aca un:
        #clientSocket.close()

    def call_method(self, method_name, *args):
        

        # Creo el respuesta XML-RPC----------
        envio_xml = dumps(tuple(args), methodname=method_name)

        # Agregamos el formato HTTP
        envio_xmlBytes = envio_xml.encode()
        formateadohttp = (
            "POST /RPC2 HTTP/1.0\r\n"
            "User-Agent: fedora/28.5.04 (Fedora42)\r\n"
            f"Host: {self.address}:{self.port}\r\n"
            "Content-Type: text/xml\r\n"
            f"Content-Length: {len(envio_xmlBytes)}\r\n"
            "\r\n"
        )
        envio_http = formateadohttp.encode() + envio_xmlBytes
        #-----------------------------------

        # Enviamo --------------------------
        total_sent = 0
        while total_sent < len(envio_http):
          sent = self.client.send(envio_http.encode()[total_sent:])
          total_sent += sent
        #-----------------------------------        

        # Recibimo -------------------------
        try:
            # Leo las lineas de cabecera hasta encontrar el separador \r\n\r\nd (un retorno de carro y dos enters)
            respuesta = ""
            content_length = 0
            while '\r\n\r\n' not in respuesta:
                parte = self.client.recv(10).decode()
                respuesta += parte
            
            # Busco el Content-Length en las cabeceras
            found = False
            headers = respuesta.split('\r\n\r\n')[0]
            for line in headers.split('\r\n'):
                if not found and 'Content-Length:' in line:
                    content_length = int(line.split(':')[1].strip())
                    found = True
            
            # Leer el body con contentlenght como cond de parada
            largocuerpo = len(respuesta.split('\r\n\r\n')[1])
            while largocuerpo < content_length:
                parte = self.client.recv(10).decode()
                respuesta += parte
                largocuerpo += len(parte)

            # Unmarshallea el respuesta de XML-RPC a string (lo hace automaticamente loads)
            try:  
                resultado = loads(respuesta.split('\r\n\r\n')[1])
            except Exception as e:
                print(f"Fault 1, Error al parsear XML: {str(e)}")
            else:
                #Solo sigue si no hubo error de parsing
                return resultado[0][0]  #el loads devuelve una tupla (params, methodname), params es una tupla (resu,)

        except Exception as e:
                # Fault 5: Solo si ocurre un error no manejado
                print("Fault 5, Error no manejado")

        #-----------------------------------    