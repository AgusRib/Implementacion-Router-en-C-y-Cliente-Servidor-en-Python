
from server2 import Server

def suma(a, b):
    return a + b

def main():
    server2 = Server("127.0.0.1", 12000)
    server2.add_method(suma)
    server2.serve()

if __name__ == "__main__":
    main()