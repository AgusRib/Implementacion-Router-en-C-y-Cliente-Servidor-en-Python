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
    def __init__(self):
        self.connection = None

    def connect(self, address, port):
        import socket
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((address, port))

    def __getattr__(self, name): #checkear si es lo mas conveniente, si no pudeo directamente implementar todo en el getattr o su alternativa
        def method(*args):
            return self.call_method(name, *args)
        return method #entiendo que la idea es terminarlo dps de un solo uso, no se si es asi, pero iria aca un:
        #clientSocket.close()

    def call_method(self, method_name, *args):
        

        # Create XML-RPC request
        request = ET.Element("methodCall") #investigar que poronga hace el ET
        method_name_elem = ET.SubElement(request, "methodName")
        method_name_elem.text = method_name
        params_elem = ET.SubElement(request, "params")

        for arg in args:
            param_elem = ET.SubElement(params_elem, "param")
            value_elem = ET.SubElement(param_elem, "value")
            value_elem.text = str(arg)  # Simplified for scalar values

        # Send request
        request_xml = ET.tostring(request, encoding='utf-8', xml_declaration=True)
        

        #NO USAR SENDALL !!!!!!!!!!!!!!!!!!!!!!!!!!
        self.connection.sendall(request_xml) #el encode() no va ahi adentro?
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # Receive response
        response = self.connection.recv(4096) #deberia dar con 1024 creo
        return self.parse_response(response)

    def parse_response(self, response):

        root = ET.fromstring(response)
        if root.tag == "methodResponse":
            value_elem = root.find("params/param/value")
            return value_elem.text if value_elem is not None else None
        else:
            raise Exception("Invalid response format")