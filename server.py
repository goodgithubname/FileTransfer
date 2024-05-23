import os
import socket

# Define directory paths
uploaded_dir = 'uploaded'

#  Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# function to get outbound ip
def get_outbound_ip():
    # Connect to a remote server on port 80 (http)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if this address is reachable
        sock.connect(('10.255.255.255', 1))
        ip = sock.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip

# Bind the socket to the address and port
server_address = (get_outbound_ip(), 12345)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
print('Waiting for a connection')
sock.listen(1)

while True:
    # wait for connection
    connection, client_address = sock.accept()

    # Check if directory exists, if not, create it
    if not os.path.exists(uploaded_dir):
        os.makedirs(uploaded_dir)

    try:
        # Receive the file name and size
        received = connection.recv(1024).decode().strip()
        print(received)
        filename, received_filesize, _ = received.split('\n', 2)
        print(f"Received filename: {filename}")
        print(f"Received filesize: {received_filesize}")
        filesize = int(received_filesize)
        print(f"Sending file size: {filesize}")

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
