from server2 import Server
import time
import threading

def suma(a, b):
    return a + b


def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a/b

def ordenar(numeros):
    return sorted(numeros)
    
def quienEs():
    return "Soy Yo..."

def CerrarServer(server):
   time.sleep(10)
   server.master.close()

def main():
    server1 = Server("150.150.0.2", 17000)
    server1.add_method(suma)
    server1.add_method(multiplicar)
    server1.add_method(ordenar)
    server1.add_method(dividir)
    server1.add_method(quienEs)
    thread=threading.Thread(
                target=CerrarServer,
                args=(server1,)
            )
    thread.start()
    server1.serve()
    



    

if __name__ == "__main__":
    main()