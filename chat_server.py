#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connection():
    while True:
        client,client_adress = SERVER.accept()
        print("%s: %s has connected." % client_adress)
        indirizzi[client] = client_adress
        Thread(target=handle_client, args=(client,)).start()
        
def handle_client(client):
    try: 
        nome = client.recv(BUFSIZ).decode("utf8")
        benvenuto = "Welcome %s: if you want left the chat, digita {quit} " % nome
        client.send(bytes(benvenuto,"utf8"))
        msg_br = "User %s has joined the chat " % nome
        broadcast(bytes(msg_br, "utf8"))
        clients[client] = nome
    except ConnectionResetError:
        print("Client has not logged in the chat")
        
    
    while True:
        try:
            msg = client.recv(BUFSIZ)
        except:
            print("Connection with client was interrupted")
            break
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg,nome + " : ")
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
            except ConnectionResetError:
                print("Connection was closed by client")
                    
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat. " % nome, "utf8"))
            break
        
def broadcast(msg, prefisso=""):
    for user in clients:
        user.send(bytes(prefisso,"utf8") + msg)

clients = {}
indirizzi = {}


HOST = ''
PORT = 5300
BUFSIZ = 1024
ADDR = (HOST,PORT)

SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connections... ")
    ACCEPT_THREAD = Thread(target=accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()