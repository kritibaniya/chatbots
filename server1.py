import os
import signal
import socket
import threading
import random
import time

# Get localhost
HOST = socket.gethostbyname(socket.gethostname())
# Port used to connect the TCP socket.
PORT = 7568

# bind method establishes the communication
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# enables the server to accept any connection
server.listen()

# an array where we will add clients and names of connected "bots/client"
clients = []
names = []


# Sends suggestion
def send_suggestion():
    # Initiate a convertation ist of questions to send
    questions = random.choice(["Want to play ?", "Let's run away", "work today"])
    # sends message to all clients
    message = "Extern : " + questions
    for c in clients:
        c.send(message.encode())


# Broadcast to everyone except the one who sent it
def broadcast(c, msg):
    for client in clients:
        if c != client:
            client.send(msg.encode())


# This function aim to disconnect clients from the chatserver.
def disconnect(client):
    # finds the index of the connection we want to remove and removes from both client list
    # and name list and close the client connection
    try:
        index = clients.index(client)
        clients.remove(client)

        client.close()
        name = names[index]
        msg = f"[DISCONNECTED] {name}"
        names.remove(name)

        print(msg)
        broadcast(client, msg)

    # Message when client is kicked out
    except:
        print("[Client removed]")


# Function that lets the server kick out any client
def kick(name):
    if name in names:
        name_index = names.index(name)
        client_to_kick = clients[name_index]
        client_to_kick.send("[You were kicked by Admin]".encode())
        print(f"Client {name} is kicked out!")
        disconnect(client_to_kick)


# Function that explains in line parameters if you call the program with "--help" or "-h"
def help_message(name):
    # If client asks for help
    if name in names:
        name_index = names.index(name)
        client_to_send = clients[name_index]
        message = "[Helpline]\n - How it works: \n " \
                  "Suggest an activity to the connected bots \n" \
                  "Type 'quit' to disconnect!\n" \
                  "You will automatically disconnect if you have been inactive for more than 2 minutes"

        client_to_send.send(message.encode())
    # When server "asks" for help
    else:
        message = "[Helpline]\n - How it works: \n " \
                  "Suggest an activity to the connected bots \n" \
                  "Type 'KICK' and username to kick a client out\n" \
                  "Type 'TERMINATE' to end the session"
        print(message)


def terminate(clients):
    time.sleep(150)
    length = len(clients)
    print(f"Going to close connection. Number of clients connected:{length}")
    if length == 0:
        os.kill(os.getpid(), signal.SIGINT)


# Handles the input from client
def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode()

            index = clients.index(client)
            name = names[index]

            if msg == f"{name} : h" or msg == f"{name} : help":
                return help_message(name)

            elif msg == f"{name} : quit":
                disconnect(client)
                break

            else:
                print(msg)
                broadcast(client, msg)
        except socket.timeout as e:
            print(e, "[Client inactive for too long!]")
            disconnect(client)
            break


# Send messages to the client
def send_to_client():
    while True:
        msg = input()
        if msg.startswith("help"):
            name = "Extern"
            return help_message(name)

        elif msg.startswith("TERMINATE"):
            os.kill(os.getpid(), signal.SIGINT)
        # kicking out unwanted clients with the function "kick".
        elif msg.startswith("KICK"):
            kick_name = msg[5:]
            kick(kick_name)

        else:
            # sends message to all clients
            message = f"Extern : {msg}"
            for c in clients:
                c.send(message.encode())


# start function
def start():
    while True:
        # accepts any clients
        client, addr = server.accept()

        # Setting a timer to disconnect if client takes too long to respond
        client.settimeout(90)

        # Ask for name of the client
        client.send("Name:".encode())

        # Receiving the name
        name = client.recv(1024).decode()

        # Add name in the list of names
        names.append(name)

        # Add client in the list of clients
        clients.append(client)

        # Print name of the client who joined and inform it to clients
        print(f"[{name} JOINED]")
        broadcast(client, f"[{name} JOINED]")
        client.send("[CONNECTED]\n".encode())

        # Initiate a conversation everytime there is a new connection
        send_suggestion()

        # Start the thread handle client
        handle_thread = threading.Thread(target=handle, args=(client,))
        handle_thread.start()

        # Starting the thread to send messages out
        send_thread = threading.Thread(target=send_to_client)
        send_thread.start()

        # Starting the thread to send terminate
        terminate_thread = threading.Thread(target=terminate, args=(clients,))
        terminate_thread.start()


print(f"[LISTENING FOR CONNECTIONS ...]")
# Run the function start
start()
