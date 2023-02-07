#import all libraries used
import threading
import socket
import sys
import os

#get arguments from terminal
username = sys.argv[1]
hostname = sys.argv[2]
port = int(sys.argv[3])

#set encoding type
encoding = 'utf-8'

#create TCP/IP client socket
client_address = (hostname, port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(client_address)

#send username to server
client.send(username.encode(encoding))

#function to send messages to the server
def send_message():
    #while loop to allow client to send multiple messages
    while True:
        #get message from client
        message = input("")
        #send meesage to server and close socket
        if message == 'quit':
            client.send('quit'.encode(encoding))
            client.close()
            break
        else:
            try:
                #get data from text file
                command, filename = message.split("/")
                if command == 'upload':
                    if os.path.isfile(filename):
                        with open(filename, "r") as f:
                            text = f.read()
                        #send command and text file data to server
                        client.send(f'{message}/{text}'.encode(encoding))
                    else:
                        print('File does not exist, enter a filename that is in the current directory')
            except:
                #send message to server
                client.send(f'{username}: {message}'.encode(encoding))

#function to receive messages from the server
def receive_message():
    #while loop to allow client to receive multiple messages from server
    while True:
        try:
            #receive and message from server and output to client
            message = client.recv(1024).decode(encoding)
            print(message)
        except:
            #close socket
            client.close()
            break

#start thread for client to send data to server
send = threading.Thread(target=send_message)
send.start()

#start thread for client to receive data from server
receive = threading.Thread(target=receive_message)
receive.start()