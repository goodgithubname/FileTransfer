import os
import socket

# Define directory paths
uploaded_dir = 'uploaded'

#  Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 12345)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
print('Waiting for a connection')
sock.listen(1)

while True:
    # wait for connection
    connection, client_address = sock.accept()

    try:
        # Receive the file name and size
        filename = connection.recv(1024).decode().strip()
        filesize = int(connection.recv(1024).decode().strip())
        
        print('request for {}, {}'.format(filename, filesize))
        # Receive the file data
        data = b''
        while len(data) < filesize:
            chunk = connection.recv(1024)
            if not chunk:
                break
            data += chunk

        # Write the file data to a file
        with open(os.path.join(uploaded_dir, filename), 'wb') as f:
            f.write(data)
        
    finally:
        connection.close()
