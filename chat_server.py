from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connection():
    while True:
        client,client_adress = SERVER.accept()
        print("%s: %s si è collegato." % client)
        indirizzi[client] = client_adress
        Thread(target=handle_client, args=(client,)).start()
        
def handle_client(client):
    nome = client.recv(BUFSIZ).decode("utf8")
    benvenuto = "Benvenuto %s: se vuoi lasciare la chat, digita {quit} " %nome
    client.send(bytes(benvenuto,"utf8"))
    msg_br = "Utente %s si è unito alla chat " %nome
    broadcast(bytes(msg_br, "utf8"))
    clients[client] = nome

clients = {}
indirizzi = {}


HOST = ''
PORT = 5300
BUFSIZ = 1024
ADDR = (HOST,PORT)

SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)