#import all libraries used
import threading
import socket
import sys
import logging
import os

#config logging and create logger object
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#creater formatter for logging
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#create file handler and set formatting
file_handler = logging.FileHandler('server.log')
file_handler.setFormatter(format)

#add file handler to logger object
logger.addHandler(file_handler)

#set encoding type
encoding = 'utf-8'

#set hostname and get port number from terminal
hostname = 'localhost'
port = int(sys.argv[1])

#create TCP/IP server socket and bind to hostname and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((hostname, port))

#starts listening for connections
server.listen()

#create lists for client connections and usernames
clients = []
usernames = []

#Function that brodadcasts messages to all connected clients
def message_broadcast(message):
    for client in clients:
        client.send(message)

#Function to handle client connections
def handle_client(client, client_address, parent_directory):
    #while loop to listen for more than one message
    while True:
        try:
            #get the index of current threads client from list of clients and get clients username
            position = clients.index(client)
            username = usernames[position]

            #accept and decode data from client
            message = client.recv(1024)
            decoded = message.decode(encoding)

            #remove client from list of clients and clean up connection
            if decoded == 'quit':
                clients.remove(client)
                client.close()

                #broadcast and log disconnection
                message_broadcast(f'{username} has left\n'.encode(encoding))
                logger.info(f'Client {username}: {client_address} left the server')
                usernames.remove(username)
            else:
                try:
                    #get filename and data of file from client 
                    command, filename, text = decoded.split("/")
                    if command == 'upload':
                        #create a new file in clients upload folder
                        path = os.path.join(parent_directory, username)
                        create_file = os.path.join(path, filename)
                        with open(create_file, 'w') as file:
                            file.write(text)
                except:
                    #broadcast and log client message
                    logger.info(f'Message from {username}: {client_address}: {decoded}')
                    message_broadcast(message)
        except:
            break

#Main function to receive the clients connection
def connection():
    #while loop to accept multiple client connections
    while True:

        #accept client connectios
        print('Server waiting for a connection...')
        client, client_address = server.accept()
        print(f'A client has connected from {str(client_address)}')

        #recieve username from client
        username = client.recv(1024).decode(encoding)
        usernames.append(username)
        clients.append(client)

        #set path for client
        parent_directory = '/Users/will/Documents/Uni/Year 2/Networks and Systems/Networks/Coursework'
        path = os.path.join(parent_directory, username)
        
        #create upload folder corresponding to clients username
        os.mkdir(path)

        #broadcast and log client connection
        print(f'Connection from {username}: {client_address}')
        message_broadcast(f'{username} has joined\n'.encode(encoding))
        logger.info(f'Client {username}: {client_address} joined the server')

        #send welcome message to client and instructions
        client.send('\nWelcome, you have connected to the server\n'.encode(encoding))
        client.send('\nEnter a message, type "quit" to exit or upload a text file using the following format; "upload/filenamme": '.encode(encoding))

        #create aand start a thread for the client
        thread = threading.Thread(target=handle_client, args=(client, client_address,parent_directory))
        thread.start()


if __name__ == "__main__":
    connection()