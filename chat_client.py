#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf8")
            if not msg:
                break
            msg_list.insert(tkt.END, msg )
        except OSError:
            break
        
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        window.quit()
        window.destroy()
        client_socket.close()
        
        
        
def on_closing(event=None):
    my_msg.set("{quit}")
    send()
    
#setting up GUI
window = tkt.Tk()
window.title("Chat")
message_frame = tkt.Frame(window)
my_msg = tkt.StringVar()
my_msg.set("Write your messages here ! ")
scrollbar = tkt.Scrollbar(message_frame)
msg_list = tkt.Listbox(message_frame, height=20, width=70, yscrollcommand=scrollbar.set)
msg_list.insert(tkt.END, "Write your message in the box")
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
message_frame.pack()
entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()
window.protocol("WM_DELETE_WINDOW", on_closing)
    
HOST = input("Insert host address: ")
PORT = input("Insert host port: ")
if not PORT:
    PORT = 5300
else:
    PORT = int(PORT)
    
BUFSIZE = 1024
ADDR = (HOST,PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

tkt.mainloop()

