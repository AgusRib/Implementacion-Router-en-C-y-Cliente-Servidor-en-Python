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
        self.master.listen(1)

        print("Pronto el server para recibir ravioles!")

        while True:
            self.connectionSocket, _ = self.master.accept()
            response = None
            try:
                # Leo las lineas de cabecera hasta encontrar el separador \r\n\r\nd (un retorno de carro y dos enters)
                request = ""
                content_length = 0
                while '\r\n\r\n' not in request:
                    parte = self.connectionSocket.recv(1024).decode()
                    request += parte
                
                # Busco el Content-Length en las cabeceras
                found = False
                headers = request.split('\r\n\r\n')[0]
                for line in headers.split('\r\n'):
                    if not found and 'Content-Length:' in line:
                        content_length = int(line.split(':')[1].strip())
                        found = True
                
                # Leer el body con contentlenght como cond dee parada
                largocuerpo = len(request.split('\r\n\r\n')[1])
                while largocuerpo < content_length:
                    parte = self.connectionSocket.recv(1024).decode()
                    request += parte
                    largocuerpo += len(parte)

                # Unmarshallea el request de XML-RPC a string (lo hace automaticamente loads)
                try:  
                    params, method_name = loads(request.split('\r\n\r\n')[1])
                except Exception as e:
                    response = dumps(Fault(1, f"Error al parsear XML: {str(e)}"), methodresponse=True)#dumps marshallea la respuesta a XML
                else:
                    #Solo sigue si no hubo error de parsing
                    if method_name not in self.methods:
                        response = dumps(Fault(2, f"No existe el método: {method_name}"), methodresponse=True)
                    else:
                        try:
                            result = self.methods[method_name](*params)
                            response = dumps((result,), methodresponse=True)
                        except TypeError as e:
                            response = dumps(Fault(3, f"Error en parámetros del metodo invocado: {str(e)}"), methodresponse=True)
                        except Exception as e:
                            response = dumps(Fault(4, f"Error interno en la ejecución del metodo: {str(e)}"), methodresponse=True)

            except Exception as e:
                # Fault 5: Solo si ocurre un error no manejado
                if not response:  # Si no se seteo ninguna response específica
                    response = dumps(Fault(5, f"Error del servidor: {str(e)}"), methodresponse=True)

            finally:
                # Enviar la respuesta con el resu o el error
                responsebytes = response.encode()
                formateadohttp = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/xml\r\n"
                    f"Content-Length: {len(responsebytes)}\r\n"
                    "\r\n"
                )
                http_response = formateadohttp.encode() + responsebytes
                
                remaining = http_response
                while remaining:
                    sent = self.connectionSocket.send(remaining)
                    remaining = remaining[sent:]
                print("Respuesta enviada")
                self.connectionSocket.close()

