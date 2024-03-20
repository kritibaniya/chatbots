import socket
import threading
import bots

# Commandline parameters. This input will be used to connect to the server
IP = input("IP: ")
Port1 = input("Port:")
PORT = int(Port1)
print("You can connect as yourself or a bot. Bots you can choose between: Joy, Sadness, Fear and Anger ")
name = input()
ADDR = (IP, PORT)

# Creating a TCP socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# This function aims to send input from commandline to server
def send():
    while True:
        try:
            # input from the commandline/terminal
            msg = f"{name} : {input()}"

            # Client can disconnect by typing "quit" and a message is sent to inform the server.
            if msg == f"{name} : quit":
                client.send(msg.encode())
                client.close()
            # Else will the message be sent normally
            else:
                client.send(msg.encode())

        # Throws error message if there is problem sending input to the server.
        except:
            print("ERROR: Can't send")
            client.close()
            break


# This function aim to receive messages from server and handle them
def receive():
    while True:
        try:

            # receive and decodes the received message
            msg = client.recv(1024).decode()

            # Split message to validate
            word_inn = msg.split()[0]
            updates = msg.split()[0][0]

            # initializing bad_chars_list
            bad_chars = ['[', ']', ';', ':', '!', "*"]

            # using join() + generator to
            # remove bad_chars
            word = ''.join(i for i in word_inn if not i in bad_chars)

            # if message from the server is to type your name, we should type your name
            if msg == "Name:":
                client.send(name.encode())

            # if message from server includes "Extern:", get responses from bots

            elif "Extern : " in msg or "[" != updates:
                if word not in bots.bot_list:
                    print(msg)
                    message = bots.bot(msg, name)
                    if message:
                        print(message)
                        client.send(f"{name} : {message}".encode())
                else:
                    print(msg)
                # print message if the received message is from other connected bots
            else:
                print(msg)
        except:
            # exception if the connection is broken
            print("ERROR: Disconnect")
            client.close()
            break


# Validates input and returns True if everything is well
def validate():
    try:
        # exception if the IP address is missing.
        if len(IP) == 0 or IP is None:
            raise Exception("Missing IP address")

        # exception if port is missing or a negative number
        if PORT is None or PORT < 0:
            raise Exception("Target port error")
        return True

    # collects all the exceptions and shows error message.
    except Exception as e:
        print(f"{e} - please try again.")
        return False


def start():
    # Connects to the server only after the input is validated
    if validate() is True:
        try:
            client.connect(ADDR)

            # A thread that starts send function independently
            send_thread = threading.Thread(target=send)
            send_thread.start()

            # A thread that starts send function independently
            receive_thread = threading.Thread(target=receive)
            receive_thread.start()

        except:
            print("Connection failed")


start()
